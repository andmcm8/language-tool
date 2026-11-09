"use client";

import React from "react";
import { TabType } from "./BottomNav";
import { MerchantConfig } from "@/types/merchant";
import { isValidPhone } from "@/lib/phone";
import { townFromAddress, taglineFor, swatchFor, initialsOf } from "@/lib/place";
import { BookOpen, Languages, MessageSquareText, Mic, MapPin, Phone, Clock, Navigation } from "lucide-react";

interface LandingViewProps {
  merchant: MerchantConfig;
  setActiveTab: (tab: TabType) => void;
  lang: "es" | "en";
}

export default function LandingView({ merchant, setActiveTab, lang }: LandingViewProps) {
  const { storeInfo: s } = merchant;
  const town = townFromAddress(s.address);
  const tagline = taglineFor(s.tagline, lang);
  const hours = s.hours?.monday_friday && !/call/i.test(s.hours.monday_friday) ? s.hours.monday_friday : "";
  const mapsHref = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${s.name} ${s.address}`)}`;

  const actions = [
    { id: "camera" as TabType, icon: Languages, title: lang === "es" ? "Traductor" : "Translator", desc: lang === "es" ? "Texto, voz y cámara" : "Text, voice, camera" },
    { id: "assistant" as TabType, icon: MessageSquareText, title: lang === "es" ? "Asistente IA" : "AI assistant", desc: lang === "es" ? "Pregunta lo que quieras" : "Ask anything" },
    { id: "assistant" as TabType, icon: Mic, title: lang === "es" ? "Por voz" : "Voice", desc: lang === "es" ? "Habla en español" : "Speak Spanish" },
  ];

  return (
    <div className="w-full max-w-md md:max-w-2xl lg:max-w-3xl mx-auto px-4 lg:px-10 pt-5 lg:pt-10 space-y-4">
      {/* Place card */}
      <section className="relative overflow-hidden rounded-[32px] bg-brand-gradient p-5 text-white shadow-lift">
        <div className="pointer-events-none absolute -right-10 -top-12 h-44 w-44 rounded-full bg-white/15 blur-2xl" />
        <div className="relative flex items-center gap-3.5">
          <span
            className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl text-lg font-extrabold text-white ring-2 ring-white/40"
            style={{ background: swatchFor(s.name) }}
          >
            {initialsOf(s.name)}
          </span>
          <div className="min-w-0">
            <h2 className="text-[22px] font-extrabold leading-tight">{s.name}</h2>
            {tagline && <p className="mt-0.5 text-[13px] leading-snug text-blue-50/90 line-clamp-2">{tagline}</p>}
          </div>
        </div>

        <ul className="relative mt-5 space-y-2.5 text-[13px] font-medium text-white/95">
          {s.address && (
            <li className="flex items-start gap-2.5">
              <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-sky-200" />
              <span>{s.address}</span>
            </li>
          )}
          {hours && (
            <li className="flex items-start gap-2.5">
              <Clock className="mt-0.5 h-4 w-4 shrink-0 text-sky-200" />
              <span>
                {lang === "es" ? "Lun–Vie " : "Mon–Fri "}
                {hours}
              </span>
            </li>
          )}
        </ul>

        <div className="relative mt-5 grid grid-cols-2 gap-2.5">
          <a
            href={mapsHref}
            target="_blank"
            rel="noopener noreferrer"
            className="flex h-11 items-center justify-center gap-2 rounded-full bg-white text-[13px] font-bold text-primary shadow-soft active:scale-[0.98] transition"
          >
            <Navigation className="h-4 w-4" />
            {lang === "es" ? "Cómo llegar" : "Directions"}
          </a>
          {isValidPhone(s.phone) ? (
            <a
              href={`tel:${s.phone}`}
              className="flex h-11 items-center justify-center gap-2 rounded-full bg-white/15 text-[13px] font-bold text-white border border-white/30 active:scale-[0.98] transition"
            >
              <Phone className="h-4 w-4" />
              {lang === "es" ? "Llamar" : "Call"}
            </a>
          ) : (
            <span className="flex h-11 items-center justify-center rounded-full bg-white/10 text-[13px] font-semibold text-white/70 border border-white/20">
              {town}
            </span>
          )}
        </div>
      </section>

      {/* Primary action */}
      <button
        onClick={() => setActiveTab("catalog")}
        className="group flex w-full items-center gap-4 rounded-3xl bg-white p-4 text-left shadow-soft border border-white hover:shadow-lift active:scale-[0.99] transition-all"
      >
        <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-primary-fixed text-primary">
          <BookOpen className="h-6 w-6" />
        </span>
        <span className="min-w-0 flex-1">
          <span className="block text-[16px] font-bold leading-tight text-on-surface">
            {lang === "es" ? "Ver el menú" : "Browse the menu"}
          </span>
          <span className="mt-0.5 block text-[13px] text-on-surface-variant">
            {merchant.products.length} {lang === "es" ? "platillos en español e inglés" : "items in Spanish & English"}
          </span>
        </span>
        <span className="grid h-9 w-9 place-items-center rounded-full bg-primary text-white transition-transform group-hover:translate-x-0.5">
          <span aria-hidden className="text-lg leading-none">›</span>
        </span>
      </button>

      {/* Tools */}
      <div className="grid grid-cols-3 gap-2.5">
        {actions.map((a, i) => {
          const Icon = a.icon;
          return (
            <button
              key={i}
              onClick={() => setActiveTab(a.id)}
              className="flex flex-col items-start gap-3 rounded-3xl bg-white p-4 text-left shadow-soft border border-white hover:shadow-lift active:scale-[0.98] transition-all"
            >
              <span className="grid h-10 w-10 place-items-center rounded-2xl bg-primary-fixed text-primary">
                <Icon className="h-5 w-5" />
              </span>
              <span>
                <span className="block text-[14px] font-bold leading-tight text-on-surface">{a.title}</span>
                <span className="mt-0.5 block text-[11.5px] leading-snug text-on-surface-variant">{a.desc}</span>
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
