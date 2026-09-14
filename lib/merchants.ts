import { MerchantConfig } from "@/types/merchant";
import { MERCHANTS_REGISTRY } from "@/data/merchants/registry";

export function getMerchantById(id: string): MerchantConfig {
  const normalizedId = id.toLowerCase().trim();
  if (MERCHANTS_REGISTRY[normalizedId]) {
    return MERCHANTS_REGISTRY[normalizedId];
  }
  return MERCHANTS_REGISTRY["demo"];
}

export function getAllMerchants(): MerchantConfig[] {
  return Object.values(MERCHANTS_REGISTRY);
}

export function listMerchants(): { id: string; name: string; tagline: string }[] {
  return Object.values(MERCHANTS_REGISTRY).map((m) => ({
    id: m.storeInfo.id,
    name: m.storeInfo.name,
    tagline: m.storeInfo.tagline,
  }));
}
