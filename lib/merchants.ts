import { MerchantConfig } from "@/types/merchant";
import { MERCHANTS_REGISTRY } from "@/data/merchants/registry";

export function getMerchantById(id: string): MerchantConfig {
  if (!id) return MERCHANTS_REGISTRY["demo"];
  const normalizedId = id.toLowerCase().trim();
  if (MERCHANTS_REGISTRY[normalizedId]) {
    return MERCHANTS_REGISTRY[normalizedId];
  }

  // 1. Match ignoring hyphens/underscores/spaces (e.g. "thefarmkitchenct" -> "the-farm-kitchen-ct")
  const strippedId = normalizedId.replace(/[-_\s]/g, "");
  const keys = Object.keys(MERCHANTS_REGISTRY);
  const matchedKey = keys.find((k) => k.replace(/[-_\s]/g, "") === strippedId);
  if (matchedKey && MERCHANTS_REGISTRY[matchedKey]) {
    return MERCHANTS_REGISTRY[matchedKey];
  }

  // 2. Match by normalized business name
  const matchedByName = keys.find((k) => {
    const name = MERCHANTS_REGISTRY[k]?.storeInfo?.name || "";
    return name.toLowerCase().replace(/[^a-z0-9]/g, "") === strippedId;
  });
  if (matchedByName && MERCHANTS_REGISTRY[matchedByName]) {
    return MERCHANTS_REGISTRY[matchedByName];
  }

  // 3. Match prefix / contains (e.g. "thefarmkitchen" -> "the-farm-kitchen-ct")
  const partialMatch = keys.find((k) => {
    const cleanK = k.replace(/[-_\s]/g, "");
    return cleanK.startsWith(strippedId) || strippedId.startsWith(cleanK);
  });
  if (partialMatch && MERCHANTS_REGISTRY[partialMatch]) {
    return MERCHANTS_REGISTRY[partialMatch];
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

export function isValidPhone(phone?: string): boolean {
  if (!phone) return false;
  const digits = phone.replace(/\D/g, "");
  const clean = digits.length === 11 && digits.startsWith("1") ? digits.slice(1) : digits;
  if (clean.length !== 10) return false;
  const areaCode = clean.slice(0, 3);
  // Connecticut area codes (203, 860, 475, 959) or legitimate US toll-free
  const validAreaCodes = ["203", "860", "475", "959", "800", "888", "877", "866", "855"];
  if (!validAreaCodes.includes(areaCode)) return false;
  const exch = clean.slice(3, 6);
  const last = clean.slice(6);
  if (["555", "000", "123", "666"].includes(exch)) return false;
  if (["0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999", "1234", "4321", "7890", "6667"].includes(last)) return false;
  return true;
}

