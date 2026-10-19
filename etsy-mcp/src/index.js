#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import { basename } from "node:path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { config } from "./config.js";
import { EtsyClient, money } from "./etsy.js";
import { buildInventoryUpdate } from "./inventory.js";

const etsy = new EtsyClient();
const server = new McpServer({ name: "sunnozy-etsy", version: "0.1.0" });

const ok = (data) => ({ content: [{ type: "text", text: JSON.stringify(data, null, 2) }] });
const fail = (err) => ({ content: [{ type: "text", text: `Fehler: ${err.message}` }], isError: true });

function tool(name, spec, handler) {
  server.registerTool(name, spec, async (args) => {
    try {
      return ok(await handler(args ?? {}));
    } catch (err) {
      return fail(err);
    }
  });
}

// Schreibende Tools fallen im Nur-Lese-Modus (ETSY_READ_ONLY=1) einfach weg
function writeTool(name, spec, handler) {
  if (config.readOnly) return;
  tool(name, { ...spec, annotations: { readOnlyHint: false, ...spec.annotations } }, handler);
}

const READ = { readOnlyHint: true, openWorldHint: true };

function slimListing(l) {
  return {
    listing_id: l.listing_id,
    title: l.title,
    state: l.state,
    price: money(l.price),
    currency: l.price?.currency_code,
    quantity: l.quantity,
    views: l.views,
    favorites: l.num_favorers,
    tags: l.tags,
    section_id: l.shop_section_id,
    url: l.url,
    ...(l.images && { images: l.images.map((i) => ({ id: i.listing_image_id, rank: i.rank, url: i.url_570xN, alt: i.alt_text })) }),
  };
}

function slimReceipt(r) {
  return {
    receipt_id: r.receipt_id,
    created: new Date(r.created_timestamp * 1000).toISOString(),
    status: r.status,
    is_paid: r.is_paid,
    is_shipped: r.is_shipped,
    buyer: r.name,
    country: r.country_iso,
    total: money(r.grandtotal),
    currency: r.grandtotal?.currency_code,
    message_from_buyer: r.message_from_buyer || undefined,
    items: (r.transactions ?? []).map((t) => ({ listing_id: t.listing_id, title: t.title, quantity: t.quantity, price: money(t.price), sku: t.sku })),
  };
}

// ---------- Lesen ----------

tool("etsy_shop_info", {
  title: "Shop-Übersicht",
  description: "Grunddaten des Etsy-Shops sunnozyCH: Titel, Ankündigung, aktive Artikel, Verkäufe, Bewertungsschnitt, Links.",
  annotations: READ,
}, async () => {
  const s = await etsy.request("GET", `/shops/${await etsy.shopId()}`);
  return {
    shop_id: s.shop_id, name: s.shop_name, title: s.title, announcement: s.announcement, sale_message: s.sale_message,
    currency: s.currency_code, active_listings: s.listing_active_count, sales: s.transaction_sold_count,
    review_average: s.review_average, review_count: s.review_count, favorites: s.num_favorers,
    is_vacation: s.is_vacation, url: s.url,
  };
});

tool("etsy_list_listings", {
  title: "Artikel auflisten",
  description: "Listet die Etsy-Artikel des Shops mit Preis, Menge, Aufrufen, Favoriten und Tags.",
  inputSchema: {
    state: z.enum(["active", "inactive", "sold_out", "draft", "expired"]).default("active"),
    limit: z.number().int().min(1).max(100).default(25),
    offset: z.number().int().min(0).default(0),
    include_images: z.boolean().default(false).describe("Bild-URLs mitliefern"),
  },
  annotations: READ,
}, async ({ state, limit, offset, include_images }) => {
  const res = await etsy.request("GET", `/shops/${await etsy.shopId()}/listings`, {
    query: { state, limit, offset, includes: include_images ? "Images" : undefined },
  });
  return { count: res.count, offset, listings: res.results.map(slimListing) };
});

tool("etsy_get_listing", {
  title: "Artikel im Detail",
  description: "Ein Etsy-Artikel komplett: Beschreibung, Tags, Materialien, Bilder, Übersetzungen und Varianten/Preise.",
  inputSchema: { listing_id: z.number().int() },
  annotations: READ,
}, async ({ listing_id }) => {
  const [l, inv] = await Promise.all([
    etsy.request("GET", `/listings/${listing_id}`, { query: { includes: "Images,Translations" } }),
    etsy.request("GET", `/listings/${listing_id}/inventory`),
  ]);
  return {
    ...slimListing(l),
    description: l.description,
    materials: l.materials,
    who_made: l.who_made, when_made: l.when_made, is_supply: l.is_supply,
    taxonomy_id: l.taxonomy_id, shipping_profile_id: l.shipping_profile_id, return_policy_id: l.return_policy_id,
    should_auto_renew: l.should_auto_renew,
    translations: l.translations,
    variants: inv.products.filter((p) => !p.is_deleted).map((p) => ({
      sku: p.sku,
      properties: p.property_values.map((v) => `${v.property_name}: ${v.values.join("/")}`),
      offerings: p.offerings.filter((o) => !o.is_deleted).map((o) => ({ price: money(o.price), quantity: o.quantity, enabled: o.is_enabled })),
    })),
  };
});

tool("etsy_list_orders", {
  title: "Bestellungen",
  description: "Etsy-Bestellungen (Receipts), neueste zuerst. Z.B. was_shipped=false für offene Sendungen.",
  inputSchema: {
    was_paid: z.boolean().optional(),
    was_shipped: z.boolean().optional(),
    days: z.number().int().min(1).optional().describe("Nur Bestellungen der letzten N Tage"),
    limit: z.number().int().min(1).max(100).default(25),
    offset: z.number().int().min(0).default(0),
  },
  annotations: READ,
}, async ({ was_paid, was_shipped, days, limit, offset }) => {
  const res = await etsy.request("GET", `/shops/${await etsy.shopId()}/receipts`, {
    query: {
      was_paid, was_shipped, limit, offset, sort_on: "created", sort_order: "desc",
      min_created: days ? Math.floor(Date.now() / 1000) - days * 86400 : undefined,
    },
  });
  return { count: res.count, orders: res.results.map(slimReceipt) };
});

tool("etsy_get_order", {
  title: "Bestellung im Detail",
  description: "Eine Etsy-Bestellung mit Lieferadresse, Positionen und Versandstatus.",
  inputSchema: { receipt_id: z.number().int() },
  annotations: READ,
}, async ({ receipt_id }) => {
  const r = await etsy.request("GET", `/shops/${await etsy.shopId()}/receipts/${receipt_id}`);
  return {
    ...slimReceipt(r),
    address: r.formatted_address,
    shipments: r.shipments,
    gift: r.is_gift ? { message: r.gift_message } : undefined,
  };
});

tool("etsy_list_reviews", {
  title: "Bewertungen",
  description: "Bewertungen des Etsy-Shops (Sterne, Text, Artikel), neueste zuerst.",
  inputSchema: {
    limit: z.number().int().min(1).max(100).default(25),
    offset: z.number().int().min(0).default(0),
  },
  annotations: READ,
}, async ({ limit, offset }) => {
  const res = await etsy.request("GET", `/shops/${await etsy.shopId()}/reviews`, { query: { limit, offset } });
  return {
    count: res.count,
    reviews: res.results.map((r) => ({
      rating: r.rating, review: r.review, language: r.language, listing_id: r.listing_id,
      created: new Date(r.created_timestamp * 1000).toISOString().slice(0, 10),
    })),
  };
});

tool("etsy_shop_setup", {
  title: "Shop-Einstellungen",
  description: "IDs, die man für neue Artikel braucht: Shop-Kategorien (Sections), Versandprofile, Rückgaberichtlinien, Bearbeitungszeiten.",
  annotations: READ,
}, async () => {
  const id = await etsy.shopId();
  const [sections, shipping, returns, readiness] = await Promise.all([
    etsy.request("GET", `/shops/${id}/sections`),
    etsy.request("GET", `/shops/${id}/shipping-profiles`),
    etsy.request("GET", `/shops/${id}/policies/return`),
    etsy.request("GET", `/shops/${id}/readiness-state-definitions`),
  ]);
  return {
    sections: sections.results.map((s) => ({ id: s.shop_section_id, title: s.title, active_listings: s.active_listing_count })),
    shipping_profiles: shipping.results.map((p) => ({ id: p.shipping_profile_id, title: p.title, origin: p.origin_country_iso })),
    return_policies: returns.results.map((p) => ({ id: p.return_policy_id, accepts_returns: p.accepts_returns, return_deadline: p.return_deadline })),
    readiness_states: readiness.results.map((r) => ({ id: r.readiness_state_id, state: r.readiness_state, days: r.processing_days_display_label ?? `${r.min_processing_days}–${r.max_processing_days}` })),
  };
});

let taxonomyCache;
tool("etsy_find_category", {
  title: "Kategorie suchen",
  description: "Sucht Etsy-Kategorien (taxonomy_id) per Stichwort, z.B. «baby clothing», «bodysuits», «gift sets». Englische Begriffe verwenden.",
  inputSchema: { query: z.string().min(2) },
  annotations: READ,
}, async ({ query }) => {
  if (!taxonomyCache) {
    const res = await etsy.request("GET", "/seller-taxonomy/nodes", { auth: false });
    taxonomyCache = [];
    const walk = (nodes, path) => {
      for (const n of nodes) {
        const full = [...path, n.name];
        taxonomyCache.push({ taxonomy_id: n.id, path: full.join(" › "), leaf: !n.children?.length });
        if (n.children?.length) walk(n.children, full);
      }
    };
    walk(res.results, []);
  }
  const words = query.toLowerCase().split(/\s+/);
  return taxonomyCache.filter((n) => words.every((w) => n.path.toLowerCase().includes(w))).slice(0, 30);
});

// ---------- Schreiben ----------

const listingFields = {
  title: z.string().max(140).optional(),
  description: z.string().optional(),
  tags: z.array(z.string().max(20)).max(13).optional().describe("Max. 13 Tags à 20 Zeichen; ersetzt alle bisherigen Tags"),
  materials: z.array(z.string()).optional(),
  shop_section_id: z.number().int().optional(),
  shipping_profile_id: z.number().int().optional(),
  return_policy_id: z.number().int().optional(),
  taxonomy_id: z.number().int().optional(),
  should_auto_renew: z.boolean().optional(),
};

writeTool("etsy_update_listing", {
  title: "Artikel bearbeiten",
  description: "Ändert Titel, Beschreibung, Tags, Materialien, Kategorie oder Status eines Etsy-Artikels. Nur übergebene Felder werden geändert. Preis/Menge → etsy_set_price_quantity.",
  inputSchema: {
    listing_id: z.number().int(),
    ...listingFields,
    state: z.enum(["active", "inactive"]).optional().describe("active veröffentlicht (Entwurf braucht ein Bild), inactive pausiert"),
  },
  annotations: { idempotentHint: true },
}, async ({ listing_id, ...fields }) => {
  if (!Object.values(fields).some((v) => v !== undefined)) throw new Error("Keine Felder zum Ändern angegeben.");
  const l = await etsy.request("PATCH", `/shops/${await etsy.shopId()}/listings/${listing_id}`, { form: fields });
  return slimListing(l);
});

writeTool("etsy_set_price_quantity", {
  title: "Preis / Menge setzen",
  description: "Setzt Preis und/oder Lagermenge eines Etsy-Artikels – für alle Varianten oder nur die mit der angegebenen SKU.",
  inputSchema: {
    listing_id: z.number().int(),
    price: z.number().positive().optional().describe("In Shop-Währung, z.B. 49.9"),
    quantity: z.number().int().min(0).max(999).optional(),
    sku: z.string().optional().describe("Nur diese Variante ändern"),
  },
  annotations: { idempotentHint: true },
}, async ({ listing_id, price, quantity, sku }) => {
  if (price === undefined && quantity === undefined) throw new Error("price oder quantity angeben.");
  const inv = await etsy.request("GET", `/listings/${listing_id}/inventory`);
  const updated = await etsy.request("PUT", `/listings/${listing_id}/inventory`, {
    json: buildInventoryUpdate(inv, { price, quantity, sku }),
  });
  return updated.products.map((p) => ({
    sku: p.sku,
    offerings: p.offerings.map((o) => ({ price: money(o.price), quantity: o.quantity })),
  }));
});

writeTool("etsy_create_draft_listing", {
  title: "Neuer Artikel (Entwurf)",
  description: "Legt einen neuen Etsy-Artikel als Entwurf an (nicht öffentlich). Danach Bilder mit etsy_upload_image hochladen und mit etsy_update_listing state=active veröffentlichen. taxonomy_id über etsy_find_category, Profile über etsy_shop_setup.",
  inputSchema: {
    title: z.string().max(140),
    description: z.string(),
    price: z.number().positive(),
    quantity: z.number().int().min(1).max(999),
    taxonomy_id: z.number().int(),
    who_made: z.enum(["i_did", "someone_else", "collective"]).default("someone_else"),
    when_made: z.string().default("made_to_order").describe("made_to_order, 2020_2026, 2010_2019, …"),
    is_supply: z.boolean().default(false),
    readiness_state_id: z.number().int().optional().describe("Bearbeitungszeit aus etsy_shop_setup (Pflicht bei physischen Artikeln)"),
    ...listingFields,
  },
}, async (fields) => {
  const l = await etsy.request("POST", `/shops/${await etsy.shopId()}/listings`, { form: { type: "physical", ...fields } });
  return slimListing(l);
});

writeTool("etsy_upload_image", {
  title: "Bild hochladen",
  description: "Lädt ein Produktbild (lokaler Pfad oder URL, JPG/PNG/GIF) zu einem Etsy-Artikel hoch. rank=1 macht es zum Hauptbild.",
  inputSchema: {
    listing_id: z.number().int(),
    file_path: z.string().optional(),
    image_url: z.string().url().optional(),
    rank: z.number().int().min(1).max(20).optional(),
    alt_text: z.string().max(500).optional(),
    overwrite: z.boolean().default(false).describe("Bestehendes Bild auf diesem Rang ersetzen"),
  },
}, async ({ listing_id, file_path, image_url, rank, alt_text, overwrite }) => {
  let bytes, name;
  if (file_path) {
    bytes = await readFile(file_path);
    name = basename(file_path);
  } else if (image_url) {
    const res = await fetch(image_url);
    if (!res.ok) throw new Error(`Bild nicht ladbar (${res.status}): ${image_url}`);
    bytes = Buffer.from(await res.arrayBuffer());
    name = basename(new URL(image_url).pathname) || "bild.jpg";
  } else {
    throw new Error("file_path oder image_url angeben.");
  }
  const form = new FormData();
  form.append("image", new Blob([bytes]), name);
  if (rank) form.append("rank", String(rank));
  if (alt_text) form.append("alt_text", alt_text);
  if (overwrite) form.append("overwrite", "true");
  const img = await etsy.request("POST", `/shops/${await etsy.shopId()}/listings/${listing_id}/images`, { multipart: form });
  return { listing_image_id: img.listing_image_id, rank: img.rank, url: img.url_fullxfull };
});

writeTool("etsy_set_translation", {
  title: "Übersetzung setzen",
  description: "Setzt Titel, Beschreibung und Tags eines Etsy-Artikels in einer weiteren Sprache (de, en, fr, it, es, nl, …). Legt sie an oder überschreibt sie.",
  inputSchema: {
    listing_id: z.number().int(),
    language: z.string().length(2),
    title: z.string().max(140),
    description: z.string(),
    tags: z.array(z.string().max(20)).max(13).optional(),
  },
  annotations: { idempotentHint: true },
}, async ({ listing_id, language, ...form }) => {
  const path = `/shops/${await etsy.shopId()}/listings/${listing_id}/translations/${language}`;
  try {
    return await etsy.request("PUT", path, { form });
  } catch (err) {
    if (!/→ 404/.test(err.message)) throw err;
    return etsy.request("POST", path, { form });
  }
});

writeTool("etsy_mark_shipped", {
  title: "Als versendet markieren",
  description: "Markiert eine Etsy-Bestellung als versendet und schickt der Kundin die Sendungsnummer (z.B. Schweizerische Post).",
  inputSchema: {
    receipt_id: z.number().int(),
    tracking_code: z.string().optional(),
    carrier_name: z.string().optional().describe("z.B. swiss-post"),
    note_to_buyer: z.string().optional(),
  },
}, async ({ receipt_id, ...json }) => {
  const r = await etsy.request("POST", `/shops/${await etsy.shopId()}/receipts/${receipt_id}/tracking`, { json });
  return slimReceipt(r);
});

writeTool("etsy_update_shop", {
  title: "Shop-Texte ändern",
  description: "Ändert Shop-Titel, Ankündigung (Banner-Text) oder die Nachricht an Käufer:innen nach dem Kauf.",
  inputSchema: {
    title: z.string().max(55).optional(),
    announcement: z.string().optional(),
    sale_message: z.string().optional(),
  },
  annotations: { idempotentHint: true },
}, async (form) => {
  const s = await etsy.request("PUT", `/shops/${await etsy.shopId()}`, { form });
  return { title: s.title, announcement: s.announcement, sale_message: s.sale_message };
});

await server.connect(new StdioServerTransport());
