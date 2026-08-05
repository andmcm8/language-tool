import { MerchantConfig } from "@/types/merchant";
import elsolConfig from "@/data/merchants/elsol.json";
import cloverConfig from "@/data/merchants/clover-pharmacy.json";
import repairConfig from "@/data/merchants/stamford-repairs.json";

const MERCHANTS_MAP: Record<string, MerchantConfig> = {
  elsol: elsolConfig as unknown as MerchantConfig,
  "clover-pharmacy": cloverConfig as unknown as MerchantConfig,
  "stamford-repairs": repairConfig as unknown as MerchantConfig,
};

export function getMerchantById(id: string): MerchantConfig {
  const normalizedId = id.toLowerCase().trim();
  if (MERCHANTS_MAP[normalizedId]) {
    return MERCHANTS_MAP[normalizedId];
  }
  // Default fallback if merchant not found
  return elsolConfig as unknown as MerchantConfig;
}

export function getAllMerchants(): MerchantConfig[] {
  return Object.values(MERCHANTS_MAP);
}

export function listMerchants(): { id: string; name: string; tagline: string }[] {
  return Object.values(MERCHANTS_MAP).map((m) => ({
    id: m.storeInfo.id,
    name: m.storeInfo.name,
    tagline: m.storeInfo.tagline,
  }));
}
