/** Client-safe helpers for presenting a place. */

/** "123 Main St, Tolland, CT 06084" -> "Tolland, CT" */
export function townFromAddress(address: string | undefined): string {
  // No commas: "225 Merrow Rd Tolland CT 06084"
  const flat = (address || "").trim();
  if (flat && !flat.includes(",")) {
    const m = flat.match(/^.*\b(?:Rd|Road|St|Street|Ave|Avenue|Blvd|Boulevard|Hwy|Highway|Pike|Turnpike|Tpke|Ln|Lane|Dr|Drive|Way|Pl|Place|Ct|Court|Sq|Square|Trl|Trail|Pkwy|Parkway|Route \d+|Rt\.? ?\d+)\b\.?\s+(.+?)\s+([A-Z]{2})\b/);
    if (m) return `${m[1]}, ${m[2]}`;
  }
  const parts = (address || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (parts.length >= 3) {
    const state = (parts[parts.length - 1].match(/[A-Z]{2}/) || ["CT"])[0];
    return `${parts[parts.length - 2]}, ${state}`;
  }
  if (parts.length === 2) {
    const st = parts[1].match(/^([A-Z]{2})\b/);
    if (st) return `${parts[0]}, ${st[1]}`; // "Cheshire, CT"
    return parts[1].replace(/\s*\d{5}(-\d{4})?$/, "");
  }
  return "";
}

/** Taglines are stored as "English | Español"; pick one side. */
export function taglineFor(tagline: string | undefined, lang: "en" | "es"): string {
  const parts = (tagline || "").split("|").map((s) => s.trim());
  if (parts.length > 1) return (lang === "es" ? parts[1] : parts[0]) || parts[0];
  return parts[0] || "";
}

const SWATCHES: [string, string][] = [
  ["#1F7BFF", "#0847D6"],
  ["#14B8A6", "#0E7C86"],
  ["#8B5CF6", "#5B33C9"],
  ["#F59E0B", "#D9480F"],
  ["#EC4899", "#BE185D"],
  ["#06B6D4", "#0369A1"],
  ["#22C55E", "#15803D"],
  ["#6366F1", "#3730A3"],
];

/** Stable gradient per place name, for the monogram avatar. */
export function swatchFor(name: string): string {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
  const [a, b] = SWATCHES[h % SWATCHES.length];
  return `linear-gradient(135deg, ${a}, ${b})`;
}

export function initialsOf(name: string): string {
  const words = name.replace(/[^A-Za-z&' ]/g, " ").split(/\s+/).filter((w) => w && !/^(the|of|and|&)$/i.test(w));
  const first = words[0]?.[0] || name[0] || "?";
  const second = words.length > 1 ? words[1][0] : "";
  return (first + second).toUpperCase();
}
