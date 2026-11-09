import { MerchantConfig } from "@/types/merchant";
import { MERCHANTS_REGISTRY } from "@/data/merchants/registry";
import VERIFIED_MENUS from "@/data/verified-menus.json";
import REMOVED_PLACES from "@/data/removed-places.json";

/*
 * SERVER-ONLY: this module imports every merchant JSON (~27 MB). Import it
 * from server components and API routes only. Client components should
 * receive a merchant as a prop, and use "@/lib/phone" for isValidPhone.
 */
export { isValidPhone } from "./phone";

/**
 * Places we could not find any trace of online (or that have closed) are listed in
 * data/removed-places.json with the reason. They are hidden from the directory and their
 * pages return 404. Delete an entry from that file to restore a place.
 */
export function isRemovedPlace(id: string): boolean {
  return Object.prototype.hasOwnProperty.call(REMOVED_PLACES, (id || "").toLowerCase().trim());
}

/** Returns the registry key for an ID/slug/name, or null if nothing matches. */
function resolveMerchantKey(id: string): string | null {
  if (!id) return null;
  let decoded = id;
  try {
    decoded = decodeURIComponent(id);
  } catch {
    // malformed %-escape → use the raw id
  }
  const normalizedId = decoded.toLowerCase().trim();
  if (isRemovedPlace(normalizedId)) return null;

  // Direct access for /demo or /demo-market
  if (normalizedId === "demo" || normalizedId === "demo-market" || normalizedId === "demomarket" || normalizedId === "elsol") {
    return MERCHANTS_REGISTRY["demo"] ? "demo" : MERCHANTS_REGISTRY["elsol"] ? "elsol" : null;
  }

  if (MERCHANTS_REGISTRY[normalizedId]) {
    return normalizedId;
  }

  // 1. Match ignoring hyphens/underscores/spaces (e.g. "thefarmkitchenct" -> "the-farm-kitchen-ct")
  const strippedId = normalizedId.replace(/[-_\s]/g, "");
  const keys = Object.keys(MERCHANTS_REGISTRY).filter((k) => !isRemovedPlace(k));
  const matchedKey = keys.find((k) => k.replace(/[-_\s]/g, "") === strippedId);
  if (matchedKey) return matchedKey;

  // 2. Match by normalized business name
  const matchedByName = keys.find((k) => {
    const name = MERCHANTS_REGISTRY[k]?.storeInfo?.name || "";
    return name.toLowerCase().replace(/[^a-z0-9]/g, "") === strippedId;
  });
  if (matchedByName) return matchedByName;

  // 3. Match prefix / contains (e.g. "thefarmkitchen" -> "the-farm-kitchen-ct")
  // (require 4+ chars so short junk like "/a" doesn't match a random place)
  if (strippedId.length >= 4) {
    const partialMatch = keys.find((k) => {
      const cleanK = k.replace(/[-_\s]/g, "");
      return cleanK.startsWith(strippedId) || strippedId.startsWith(cleanK);
    });
    if (partialMatch) return partialMatch;
  }

  return null;
}

export function hasMerchant(id: string): boolean {
  return resolveMerchantKey(id) !== null;
}

/** Menus listed in data/verified-menus.json were taken from the place's real menu. */
export function isMenuVerified(key: string): boolean {
  return Object.prototype.hasOwnProperty.call(VERIFIED_MENUS, key);
}

export function getMerchantById(id: string): MerchantConfig {
  const key = resolveMerchantKey(id);
  if (!key || !MERCHANTS_REGISTRY[key]) return MERCHANTS_REGISTRY["demo"];
  return { ...MERCHANTS_REGISTRY[key], menuVerified: isMenuVerified(key) };
}

export function getAllMerchants(): MerchantConfig[] {
  // Some places are saved under two URL slugs (e.g. cake-box + the-cake-box) so
  // both links work; list each place only once in the directory.
  const seen = new Set<string>();
  return Object.values(MERCHANTS_REGISTRY).filter((m) => {
    const id = (m.storeInfo?.id || "").toLowerCase();
    const name = (m.storeInfo?.name || "").toLowerCase();
    // Exclude internal demo test markets from public directory
    if (id === "demo" || id === "elsol" || name.includes("demo market")) {
      return false;
    }
    if (isRemovedPlace(id)) return false;
    const placeKey = `${name.trim()}|${(m.storeInfo?.address || "").toLowerCase().trim()}`;
    if (seen.has(id) || seen.has(placeKey)) return false;
    seen.add(id);
    seen.add(placeKey);
    return true;
  });
}

export function listMerchants(): { id: string; name: string; tagline: string }[] {
  return getAllMerchants().map((m) => ({
    id: m.storeInfo.id,
    name: m.storeInfo.name,
    tagline: m.storeInfo.tagline,
  }));
}

