"use client";

import React, { useState, useMemo, useEffect } from "react";
import { MerchantConfig, Product } from "@/types/merchant";
import { isValidPhone } from "@/lib/phone";
import { Search, X, Phone, LayoutGrid, List, ChevronRight, MapPin, Clock } from "lucide-react";

interface CatalogTabProps {
  merchant: MerchantConfig;
  lang: "es" | "en";
}

/** Some official menus publish no prices; say so instead of rendering an empty badge. */
function priceLabel(price: string | undefined, lang: "es" | "en"): string {
  return price?.trim() ? price : lang === "es" ? "Consultar" : "Ask";
}
const hasPrice = (price?: string) => Boolean(price?.trim());

function PricePill({ price, lang, large = false }: { price?: string; lang: "es" | "en"; large?: boolean }) {
  const real = hasPrice(price);
  return (
    <span
      className={`shrink-0 font-bold tabular-nums rounded-full ${
        large ? "text-base px-4 py-1.5" : "text-[13px] px-3 py-1"
      } ${real ? "bg-primary-fixed text-primary" : "bg-surface-container text-on-surface-variant font-semibold"}`}
    >
      {priceLabel(price, lang)}
    </span>
  );
}

export default function CatalogTab({ merchant, lang }: CatalogTabProps) {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedItem, setSelectedItem] = useState<Product | null>(null);
  const [viewMode, setViewMode] = useState<"list" | "grid">("list");

  // Lock page scroll while the item sheet is open
  useEffect(() => {
    if (!selectedItem) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [selectedItem]);

  const filteredProducts = useMemo(() => {
    const query = searchQuery.toLowerCase().trim();
    return merchant.products.filter((item) => {
      const matchesCategory = selectedCategory === "all" || item.categoryId === selectedCategory;
      const matchesSearch =
        !query ||
        item.nameEs.toLowerCase().includes(query) ||
        item.nameEn.toLowerCase().includes(query) ||
        item.descriptionEs.toLowerCase().includes(query) ||
        item.descriptionEn.toLowerCase().includes(query);
      return matchesCategory && matchesSearch;
    });
  }, [merchant.products, selectedCategory, searchQuery]);

  // Group by section when browsing everything (no search), so long menus stay scannable.
  const groups = useMemo(() => {
    if (selectedCategory !== "all" || searchQuery.trim()) return null;
    const byCat = new Map<string, Product[]>();
    for (const p of filteredProducts) {
      if (!byCat.has(p.categoryId)) byCat.set(p.categoryId, []);
      byCat.get(p.categoryId)!.push(p);
    }
    return merchant.categories
      .filter((c) => c.id !== "all" && byCat.has(c.id))
      .map((c) => ({ cat: c, items: byCat.get(c.id)! }));
  }, [filteredProducts, merchant.categories, selectedCategory, searchQuery]);

  const handleAction = (item: Product) => {
    if (item.ctaType === "phone") window.open(`tel:${merchant.storeInfo.phone}`, "_self");
  };

  const { storeInfo } = merchant;
  const text = (item: Product) => ({
    name: lang === "es" ? item.nameEs : item.nameEn,
    desc: lang === "es" ? item.descriptionEs : item.descriptionEn,
  });

  const renderRow = (item: Product) => {
    const { name, desc } = text(item);
    return (
      <button
        key={item.id}
        onClick={() => setSelectedItem(item)}
        className="group w-full text-left flex items-start gap-3 p-4 bg-white rounded-3xl border border-white shadow-soft hover:shadow-lift active:scale-[0.99] transition-all duration-200"
      >
        {item.image && (
          <img src={item.image} alt="" className="w-[72px] h-[72px] rounded-2xl object-cover shrink-0 bg-surface-container" />
        )}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <h3 className="font-bold text-[15px] leading-snug text-on-surface">{name}</h3>
            <PricePill price={item.price} lang={lang} />
          </div>
          {desc && <p className="mt-1 text-[13px] leading-relaxed text-on-surface-variant line-clamp-2">{desc}</p>}
          {(item.badge || (item.tags && item.tags.length > 0)) && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {item.badge && (
                <span className="px-2 py-0.5 rounded-full bg-primary text-white text-[10px] font-bold uppercase tracking-wide">{item.badge}</span>
              )}
              {item.tags?.map((tag, i) => (
                <span key={i} className="px-2 py-0.5 rounded-full bg-surface-container text-on-surface-variant text-[10px] font-semibold">{tag}</span>
              ))}
            </div>
          )}
        </div>
      </button>
    );
  };

  const renderTile = (item: Product) => {
    const { name, desc } = text(item);
    return (
      <button
        key={item.id}
        onClick={() => setSelectedItem(item)}
        className="text-left p-4 bg-white rounded-3xl border border-white shadow-soft hover:shadow-lift active:scale-[0.99] transition-all duration-200 flex flex-col justify-between min-h-[132px]"
      >
        <div>
          <h3 className="font-bold text-[14px] leading-snug text-on-surface line-clamp-2">{name}</h3>
          {desc && <p className="mt-1 text-xs text-on-surface-variant line-clamp-2 leading-relaxed">{desc}</p>}
        </div>
        <div className="mt-3"><PricePill price={item.price} lang={lang} /></div>
      </button>
    );
  };

  const renderItems = (items: Product[]) =>
    viewMode === "list" ? (
      <div className="flex flex-col gap-2.5">{items.map(renderRow)}</div>
    ) : (
      <div className="grid grid-cols-2 gap-2.5">{items.map(renderTile)}</div>
    );

  return (
    <div className="w-full max-w-md mx-auto px-4 pt-5 space-y-5">
      {/* Intro */}
      <div>
        <h2 className="text-[28px] leading-tight font-extrabold text-on-surface">
          {lang === "es" ? "Nuestro menú" : "Our menu"}
        </h2>
        <p className="mt-1 text-sm text-on-surface-variant font-medium">
          {merchant.products.length} {lang === "es" ? "platillos en español e inglés" : "items in Spanish & English"}
        </p>
        {(isValidPhone(storeInfo.phone) || storeInfo.hours?.monday_friday) && (
          <div className="mt-3 flex flex-wrap gap-2">
            {storeInfo.hours?.monday_friday && !/call/i.test(storeInfo.hours.monday_friday) && (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-white shadow-soft px-3 py-1.5 text-xs font-semibold text-on-surface-variant">
                <Clock className="w-3.5 h-3.5 text-primary" /> {storeInfo.hours.monday_friday}
              </span>
            )}
            {isValidPhone(storeInfo.phone) && (
              <a
                href={`tel:${storeInfo.phone}`}
                className="inline-flex items-center gap-1.5 rounded-full bg-white shadow-soft px-3 py-1.5 text-xs font-semibold text-on-surface-variant hover:text-primary transition-colors"
              >
                <Phone className="w-3.5 h-3.5 text-primary" /> {storeInfo.phone}
              </a>
            )}
          </div>
        )}
      </div>

      {/* Search + view toggle */}
      <div className="flex items-center gap-2.5">
        <div className="relative flex-1">
          <Search className="w-[18px] h-[18px] text-on-surface-variant absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={lang === "es" ? "Buscar en el menú..." : "Search the menu..."}
            className="w-full h-12 pl-11 pr-10 bg-white rounded-full shadow-soft border border-white text-sm font-medium text-on-surface placeholder:text-on-surface-variant/60 focus:outline-none focus:ring-2 focus:ring-primary/40 transition-all"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              aria-label="Clear"
              className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded-full text-on-surface-variant hover:bg-surface-container"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
        <div className="flex items-center p-1 rounded-full bg-white shadow-soft border border-white">
          {([["list", List], ["grid", LayoutGrid]] as const).map(([mode, Icon]) => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              aria-label={mode}
              aria-pressed={viewMode === mode}
              className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                viewMode === mode ? "bg-brand-gradient text-white shadow-brand" : "text-on-surface-variant"
              }`}
            >
              <Icon className="w-[18px] h-[18px]" />
            </button>
          ))}
        </div>
      </div>

      {/* Category chips */}
      <div className="-mx-4 px-4 flex items-center gap-2 overflow-x-auto pb-1">
        {merchant.categories.map((cat) => {
          const isActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`chip shrink-0 ${
                isActive
                  ? "bg-navy text-white shadow-soft"
                  : "bg-white text-on-surface-variant border border-white shadow-soft hover:text-on-surface"
              }`}
            >
              {lang === "es" ? cat.nameEs : cat.nameEn}
            </button>
          );
        })}
      </div>

      {/* Items */}
      {filteredProducts.length === 0 ? (
        <div className="text-center py-14 px-6 bg-white rounded-3xl shadow-soft">
          <div className="mx-auto mb-3 w-12 h-12 rounded-full bg-surface-container flex items-center justify-center">
            <Search className="w-5 h-5 text-on-surface-variant" />
          </div>
          <p className="font-bold text-on-surface">{lang === "es" ? "Sin resultados" : "No matches"}</p>
          <p className="mt-1 text-sm text-on-surface-variant">
            {lang === "es" ? "Prueba con otra palabra o categoría." : "Try another word or category."}
          </p>
        </div>
      ) : groups ? (
        <div className="space-y-7">
          {groups.map(({ cat, items }) => (
            <section key={cat.id} className="space-y-2.5">
              <div className="flex items-baseline justify-between px-1">
                <h3 className="text-lg font-extrabold text-on-surface">{lang === "es" ? cat.nameEs : cat.nameEn}</h3>
                <span className="text-xs font-semibold text-on-surface-variant">{items.length}</span>
              </div>
              {renderItems(items)}
            </section>
          ))}
        </div>
      ) : (
        renderItems(filteredProducts)
      )}

      {/* Item detail bottom sheet */}
      {selectedItem && (
        <div
          className="fixed inset-0 z-50 flex items-end justify-center bg-navy/50 backdrop-blur-sm animate-in fade-in duration-200"
          onClick={() => setSelectedItem(null)}
        >
          <div
            role="dialog"
            aria-modal="true"
            onClick={(e) => e.stopPropagation()}
            className="relative w-full max-w-md bg-white rounded-t-[32px] shadow-float animate-in slide-in-from-bottom duration-300 max-h-[86vh] overflow-y-auto"
            style={{ paddingBottom: "max(24px, env(safe-area-inset-bottom))" }}
          >
            <div className="mx-auto mt-2.5 h-1.5 w-10 rounded-full bg-surface-container-highest" />
            <button
              onClick={() => setSelectedItem(null)}
              aria-label="Close"
              className="absolute top-4 right-4 w-9 h-9 rounded-full bg-surface-container flex items-center justify-center text-on-surface-variant hover:text-on-surface"
            >
              <X className="w-4 h-4" />
            </button>

            {selectedItem.image && (
              <img src={selectedItem.image} alt="" className="mt-4 w-full h-48 object-cover" />
            )}

            <div className="px-6 pt-5">
              {selectedItem.badge && (
                <span className="inline-block mb-2 px-2.5 py-0.5 rounded-full bg-primary text-white text-[10px] font-bold uppercase tracking-wide">
                  {selectedItem.badge}
                </span>
              )}
              <h3 className="text-2xl font-extrabold leading-tight text-on-surface pr-10">{text(selectedItem).name}</h3>

              <div className="mt-3 flex items-center gap-2">
                <PricePill price={selectedItem.price} lang={lang} large />
              </div>

              {/* Both languages, so the diner can show staff exactly what they mean */}
              <div className="mt-5 rounded-3xl bg-surface-container-low p-4 space-y-3">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-wider text-primary">English</p>
                  <p className="mt-0.5 font-bold text-on-surface">{selectedItem.nameEn}</p>
                  {selectedItem.descriptionEn && <p className="text-sm text-on-surface-variant leading-relaxed mt-0.5">{selectedItem.descriptionEn}</p>}
                </div>
                <div className="h-px bg-outline-variant/50" />
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-wider text-primary">Español</p>
                  <p className="mt-0.5 font-bold text-on-surface">{selectedItem.nameEs}</p>
                  {selectedItem.descriptionEs && <p className="text-sm text-on-surface-variant leading-relaxed mt-0.5">{selectedItem.descriptionEs}</p>}
                </div>
              </div>

              {selectedItem.tags && selectedItem.tags.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-1.5">
                  {selectedItem.tags.map((tag, i) => (
                    <span key={i} className="px-3 py-1 rounded-full bg-surface-container text-on-surface text-xs font-semibold">{tag}</span>
                  ))}
                </div>
              )}

              {selectedItem.allergens && selectedItem.allergens.length > 0 && (
                <div className="mt-4 p-3 rounded-2xl bg-amber-50 border border-amber-200 text-xs text-amber-900 font-semibold">
                  {lang === "es" ? "Alérgenos: " : "Allergens: "}
                  {selectedItem.allergens.join(", ")}
                </div>
              )}

              <div className="mt-6">
                {selectedItem.ctaType === "phone" && isValidPhone(storeInfo.phone) ? (
                  <button onClick={() => handleAction(selectedItem)} className="btn-primary w-full h-12 text-sm">
                    <Phone className="w-4 h-4" />
                    {lang === "es" ? "Llamar al local" : "Call the store"}
                  </button>
                ) : (
                  <button onClick={() => setSelectedItem(null)} className="btn-primary w-full h-12 text-sm">
                    {lang === "es" ? "Listo" : "Done"}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
