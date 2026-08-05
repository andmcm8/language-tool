"use client";

import React, { useState, useMemo } from "react";
import { MerchantConfig, Product } from "@/types/merchant";
import {
  Search,
  AlertTriangle,
  ChevronRight,
  X,
  Tag,
  CheckCircle2,
  LayoutGrid,
  List,
  Phone,
  ShoppingBag,
  Wrench,
  Pill,
  Syringe,
  Activity,
  Utensils,
  Cake,
  CreditCard,
  Smartphone,
  Laptop,
  Unlock
} from "lucide-react";

interface CatalogTabProps {
  merchant: MerchantConfig;
  lang: "es" | "en";
}

export default function CatalogTab({ merchant, lang }: CatalogTabProps) {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedItem, setSelectedItem] = useState<Product | null>(null);
  const [viewMode, setViewMode] = useState<"list" | "grid">("list");

  const filteredProducts = useMemo(() => {
    return merchant.products.filter((item) => {
      const matchesCategory = selectedCategory === "all" || item.categoryId === selectedCategory;
      const query = searchQuery.toLowerCase().trim();
      const matchesSearch =
        !query ||
        item.nameEs.toLowerCase().includes(query) ||
        item.nameEn.toLowerCase().includes(query) ||
        item.descriptionEs.toLowerCase().includes(query) ||
        item.descriptionEn.toLowerCase().includes(query);
      return matchesCategory && matchesSearch;
    });
  }, [merchant.products, selectedCategory, searchQuery]);

  const getCategoryIcon = (categoryId: string, itemBadge?: string) => {
    const key = categoryId.toLowerCase();
    if (key.includes("deli") || key.includes("food") || key.includes("utensil"))
      return <Utensils className="w-5 h-5 text-amber-600" />;
    if (key.includes("bake") || key.includes("pan"))
      return <Cake className="w-5 h-5 text-orange-600" />;
    if (key.includes("prescription") || key.includes("pill") || key.includes("med"))
      return <Pill className="w-5 h-5 text-emerald-600" />;
    if (key.includes("vaccine") || key.includes("immun"))
      return <Syringe className="w-5 h-5 text-teal-600" />;
    if (key.includes("well") || key.includes("health") || key.includes("screen"))
      return <Activity className="w-5 h-5 text-blue-600" />;
    if (key.includes("phone") || key.includes("smart"))
      return <Smartphone className="w-5 h-5 text-violet-600" />;
    if (key.includes("laptop") || key.includes("mac"))
      return <Laptop className="w-5 h-5 text-indigo-600" />;
    if (key.includes("unlock"))
      return <Unlock className="w-5 h-5 text-rose-600" />;
    if (key.includes("repair") || key.includes("wrench"))
      return <Wrench className="w-5 h-5 text-purple-600" />;
    if (key.includes("service") || key.includes("card"))
      return <CreditCard className="w-5 h-5 text-blue-600" />;

    return <ShoppingBag className="w-5 h-5 text-primary" />;
  };

  const handleAction = (item: Product) => {
    if (item.ctaType === "phone") {
      window.open(`tel:${merchant.storeInfo.phone}`, "_self");
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-4 pb-24 space-y-3">
      {/* Search Header & View Mode Switcher */}
      <div className="bg-surface p-3 rounded-2xl border border-secondary-fixed/50 shadow-2xs space-y-2">
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-on-surface-variant absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={
                lang === "es"
                  ? `Buscar en ${merchant.storeInfo.name}...`
                  : `Search ${merchant.storeInfo.name}...`
              }
              className="w-full pl-9 pr-8 py-2 bg-surface-container-lowest border border-outline-variant/40 rounded-xl text-xs text-on-surface placeholder:text-on-surface-variant/60 focus:outline-hidden focus:border-primary transition-all"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 p-1 text-on-surface-variant"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* List vs Grid Switcher */}
          <div className="flex items-center bg-surface-container p-1 rounded-xl border border-outline-variant/30">
            <button
              onClick={() => setViewMode("list")}
              className={`p-1.5 rounded-lg transition-all ${
                viewMode === "list" ? "bg-primary text-white shadow-2xs" : "text-on-surface-variant"
              }`}
              title="Lista / List view"
            >
              <List className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode("grid")}
              className={`p-1.5 rounded-lg transition-all ${
                viewMode === "grid" ? "bg-primary text-white shadow-2xs" : "text-on-surface-variant"
              }`}
              title="Cuadrícula / Grid view"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Dynamic Category Selector Pills */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
        {merchant.categories.map((cat) => {
          const isActive = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold shrink-0 transition-all ${
                isActive
                  ? "bg-primary text-white shadow-2xs"
                  : "bg-surface-container text-on-surface-variant hover:bg-surface-container-high"
              }`}
            >
              {lang === "es" ? cat.nameEs : cat.nameEn}
            </button>
          );
        })}
      </div>

      {/* Product & Service Item List */}
      {filteredProducts.length === 0 ? (
        <div className="text-center py-10 bg-surface rounded-2xl border border-dashed border-outline-variant/60 p-4 text-xs text-on-surface-variant">
          {lang === "es" ? "Sin resultados en esta categoría" : "No items found"}
        </div>
      ) : viewMode === "list" ? (
        /* LIST VIEW */
        <div className="grid grid-cols-1 gap-2.5">
          {filteredProducts.map((item) => {
            const hasPhoto = Boolean(item.image);

            return (
              <div
                key={item.id}
                onClick={() => setSelectedItem(item)}
                className={`group p-3.5 rounded-2xl border shadow-2xs hover:shadow-xs transition-all duration-200 cursor-pointer flex gap-3 items-center ${
                  hasPhoto
                    ? "bg-surface border-secondary-fixed/50"
                    : "bg-surface border-secondary-fixed/70 hover:border-primary/40"
                }`}
              >
                {hasPhoto && (
                  <div className="relative w-16 h-16 rounded-xl overflow-hidden bg-surface-container shrink-0">
                    <img
                      src={item.image}
                      alt={item.nameEs}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    {item.badge && (
                      <span className="absolute top-1 left-1 px-1 py-0.2 bg-primary text-white text-[8px] font-bold rounded-xs truncate max-w-[50px]">
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}

                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline justify-between gap-1">
                    <h3 className="font-bold text-xs text-on-surface leading-tight truncate">
                      {lang === "es" ? item.nameEs : item.nameEn}
                    </h3>
                    <span className="font-extrabold text-xs text-primary shrink-0">
                      {item.price}
                    </span>
                  </div>
                  <p className="text-[11px] text-on-surface-variant line-clamp-1 mt-0.5">
                    {lang === "es" ? item.descriptionEs : item.descriptionEn}
                  </p>

                  <div className="flex flex-wrap items-center gap-1 mt-1">
                    {!hasPhoto && item.badge && (
                      <span className="px-1.5 py-0.2 bg-primary/10 text-primary text-[9px] font-bold rounded-md">
                        {item.badge}
                      </span>
                    )}
                    {item.tags && item.tags.map((tag, idx) => (
                      <span key={idx} className="px-1.5 py-0.2 bg-surface-container text-on-surface-variant text-[9px] font-semibold rounded-md">
                        {tag}
                      </span>
                    ))}
                    {item.allergens && item.allergens.length > 0 && (
                      <span className="text-[9px] font-semibold text-amber-600">
                        ⚠️ {item.allergens.join(", ")}
                      </span>
                    )}
                  </div>
                </div>

                <ChevronRight className="w-4 h-4 text-on-surface-variant/40 shrink-0" />
              </div>
            );
          })}
        </div>
      ) : (
        /* GRID VIEW */
        <div className="grid grid-cols-2 gap-2.5">
          {filteredProducts.map((item) => {
            const hasPhoto = Boolean(item.image);

            return (
              <div
                key={item.id}
                onClick={() => setSelectedItem(item)}
                className={`group p-3 rounded-2xl border shadow-2xs hover:shadow-xs transition-all duration-200 cursor-pointer flex flex-col justify-between ${
                  hasPhoto
                    ? "bg-surface border-secondary-fixed/50"
                    : "bg-surface border-secondary-fixed/70 hover:border-primary/40 min-h-[120px]"
                }`}
              >
                <div>
                  {hasPhoto ? (
                    <div className="relative w-full aspect-square rounded-xl overflow-hidden bg-surface-container mb-2">
                      <img
                        src={item.image}
                        alt={item.nameEs}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      {item.badge && (
                        <span className="absolute top-1 left-1 px-1.5 py-0.5 bg-primary text-white text-[8px] font-bold rounded-md">
                          {item.badge}
                        </span>
                      )}
                    </div>
                  ) : (
                    item.badge && (
                      <div className="mb-1.5">
                        <span className="px-1.5 py-0.5 bg-primary/10 text-primary text-[9px] font-bold rounded-md">
                          {item.badge}
                        </span>
                      </div>
                    )
                  )}

                  <h3 className="font-bold text-xs text-on-surface leading-tight line-clamp-2">
                    {lang === "es" ? item.nameEs : item.nameEn}
                  </h3>

                  {!hasPhoto && (
                    <p className="text-[10px] text-on-surface-variant line-clamp-2 mt-1">
                      {lang === "es" ? item.descriptionEs : item.descriptionEn}
                    </p>
                  )}
                </div>

                <div className="mt-2.5 flex items-center justify-between pt-1 border-t border-outline-variant/20">
                  <span className="font-extrabold text-xs text-primary">{item.price}</span>
                  <ChevronRight className="w-3.5 h-3.5 text-on-surface-variant" />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Item Detail Modal */}
      {selectedItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-surface-container-lowest rounded-3xl max-w-xs w-full p-4 shadow-2xl border border-secondary-fixed relative overflow-hidden animate-in zoom-in-95 duration-200">
            <button
              onClick={() => setSelectedItem(null)}
              className="absolute top-3 right-3 p-1.5 rounded-full bg-surface-container text-on-surface-variant hover:text-on-surface transition-all z-10"
            >
              <X className="w-4 h-4" />
            </button>

            {selectedItem.image ? (
              <div className="relative h-36 -mx-4 -mt-4 mb-3 overflow-hidden">
                <img
                  src={selectedItem.image}
                  alt={selectedItem.nameEs}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />
                <div className="absolute bottom-2 left-3 right-3 flex justify-between items-end">
                  <h3 className="text-sm font-extrabold text-white leading-tight">
                    {lang === "es" ? selectedItem.nameEs : selectedItem.nameEn}
                  </h3>
                  <span className="text-xs font-black text-white bg-primary px-2 py-0.5 rounded-md">
                    {selectedItem.price}
                  </span>
                </div>
              </div>
            ) : (
              <div className="pt-2 mb-3 border-b border-outline-variant/20 pb-3">
                <div className="mb-2">
                  {selectedItem.badge && (
                    <span className="px-1.5 py-0.5 bg-primary/10 text-primary text-[9px] font-bold rounded-md uppercase">
                      {selectedItem.badge}
                    </span>
                  )}
                  <h3 className="text-sm font-extrabold text-on-surface leading-tight mt-1">
                    {lang === "es" ? selectedItem.nameEs : selectedItem.nameEn}
                  </h3>
                </div>
                <div className="inline-block text-xs font-black text-primary bg-secondary-fixed px-2.5 py-1 rounded-xl">
                  {selectedItem.price}
                </div>
              </div>
            )}

            <p className="text-xs text-on-surface-variant leading-relaxed">
              {lang === "es" ? selectedItem.descriptionEs : selectedItem.descriptionEn}
            </p>

            {selectedItem.tags && selectedItem.tags.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1">
                {selectedItem.tags.map((tag, idx) => (
                  <span key={idx} className="px-2 py-0.5 bg-surface-container text-on-surface text-[10px] font-semibold rounded-md">
                    ✓ {tag}
                  </span>
                ))}
              </div>
            )}

            {selectedItem.allergens && selectedItem.allergens.length > 0 && (
              <div className="mt-2.5 p-2 bg-amber-50 rounded-xl border border-amber-200 text-[10px] text-amber-900 font-semibold">
                ⚠️ {lang === "es" ? "Alérgenos: " : "Allergens: "}
                {selectedItem.allergens.join(", ")}
              </div>
            )}

            <div className="mt-4 pt-3 border-t border-outline-variant/30 flex gap-2">
              {selectedItem.ctaType === "phone" && (
                <button
                  onClick={() => handleAction(selectedItem)}
                  className="flex-1 py-2 bg-primary text-white font-bold text-xs rounded-xl shadow-xs hover:bg-primary-container transition-all flex items-center justify-center gap-1.5"
                >
                  <Phone className="w-4 h-4" />
                  <span>{lang === "es" ? "Llamar Tienda" : "Call Store"}</span>
                </button>
              )}
              {(!selectedItem.ctaType || selectedItem.ctaType === "in_store") && (
                <button
                  onClick={() => setSelectedItem(null)}
                  className="flex-1 py-2 bg-primary text-white font-bold text-xs rounded-xl shadow-xs hover:bg-primary-container transition-all"
                >
                  OK
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
