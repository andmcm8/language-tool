"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { getAllMerchants } from "@/lib/merchants";
import {
  ShoppingBag,
  Pill,
  Wrench,
  Search,
  X,
  MapPin,
  Clock,
  Phone,
  ArrowRight,
  Globe,
  Store,
  ChevronRight,
} from "lucide-react";

const MERCHANT_ICONS: Record<string, any> = {
  elsol: ShoppingBag,
  "clover-pharmacy": Pill,
  "stamford-repairs": Wrench,
};

const MERCHANT_BADGES: Record<string, { en: string; es: string }> = {
  elsol: { en: "Supermarket & Deli", es: "Supermercado y Deli" },
  "clover-pharmacy": { en: "Pharmacy & Wellness", es: "Farmacia y Bienestar" },
  "stamford-repairs": { en: "Tech & Phone Repair", es: "Reparación Celular y Tech" },
};

const CATEGORIES = [
  { id: "all", labelEn: "All Places", labelEs: "Todos los Negocios" },
  { id: "supermarket", labelEn: "Supermarket & Deli", labelEs: "Supermercado y Deli" },
  { id: "pharmacy", labelEn: "Pharmacy", labelEs: "Farmacia" },
  { id: "repair", labelEn: "Tech Repair", labelEs: "Reparación Técnica" },
];

/* ================================================================
   BILINGUAL DICTIONARY FOR HOMEPAGE PORTAL
   ================================================================ */
const DICT = {
  en: {
    portalBadge: "MERCHANT ASSISTANT PORTAL",
    portalTitle: "Language Tool Portal",
    subtitle:
      "Select a merchant below to launch their bilingual AI assistant, camera translation tool, and store directory.",
    searchPlaceholder: "Search places by name, city, service...",
    foundSuffix: "Merchants Found",
    launchBtn: "Launch Merchant Tool",
    noResultsTitle: "No Merchants Match Your Search",
    noResultsDesc:
      'Try searching for "El Sol", "Pharmacy", "Stamford", or click "All Places" above.',
    clearBtn: "Clear Search & Show All",
    monFri: "Mon-Fri",
    footerText: "Language Tool • Multi-Merchant Bilingual Assistant",
  },
  es: {
    portalBadge: "PORTAL DE ASISTENTES COMERCIALES",
    portalTitle: "Portal Language Tool",
    subtitle:
      "Seleccione un negocio a continuación para abrir su asistente de IA bilingüe, herramienta de cámara y directorio.",
    searchPlaceholder: "Buscar negocios por nombre, ciudad, servicio...",
    foundSuffix: "Negocios Encontrados",
    launchBtn: "Abrir Herramienta del Comercio",
    noResultsTitle: "No se encontraron negocios para su búsqueda",
    noResultsDesc:
      'Intente buscar "El Sol", "Farmacia", "Stamford", o presione "Todos los Negocios" arriba.',
    clearBtn: "Borrar Búsqueda y Mostrar Todos",
    monFri: "Lun-Vie",
    footerText: "Language Tool • Portal de Asistentes Comercial Bilingüe",
  },
};

export default function HomePage() {
  const allMerchants = useMemo(() => getAllMerchants(), []);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [lang, setLang] = useState<"en" | "es">("es"); // Default to bilingual Spanish friendly

  const t = DICT[lang];

  /* ---------- Real-Time Filtering Logic ---------- */
  const filteredMerchants = useMemo(() => {
    return allMerchants.filter((m) => {
      const id = m.storeInfo.id.toLowerCase();
      const name = m.storeInfo.name.toLowerCase();
      const tagline = m.storeInfo.tagline.toLowerCase();
      const address = m.storeInfo.address.toLowerCase();
      const badgeEn = (MERCHANT_BADGES[id]?.en || "").toLowerCase();
      const badgeEs = (MERCHANT_BADGES[id]?.es || "").toLowerCase();
      const amenities = (m.storeInfo.amenities || []).join(" ").toLowerCase();

      const q = searchQuery.toLowerCase().trim();
      const matchesSearch =
        !q ||
        name.includes(q) ||
        tagline.includes(q) ||
        address.includes(q) ||
        badgeEn.includes(q) ||
        badgeEs.includes(q) ||
        amenities.includes(q);

      let matchesCategory = true;
      if (selectedCategory === "supermarket") {
        matchesCategory = id === "elsol" || badgeEn.includes("supermarket");
      } else if (selectedCategory === "pharmacy") {
        matchesCategory = id === "clover-pharmacy" || badgeEn.includes("pharmacy");
      } else if (selectedCategory === "repair") {
        matchesCategory = id === "stamford-repairs" || badgeEn.includes("repair");
      }

      return matchesSearch && matchesCategory;
    });
  }, [allMerchants, searchQuery, selectedCategory]);

  return (
    <main className="min-h-screen bg-[#f7f9fb] text-slate-800 font-sans selection:bg-primary selection:text-white pb-20">
      {/* ROYAL BLUE MOBILE-FIRST HEADER */}
      <header className="bg-[#003ec7] text-white shadow-md">
        <div className="max-w-md md:max-w-4xl mx-auto px-4 py-4 space-y-3">
          {/* Top Title & WORKING Interactive EN / ES Language Swapper Toggle */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-white text-[#003ec7] flex items-center justify-center shadow-sm font-black text-xl">
                L
              </div>
              <div>
                <h1 className="font-extrabold text-lg leading-tight text-white tracking-tight">
                  {t.portalTitle}
                </h1>
                <p className="text-[10px] text-blue-100 font-semibold tracking-wide">
                  {t.portalBadge}
                </p>
              </div>
            </div>

            {/* FULLY FUNCTIONAL 1-TAP LANGUAGE TOGGLE BUTTON */}
            <button
              onClick={() => setLang(lang === "es" ? "en" : "es")}
              className="flex items-center gap-1.5 bg-white text-[#003ec7] hover:bg-blue-50 px-3 py-1.5 rounded-full text-xs font-black shadow-md transition-all active:scale-95"
              title="Switch Language / Cambiar Idioma"
            >
              <Globe className="w-3.5 h-3.5 text-[#003ec7]" />
              <span>{lang === "es" ? "🇲🇽 Español" : "🇺🇸 English"}</span>
            </button>
          </div>

          {/* Subtitle Message */}
          <p className="text-xs text-blue-100 font-medium leading-relaxed">
            {t.subtitle}
          </p>

          {/* FUNCTIONAL SEARCH INPUT BAR */}
          <div className="relative pt-1">
            <div className="relative flex items-center">
              <Search className="absolute left-3.5 w-4 h-4 text-slate-400 pointer-events-none" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={t.searchPlaceholder}
                className="w-full pl-10 pr-9 py-2.5 bg-white text-slate-900 rounded-xl text-xs font-medium placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-400 shadow-md"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-3 p-1 rounded-full text-slate-400 hover:text-slate-600"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* CATEGORY FILTER PILLS */}
      <section className="max-w-md md:max-w-4xl mx-auto px-4 pt-3.5 pb-2">
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all shadow-2xs ${
                selectedCategory === cat.id
                  ? "bg-[#003ec7] text-white shadow-sm"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-100"
              }`}
            >
              {lang === "es" ? cat.labelEs : cat.labelEn}
            </button>
          ))}
        </div>
      </section>

      {/* MERCHANT RESULTS COUNT & GRID */}
      <section className="max-w-md md:max-w-4xl mx-auto px-4 pt-2">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500 mb-3 px-1">
          <div className="flex items-center gap-1.5">
            <Store className="w-3.5 h-3.5 text-[#003ec7]" />
            <span>
              {filteredMerchants.length} {t.foundSuffix}
            </span>
          </div>
          {searchQuery && (
            <span className="text-slate-400 font-medium truncate max-w-[140px]">
              "{searchQuery}"
            </span>
          )}
        </div>

        {/* NEAT MOBILE-FIRST GRID */}
        {filteredMerchants.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            {filteredMerchants.map((merchant) => {
              const id = merchant.storeInfo.id;
              const Icon = MERCHANT_ICONS[id] || ShoppingBag;
              const badgeObj = MERCHANT_BADGES[id] || { en: "Local Business", es: "Negocio Local" };
              const badgeText = lang === "es" ? badgeObj.es : badgeObj.en;

              return (
                <Link
                  key={id}
                  href={`/${id}`}
                  className="group bg-white rounded-2xl p-4 border border-slate-200 hover:border-[#003ec7]/40 shadow-xs hover:shadow-md transition-all flex flex-col justify-between space-y-3 relative overflow-hidden"
                >
                  {/* Left Accent Stripe */}
                  <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-[#003ec7]" />

                  <div className="space-y-2.5 pl-1.5">
                    {/* Header: Icon + Badge */}
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl bg-blue-50 text-[#003ec7] flex items-center justify-center shadow-2xs group-hover:bg-[#003ec7] group-hover:text-white transition-colors">
                        <Icon className="w-5 h-5" />
                      </div>

                      <span className="text-[10px] font-extrabold uppercase tracking-wider text-[#003ec7] bg-blue-50 px-2.5 py-0.5 rounded-full border border-blue-100">
                        {badgeText}
                      </span>
                    </div>

                    {/* Merchant Name & Tagline */}
                    <div>
                      <h2 className="text-base font-extrabold text-slate-900 group-hover:text-[#003ec7] transition-colors leading-tight">
                        {merchant.storeInfo.name}
                      </h2>
                      <p className="text-xs text-slate-500 mt-0.5 line-clamp-2 leading-relaxed">
                        {merchant.storeInfo.tagline}
                      </p>
                    </div>

                    {/* Address & Phone Details */}
                    <div className="space-y-1 text-xs text-slate-600 pt-1 border-t border-slate-100">
                      <div className="flex items-center gap-1.5 truncate">
                        <MapPin className="w-3.5 h-3.5 text-[#003ec7] shrink-0" />
                        <span className="truncate">{merchant.storeInfo.address}</span>
                      </div>

                      <div className="flex items-center gap-1.5">
                        <Phone className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                        <span>{merchant.storeInfo.phone}</span>
                      </div>
                    </div>

                    {/* Amenities Tags */}
                    <div className="flex flex-wrap gap-1 pt-1">
                      {merchant.storeInfo.amenities?.slice(0, 3).map((item, idx) => (
                        <span
                          key={idx}
                          className="text-[10px] font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md"
                        >
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Launch Action Bar */}
                  <div className="pt-2 pl-1.5 flex items-center justify-between text-xs font-extrabold text-[#003ec7] group-hover:translate-x-0.5 transition-transform">
                    <span>{t.launchBtn}</span>
                    <ChevronRight className="w-4 h-4 text-[#003ec7]" />
                  </div>
                </Link>
              );
            })}
          </div>
        ) : (
          <div className="bg-white rounded-2xl p-8 text-center space-y-3 border border-slate-200 my-4 shadow-xs">
            <Store className="w-10 h-10 text-slate-300 mx-auto" />
            <h3 className="font-extrabold text-slate-800 text-sm">
              {t.noResultsTitle}
            </h3>
            <p className="text-xs text-slate-500 max-w-xs mx-auto">
              {t.noResultsDesc}
            </p>
            <button
              onClick={() => {
                setSearchQuery("");
                setSelectedCategory("all");
              }}
              className="px-4 py-2 rounded-xl bg-[#003ec7] text-white font-extrabold text-xs shadow-sm hover:brightness-110 transition-all"
            >
              {t.clearBtn}
            </button>
          </div>
        )}
      </section>

      {/* FOOTER */}
      <footer className="max-w-md md:max-w-4xl mx-auto px-4 pt-10 text-center text-xs text-slate-400">
        <p>© {new Date().getFullYear()} {t.footerText}</p>
      </footer>
    </main>
  );
}
