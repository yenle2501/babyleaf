import { money } from "./etsy.js";

/**
 * Baut aus der GET-Antwort von getListingInventory den Body für updateListingInventory.
 * Etsy verlangt beim PUT immer *alle* Produkte; read-only-Felder (product_id, offering_id,
 * is_deleted, scale_name) müssen weg und der Preis als Zahl statt Money-Objekt kommen.
 * Mit `price`/`quantity` werden alle Angebote (oder nur die mit passender `sku`) angepasst.
 */
export function buildInventoryUpdate(inventory, { price, quantity, sku } = {}) {
  let matched = 0;
  const products = inventory.products
    .filter((p) => !p.is_deleted)
    .map((p) => {
      const hit = sku === undefined || p.sku === sku;
      if (hit) matched++;
      return {
        sku: p.sku ?? "",
        property_values: (p.property_values ?? []).map((v) => ({
          property_id: v.property_id,
          property_name: v.property_name,
          scale_id: v.scale_id ?? null,
          value_ids: v.value_ids,
          values: v.values,
        })),
        offerings: p.offerings
          .filter((o) => !o.is_deleted)
          .map((o) => ({
            price: hit && price !== undefined ? price : money(o.price),
            quantity: hit && quantity !== undefined ? quantity : o.quantity,
            is_enabled: o.is_enabled,
            readiness_state_id: o.readiness_state_id,
          })),
      };
    });
  if (sku !== undefined && matched === 0) {
    throw new Error(`Keine Variante mit SKU «${sku}» gefunden.`);
  }
  const body = { products };
  for (const key of ["price_on_property", "quantity_on_property", "sku_on_property", "readiness_state_on_property"]) {
    if (inventory[key]?.length) body[key] = inventory[key];
  }
  return body;
}
