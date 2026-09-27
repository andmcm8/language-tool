"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { getAllMerchants as getAllPlaces, isValidPhone } from "@/lib/merchants";
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
  Info,
} from "lucide-react";

const PLACE_ICONS: Record<string, any> = {
  demo: ShoppingBag,
  elsol: ShoppingBag,
};

const PLACE_TAGLINES: Record<string, { en: string; es: string }> = {
  demo: {
    es: "Tu Tienda Hispana Local en Stamford — Asistente Demo",
    en: "Your Local Hispanic Store in Stamford — Demo Assistant",
  },
  elsol: {
    es: "Tu Tienda Hispana Local en Stamford — Asistente Demo",
    en: "Your Local Hispanic Store in Stamford — Demo Assistant",
  },
};

const DICT = {
  en: {
    portalBadge: "Language Assistance Tool",
    portalTitle: "DuoTaps",
    subtitle:
      "Explore Connecticut restaurants, delis, and cafes with interactive bilingual Spanish menus and customer assistance.",
    searchPlaceholder: "Search places by name, city, cuisine...",
    foundSuffix: "Places Found",
    launchBtn: "View Bilingual Menu",
    noResultsTitle: "No Places Match Your Search",
    noResultsDesc:
      'Try searching for "Pizza", "Tacos", "Stamford", or click "Clear Search" above.',
    clearBtn: "Clear Search & Show All",
    monFri: "Mon-Fri",
    footerText: "DuoTaps • Language Assistance Tool",
  },
  es: {
    portalBadge: "Herramienta de Asistencia Lingüística",
    portalTitle: "DuoTaps",
    subtitle:
      "Explore restaurantes, delis y cafeterías de Connecticut con menús interactivos en español y asistencia al cliente.",
    searchPlaceholder: "Buscar lugares por nombre, ciudad, tipo de comida...",
    foundSuffix: "Lugares Encontrados",
    launchBtn: "Ver Menú Bilingüe",
    noResultsTitle: "No se encontraron lugares para su búsqueda",
    noResultsDesc:
      'Intente buscar "Pizza", "Tacos", "Stamford", o presione "Borrar Búsqueda" arriba.',
    clearBtn: "Borrar Búsqueda y Mostrar Todos",
    monFri: "Lun-Vie",
    footerText: "DuoTaps • Herramienta de Asistencia Lingüística",
  },
};


export default function HomePage() {
  const allPlaces = useMemo(() => {
    return getAllPlaces().filter((m) => {
      const id = (m.storeInfo?.id || "").toLowerCase();
      const name = (m.storeInfo?.name || "").toLowerCase();
      return id !== "demo" && id !== "elsol" && !name.includes("demo market");
    });
  }, []);

  const [searchQuery, setSearchQuery] = useState("");
  const [lang, setLang] = useState<"en" | "es">("en");
  const [showInfoModal, setShowInfoModal] = useState(false);

  const t = DICT[lang];

  /* ---------- Real-Time Filtering Logic ---------- */
  const filteredPlaces = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    if (!q) return allPlaces;

    return allPlaces.filter((m) => {
      const name = (m.storeInfo?.name || (m.storeInfo as any)?.Name || "").toLowerCase();
      const tagline = (m.storeInfo?.tagline || "").toLowerCase();
      const address = (m.storeInfo?.address || "").toLowerCase();

      return (
        name.includes(q) ||
        tagline.includes(q) ||
        address.includes(q)
      );
    });
  }, [allPlaces, searchQuery]);

  return (
    <main className="min-h-screen bg-[#f7f9fb] text-slate-800 font-sans selection:bg-primary selection:text-white pb-20">
      {/* ROYAL BLUE MOBILE-FIRST HEADER */}
      <header className="bg-[#003ec7] text-white shadow-md">
        <div className="max-w-md md:max-w-4xl mx-auto px-4 py-4 space-y-3">
          {/* Top Title & WORKING Interactive EN / ES Language Swapper Toggle */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm overflow-hidden shrink-0">
                <img
                  src="/logo.jpg"
                  alt="DuoTaps Logo"
                  className="w-full h-full object-cover scale-110"
                />
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

            {/* EXACT MATCH: Segmented Pill Toggle Switch (ES / EN | Info) */}
            <div className="flex items-center gap-0.5 bg-white text-slate-800 p-1 rounded-full border border-white/30 shadow-md">
              <button
                onClick={() => setLang("es")}
                className={`px-3 py-1 rounded-full text-xs font-black transition-all ${
                  lang === "es"
                    ? "bg-[#003ec7] text-white shadow-xs"
                    : "text-slate-700 hover:text-slate-900"
                }`}
              >
                ES
              </button>
              <button
                onClick={() => setLang("en")}
                className={`px-3 py-1 rounded-full text-xs font-black transition-all ${
                  lang === "en"
                    ? "bg-[#003ec7] text-white shadow-xs"
                    : "text-slate-700 hover:text-slate-900"
                }`}
              >
                EN
              </button>

              <div className="w-px h-3.5 bg-slate-300 mx-0.5" />

              <button
                onClick={() => setShowInfoModal(true)}
                className="p-1 rounded-full text-slate-600 hover:text-[#003ec7] transition-colors"
                title="Portal Info / Información"
                aria-label="Portal Info"
              >
                <Info className="w-4 h-4" />
              </button>
            </div>
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

      {/* RESULTS COUNT & GRID */}
      <section className="max-w-md md:max-w-4xl mx-auto px-4 pt-4">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500 mb-3 px-1">
          <div className="flex items-center gap-1.5">
            <Store className="w-3.5 h-3.5 text-[#003ec7]" />
            <span>
              {filteredPlaces.length} {t.foundSuffix}
            </span>
          </div>
          {searchQuery && (
            <span className="text-slate-400 font-medium truncate max-w-[140px]">
              "{searchQuery}"
            </span>
          )}
        </div>

        {/* NEAT MOBILE-FIRST GRID */}
        {filteredPlaces.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            {filteredPlaces.map((place) => {
              const id = place.storeInfo.id;
              const Icon = PLACE_ICONS[id] || ShoppingBag;

              return (
                <Link
                  key={id}
                  href={`/${id}`}
                  className="group bg-white rounded-2xl p-4 border border-slate-200 hover:border-[#003ec7]/40 shadow-xs hover:shadow-md transition-all flex flex-col justify-between space-y-3 relative overflow-hidden"
                >
                  {/* Left Accent Stripe */}
                  <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-[#003ec7]" />

                  <div className="space-y-2.5 pl-1.5">
                    {/* Header: Icon */}
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl bg-blue-50 text-[#003ec7] flex items-center justify-center shadow-2xs group-hover:bg-[#003ec7] group-hover:text-white transition-colors">
                        <Icon className="w-5 h-5" />
                      </div>
                    </div>

                    {/* Place Name & Tagline */}
                    <div>
                      <h2 className="text-base font-extrabold text-slate-900 group-hover:text-[#003ec7] transition-colors leading-tight">
                        {place.storeInfo.name}
                      </h2>
                      <p className="text-xs text-slate-500 mt-0.5 line-clamp-2 leading-relaxed">
                        {PLACE_TAGLINES[id]?.[lang] || place.storeInfo.tagline}
                      </p>
                    </div>

                    {/* Address & Phone Details */}
                    <div className="space-y-1 text-xs text-slate-600 pt-1 border-t border-slate-100">
                      <div className="flex items-center gap-1.5 truncate">
                        <MapPin className="w-3.5 h-3.5 text-[#003ec7] shrink-0" />
                        <span className="truncate">{place.storeInfo.address}</span>
                      </div>

                      {isValidPhone(place.storeInfo.phone) ? (
                        <div className="flex items-center gap-1.5">
                          <Phone className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                          <span>{place.storeInfo.phone}</span>
                        </div>
                      ) : place.storeInfo.hours?.monday_friday ? (
                        <div className="flex items-center gap-1.5">
                          <Clock className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                          <span>{place.storeInfo.hours.monday_friday}</span>
                        </div>
                      ) : null}
                    </div>
                  </div>

                  {/* Action Bar */}
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

      {/* PORTAL INFO MODAL DIALOG */}
      {showInfoModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl p-6 max-w-sm w-full space-y-4 shadow-2xl border border-slate-100 relative">
            <button
              onClick={() => setShowInfoModal(false)}
              className="absolute top-4 right-4 p-1.5 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-blue-50 text-[#003ec7] flex items-center justify-center font-black text-xl shadow-2xs">
                D
              </div>
              <div>
                <h3 className="font-extrabold text-base text-slate-900 leading-tight">
                  {lang === "es" ? "Acerca de DuoTaps" : "About DuoTaps"}
                </h3>
                <p className="text-xs text-[#003ec7] font-bold">
                  {lang === "es" ? "Menús Bilingües y Asistentes IA" : "Bilingual Menus & AI Assistants"}
                </p>
              </div>
            </div>

            <div className="space-y-2.5 text-xs text-slate-600 leading-relaxed border-t border-slate-100 pt-3">
              <p>
                {lang === "es"
                  ? "DuoTaps ayuda a restaurantes, cafeterías y delis de Connecticut a comunicarse con clientes hispanohablantes mediante menús traducidos al español y asistencia al comensal."
                  : "DuoTaps helps Connecticut restaurants, cafes, and delis serve Spanish-speaking guests with instant bilingual translated menus and AI customer assistance."}
              </p>
              <p className="font-semibold text-slate-800">
                {lang === "es"
                  ? "¿Es dueño de un restaurante? Contáctenos para reclamar o personalizar su menú oficial de forma gratuita."
                  : "Are you a restaurant owner? Contact us to claim or customize your official menu for free."}
              </p>
            </div>

            <button
              onClick={() => setShowInfoModal(false)}
              className="w-full py-2.5 bg-[#003ec7] text-white font-extrabold text-xs rounded-xl shadow-sm hover:brightness-110 transition-all"
            >
              {lang === "es" ? "Entendido" : "Got It"}
            </button>
          </div>
        </div>
      )}
    </main>
  );
}
