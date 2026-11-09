"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { isValidPhone } from "@/lib/phone";
import { townFromAddress, taglineFor, swatchFor, initialsOf } from "@/lib/place";
import { Search, X, MapPin, Phone, ChevronRight, Info, Languages, MessageSquareText, QrCode } from "lucide-react";

const DICT = {
  en: {
    portalTitle: "DuoTaps",
    heroLine1: "Every menu,",
    heroLine2: "in Spanish.",
    subtitle: "Bilingual menus and an AI assistant for Connecticut restaurants, cafes and delis.",
    searchPlaceholder: "Search by name, town or cuisine",
    places: "places",
    viewMenu: "View menu",
    all: "All",
    more: "Show more places",
    noResultsTitle: "No places match your search",
    noResultsDesc: "Try a different name, town or cuisine.",
    clearBtn: "Clear search",
    f1: "Bilingual menus",
    f1d: "Every dish in English and Spanish",
    f2: "Live translator",
    f2d: "Type, speak or scan a sign",
    f3: "AI assistant",
    f3d: "Ask about the menu in Spanish",
    footerText: "DuoTaps · Language Assistance Tool",
    aboutTitle: "About DuoTaps",
    aboutSub: "Bilingual menus & AI assistants",
    aboutP1: "DuoTaps helps Connecticut restaurants, cafes and delis serve Spanish-speaking guests with instant bilingual menus and AI customer assistance.",
    aboutP2: "Own a restaurant? Contact us to claim or customize your menu for free.",
    done: "Done",
  },
  es: {
    portalTitle: "DuoTaps",
    heroLine1: "Cada menú,",
    heroLine2: "en español.",
    subtitle: "Menús bilingües y un asistente con IA para restaurantes, cafeterías y delis de Connecticut.",
    searchPlaceholder: "Busca por nombre, ciudad o tipo de comida",
    places: "lugares",
    viewMenu: "Ver menú",
    all: "Todos",
    more: "Mostrar más lugares",
    noResultsTitle: "No encontramos lugares",
    noResultsDesc: "Prueba con otro nombre, ciudad o tipo de comida.",
    clearBtn: "Borrar búsqueda",
    f1: "Menús bilingües",
    f1d: "Cada platillo en inglés y español",
    f2: "Traductor en vivo",
    f2d: "Escribe, habla o escanea un letrero",
    f3: "Asistente con IA",
    f3d: "Pregunta sobre el menú en español",
    footerText: "DuoTaps · Herramienta de Asistencia Lingüística",
    aboutTitle: "Acerca de DuoTaps",
    aboutSub: "Menús bilingües y asistentes con IA",
    aboutP1: "DuoTaps ayuda a restaurantes, cafeterías y delis de Connecticut a atender a clientes hispanohablantes con menús bilingües y asistencia con IA.",
    aboutP2: "¿Es dueño de un restaurante? Contáctenos para reclamar o personalizar su menú gratis.",
    done: "Listo",
  },
};

// Cuisine filters: label + keywords matched against name & tagline
const CUISINES: { id: string; en: string; es: string; re: RegExp }[] = [
  { id: "pizza", en: "Pizza", es: "Pizza", re: /pizz/i },
  { id: "italian", en: "Italian", es: "Italiana", re: /ital|pasta|trattoria|ristorante/i },
  { id: "mexican", en: "Mexican", es: "Mexicana", re: /mexic|taco|burrito|cantina/i },
  { id: "asian", en: "Asian", es: "Asiática", re: /chinese|asian|thai|sushi|japan|ramen|pho|viet|korean|noodle|hibachi|chino/i },
  { id: "indian", en: "Indian", es: "India", re: /indian|india/i },
  { id: "seafood", en: "Seafood", es: "Mariscos", re: /seafood|lobster|oyster|fish|clam|marisc/i },
  { id: "american", en: "American", es: "Americana", re: /american|burger|grill|bbq|barbecue|steak|tavern|pub|diner/i },
  { id: "cafe", en: "Cafe & Bakery", es: "Café y panadería", re: /cafe|café|coffee|bakery|bake|donut|bagel|pastry|dessert|ice cream/i },
];

const PAGE = 30;

/** Slim per-place data sent to the browser (not the full menus). */
export interface PlaceSummary {
  storeInfo: {
    id: string;
    name: string;
    tagline: string;
    address: string;
    phone: string;
    hours?: { monday_friday?: string };
  };
}

export default function HomeDirectory({ places: allPlaces }: { places: PlaceSummary[] }) {
  const [searchQuery, setSearchQuery] = useState("");
  const [lang, setLang] = useState<"en" | "es">("en");
  const [cuisine, setCuisine] = useState("all");
  const [visible, setVisible] = useState(PAGE);
  const [showInfoModal, setShowInfoModal] = useState(false);

  const t = DICT[lang];

  const filteredPlaces = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    const c = CUISINES.find((x) => x.id === cuisine);
    return allPlaces.filter((m) => {
      const s = m.storeInfo;
      const hay = `${s.name} ${s.tagline} ${s.address}`;
      if (c && !c.re.test(`${s.name} ${s.tagline}`)) return false;
      return !q || hay.toLowerCase().includes(q);
    });
  }, [allPlaces, searchQuery, cuisine]);

  const shown = filteredPlaces.slice(0, visible);

  const onSearch = (v: string) => {
    setSearchQuery(v);
    setVisible(PAGE);
  };
  const onCuisine = (id: string) => {
    setCuisine(id);
    setVisible(PAGE);
  };

  const features = [
    { icon: QrCode, title: t.f1, desc: t.f1d },
    { icon: Languages, title: t.f2, desc: t.f2d },
    { icon: MessageSquareText, title: t.f3, desc: t.f3d },
  ];

  return (
    <main className="min-h-screen pb-16 selection:bg-primary selection:text-white">
      {/* HERO */}
      <header className="relative overflow-hidden bg-brand-gradient text-white rounded-b-[40px] shadow-lift">
        <div className="pointer-events-none absolute -top-24 -right-16 h-72 w-72 rounded-full bg-white/15 blur-3xl" />
        <div className="pointer-events-none absolute top-24 -left-24 h-64 w-64 rounded-full bg-sky-300/30 blur-3xl" />

        <div className="relative mx-auto max-w-md md:max-w-4xl px-5 pt-5 pb-20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <span className="grid h-10 w-10 place-items-center overflow-hidden rounded-full bg-white shadow-soft">
                <img src="/logo.jpg" alt="DuoTaps" className="h-full w-full scale-110 object-cover" />
              </span>
              <span className="text-lg font-extrabold tracking-tight">{t.portalTitle}</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex items-center rounded-full bg-white/15 p-1 backdrop-blur-md border border-white/25">
                {(["es", "en"] as const).map((code) => (
                  <button
                    key={code}
                    onClick={() => setLang(code)}
                    aria-pressed={lang === code}
                    className={`h-8 rounded-full px-3 text-xs font-bold transition-all ${
                      lang === code ? "bg-white text-primary shadow-soft" : "text-white/80 hover:text-white"
                    }`}
                  >
                    {code.toUpperCase()}
                  </button>
                ))}
              </div>
              <button
                onClick={() => setShowInfoModal(true)}
                aria-label="Info"
                className="grid h-10 w-10 place-items-center rounded-full bg-white/15 backdrop-blur-md border border-white/25 hover:bg-white/25 transition-colors"
              >
                <Info className="h-[18px] w-[18px]" />
              </button>
            </div>
          </div>

          <h1 className="mt-9 text-[40px] md:text-6xl font-extrabold leading-[1.05] tracking-tight">
            {t.heroLine1}
            <br />
            <span className="text-sky-200">{t.heroLine2}</span>
          </h1>
          <p className="mt-3 max-w-sm md:max-w-lg text-[15px] leading-relaxed text-blue-50/90">{t.subtitle}</p>
        </div>
      </header>

      {/* SEARCH — overlaps hero */}
      <div className="relative z-10 mx-auto -mt-7 max-w-md md:max-w-4xl px-5">
        <div className="relative">
          <Search className="pointer-events-none absolute left-5 top-1/2 h-5 w-5 -translate-y-1/2 text-primary" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearch(e.target.value)}
            placeholder={t.searchPlaceholder}
            className="h-14 w-full rounded-full border border-white bg-white pl-13 pr-12 text-[15px] font-medium text-on-surface shadow-lift placeholder:text-on-surface-variant/60 focus:outline-none focus:ring-2 focus:ring-primary/40"
            style={{ paddingLeft: "3.25rem" }}
          />
          {searchQuery && (
            <button
              onClick={() => onSearch("")}
              aria-label="Clear"
              className="absolute right-4 top-1/2 -translate-y-1/2 rounded-full p-1.5 text-on-surface-variant hover:bg-surface-container"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      <section className="mx-auto max-w-md md:max-w-4xl px-5">
        {/* Feature strip */}
        <div className="mt-6 grid grid-cols-3 gap-2.5">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="rounded-3xl bg-white/80 backdrop-blur border border-white p-3.5 shadow-soft">
              <span className="grid h-9 w-9 place-items-center rounded-2xl bg-primary-fixed text-primary">
                <Icon className="h-[18px] w-[18px]" />
              </span>
              <p className="mt-2.5 text-[13px] font-bold leading-tight text-on-surface">{title}</p>
              <p className="mt-0.5 hidden text-[11px] leading-snug text-on-surface-variant sm:block">{desc}</p>
            </div>
          ))}
        </div>

        {/* Cuisine chips */}
        <div className="-mx-5 mt-6 flex items-center gap-2 overflow-x-auto px-5 pb-1">
          {[{ id: "all", en: t.all, es: t.all }, ...CUISINES].map((c) => {
            const active = cuisine === c.id;
            return (
              <button
                key={c.id}
                onClick={() => onCuisine(c.id)}
                className={`chip shrink-0 ${
                  active ? "bg-navy text-white shadow-soft" : "bg-white text-on-surface-variant border border-white shadow-soft hover:text-on-surface"
                }`}
              >
                {lang === "es" ? c.es : c.en}
              </button>
            );
          })}
        </div>

        {/* Count */}
        <div className="mt-6 mb-3 flex items-baseline justify-between px-1">
          <h2 className="text-xl font-extrabold text-on-surface">{lang === "es" ? "Lugares" : "Places"}</h2>
          <span className="text-sm font-semibold text-on-surface-variant tabular-nums">
            {filteredPlaces.length.toLocaleString()} {t.places}
          </span>
        </div>

        {/* LIST */}
        {filteredPlaces.length > 0 ? (
          <>
            <div className="grid grid-cols-1 gap-2.5 md:grid-cols-2">
              {shown.map((place) => {
                const s = place.storeInfo;
                const town = townFromAddress(s.address);
                const tag = taglineFor(s.tagline, lang);
                return (
                  <Link
                    key={s.id}
                    href={`/${s.id}`}
                    className="group flex items-center gap-3.5 rounded-3xl border border-white bg-white p-3.5 shadow-soft transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lift active:scale-[0.99]"
                  >
                    <span
                      className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl text-lg font-extrabold text-white shadow-soft"
                      style={{ background: swatchFor(s.name) }}
                    >
                      {initialsOf(s.name)}
                    </span>
                    <div className="min-w-0 flex-1">
                      <h3 className="truncate text-[15px] font-bold leading-snug text-on-surface">{s.name}</h3>
                      {tag && <p className="truncate text-[13px] text-on-surface-variant">{tag}</p>}
                      <div className="mt-1 flex items-center gap-3 text-xs font-medium text-on-surface-variant">
                        {town && (
                          <span className="flex min-w-0 items-center gap-1">
                            <MapPin className="h-3 w-3 shrink-0 text-primary" />
                            <span className="truncate">{town}</span>
                          </span>
                        )}
                        {isValidPhone(s.phone) && (
                          <span className="hidden items-center gap-1 sm:flex">
                            <Phone className="h-3 w-3 shrink-0 text-primary" />
                            {s.phone}
                          </span>
                        )}
                      </div>
                    </div>
                    <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-surface-container text-on-surface-variant transition-colors group-hover:bg-primary group-hover:text-white">
                      <ChevronRight className="h-[18px] w-[18px]" />
                    </span>
                  </Link>
                );
              })}
            </div>

            {visible < filteredPlaces.length && (
              <div className="mt-6 text-center">
                <button
                  onClick={() => setVisible((v) => v + PAGE * 2)}
                  className="rounded-full border border-white bg-white px-6 py-3 text-sm font-bold text-primary shadow-soft transition-all hover:shadow-lift active:scale-[0.98]"
                >
                  {t.more}
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="rounded-3xl bg-white p-10 text-center shadow-soft">
            <span className="mx-auto grid h-14 w-14 place-items-center rounded-full bg-surface-container text-on-surface-variant">
              <Search className="h-6 w-6" />
            </span>
            <h3 className="mt-4 text-base font-extrabold text-on-surface">{t.noResultsTitle}</h3>
            <p className="mx-auto mt-1 max-w-xs text-sm text-on-surface-variant">{t.noResultsDesc}</p>
            <button
              onClick={() => {
                onSearch("");
                onCuisine("all");
              }}
              className="btn-primary mt-5 h-11 px-6 text-sm"
            >
              {t.clearBtn}
            </button>
          </div>
        )}
      </section>

      <footer className="mx-auto max-w-md md:max-w-4xl px-5 pt-12 text-center text-xs font-medium text-on-surface-variant/70">
        © {new Date().getFullYear()} {t.footerText}
      </footer>

      {/* INFO MODAL */}
      {showInfoModal && (
        <div
          className="fixed inset-0 z-50 flex items-end justify-center bg-navy/50 p-4 backdrop-blur-sm animate-in fade-in duration-200 sm:items-center"
          onClick={() => setShowInfoModal(false)}
        >
          <div
            role="dialog"
            aria-modal="true"
            onClick={(e) => e.stopPropagation()}
            className="relative w-full max-w-sm rounded-[28px] bg-white p-6 shadow-float animate-in slide-in-from-bottom duration-300"
          >
            <button
              onClick={() => setShowInfoModal(false)}
              aria-label="Close"
              className="absolute right-4 top-4 grid h-9 w-9 place-items-center rounded-full bg-surface-container text-on-surface-variant hover:text-on-surface"
            >
              <X className="h-4 w-4" />
            </button>
            <div className="flex items-center gap-3">
              <span className="grid h-12 w-12 place-items-center overflow-hidden rounded-2xl bg-white shadow-soft border border-surface-container">
                <img src="/logo.jpg" alt="" className="h-full w-full scale-110 object-cover" />
              </span>
              <div>
                <h3 className="text-lg font-extrabold leading-tight text-on-surface">{t.aboutTitle}</h3>
                <p className="text-xs font-semibold text-primary">{t.aboutSub}</p>
              </div>
            </div>
            <div className="mt-4 space-y-3 text-sm leading-relaxed text-on-surface-variant">
              <p>{t.aboutP1}</p>
              <p className="font-semibold text-on-surface">{t.aboutP2}</p>
            </div>
            <button onClick={() => setShowInfoModal(false)} className="btn-primary mt-5 h-12 w-full text-sm">
              {t.done}
            </button>
          </div>
        </div>
      )}
    </main>
  );
}
