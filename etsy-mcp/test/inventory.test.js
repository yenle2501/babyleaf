import { test } from "node:test";
import assert from "node:assert/strict";
import { buildInventoryUpdate } from "../src/inventory.js";

const inventory = {
  price_on_property: [513],
  quantity_on_property: [],
  products: [
    {
      product_id: 1, sku: "SET-50", is_deleted: false,
      property_values: [{ property_id: 513, property_name: "Grösse", scale_id: 1, scale_name: "EU", value_ids: [1], values: ["50"] }],
      offerings: [{ offering_id: 11, quantity: 3, is_enabled: true, is_deleted: false, readiness_state_id: 7, price: { amount: 4990, divisor: 100, currency_code: "CHF" } }],
    },
    {
      product_id: 2, sku: "SET-56", is_deleted: false,
      property_values: [{ property_id: 513, property_name: "Grösse", scale_id: 1, value_ids: [2], values: ["56"] }],
      offerings: [{ offering_id: 12, quantity: 5, is_enabled: true, is_deleted: false, readiness_state_id: 7, price: { amount: 5490, divisor: 100, currency_code: "CHF" } }],
    },
    { product_id: 3, sku: "ALT", is_deleted: true, property_values: [], offerings: [] },
  ],
};

test("strips read-only fields and converts money", () => {
  const body = buildInventoryUpdate(inventory);
  assert.equal(body.products.length, 2);
  assert.deepEqual(body.products[0].offerings[0], { price: 49.9, quantity: 3, is_enabled: true, readiness_state_id: 7 });
  assert.equal(body.products[0].product_id, undefined);
  assert.equal(body.products[0].property_values[0].scale_name, undefined);
  assert.deepEqual(body.price_on_property, [513]);
  assert.equal(body.quantity_on_property, undefined);
});

test("updates only the matching sku", () => {
  const body = buildInventoryUpdate(inventory, { quantity: 0, sku: "SET-56" });
  assert.equal(body.products[0].offerings[0].quantity, 3);
  assert.equal(body.products[1].offerings[0].quantity, 0);
});

test("updates all variants without sku", () => {
  const body = buildInventoryUpdate(inventory, { price: 39 });
  assert.deepEqual(body.products.map((p) => p.offerings[0].price), [39, 39]);
});

test("rejects unknown sku", () => {
  assert.throws(() => buildInventoryUpdate(inventory, { price: 1, sku: "NOPE" }), /SKU/);
});
