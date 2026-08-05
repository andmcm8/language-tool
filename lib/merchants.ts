import { MerchantConfig } from "@/types/merchant";
import demoConfig from "@/data/merchants/demo.json";

const MERCHANTS_MAP: Record<string, MerchantConfig> = {
  demo: demoConfig as unknown as MerchantConfig,
  elsol: demoConfig as unknown as MerchantConfig,
};

export function getMerchantById(id: string): MerchantConfig {
  const normalizedId = id.toLowerCase().trim();
  if (MERCHANTS_MAP[normalizedId]) {
    return MERCHANTS_MAP[normalizedId];
  }
  return demoConfig as unknown as MerchantConfig;
}

export function getAllMerchants(): MerchantConfig[] {
  return [demoConfig as unknown as MerchantConfig];
}

export function listMerchants(): { id: string; name: string; tagline: string }[] {
  return [{
    id: demoConfig.storeInfo.id,
    name: demoConfig.storeInfo.name,
    tagline: demoConfig.storeInfo.tagline,
  }];
}
