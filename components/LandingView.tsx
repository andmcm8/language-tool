"use client";

import React from "react";
import { TabType } from "./BottomNav";
import { MerchantConfig } from "@/types/merchant";
import { ShoppingBag, Languages, MessageSquare, Mic, ChevronRight } from "lucide-react";

interface LandingViewProps {
  merchant: MerchantConfig;
  setActiveTab: (tab: TabType) => void;
  lang: "es" | "en";
}

export default function LandingView({ merchant, setActiveTab, lang }: LandingViewProps) {
  const cards = [
    {
      id: "catalog" as TabType,
      titleEs: "Catálogo & Servicios",
      titleEn: "Catalog & Services",
      descEs: `Explorar catálogo de ${merchant.storeInfo.name}`,
      descEn: `Browse ${merchant.storeInfo.name} catalog & items`,
      icon: ShoppingBag,
      gradient: "from-blue-500/10 to-indigo-500/5",
      border: "hover:border-blue-500/30",
      accentBg: "bg-blue-500/10 text-blue-600",
    },
    {
      id: "camera" as TabType,
      titleEs: "Traductor Bilingüe",
      titleEn: "Bilingual Translator",
      descEs: "Traducción de texto y voz en tiempo real con frases rápidas",
      descEn: "Real-time text & voice translation with quick store phrases",
      icon: Languages,
      gradient: "from-emerald-500/10 to-teal-500/5",
      border: "hover:border-emerald-500/30",
      accentBg: "bg-emerald-500/10 text-emerald-600",
    },
    {
      id: "assistant" as TabType,
      titleEs: "Asistente IA de la Tienda",
      titleEn: "Store AI Assistant",
      descEs: "Respuestas inmediatas sobre horarios, ubicación y preguntas",
      descEn: "Instant grounded answers for hours, location & policies",
      icon: MessageSquare,
      gradient: "from-violet-500/10 to-purple-500/5",
      border: "hover:border-violet-500/30",
      accentBg: "bg-violet-500/10 text-violet-600",
    },
    {
      id: "assistant" as TabType,
      titleEs: "Asistente por Voz en Español",
      titleEn: "Voice-Enabled Assistant",
      descEs: "Interacción manos libres con voz y audio en español",
      descEn: "Hands-free spoken Spanish Q&A with live audio",
      icon: Mic,
      gradient: "from-amber-500/10 to-orange-500/5",
      border: "hover:border-amber-500/30",
      accentBg: "bg-amber-500/10 text-amber-600",
    },
  ];

  return (
    <div className="w-full flex-1 flex flex-col p-4 max-w-md mx-auto min-h-[calc(100vh-130px)] pb-24 justify-center">
      <div className="flex-1 flex flex-col justify-between gap-3.5 w-full my-auto">
        {cards.map((card, index) => {
          const Icon = card.icon;
          return (
            <div
              key={index}
              onClick={() => setActiveTab(card.id)}
              className={`group relative flex-1 flex items-center justify-between p-5 md:p-6 bg-surface rounded-3xl border border-secondary-fixed/50 shadow-2xs hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 cursor-pointer overflow-hidden w-full min-h-[110px] ${card.border}`}
            >
              <div className={`absolute top-0 right-0 w-36 h-36 bg-gradient-to-br ${card.gradient} rounded-full blur-xl group-hover:scale-150 transition-transform duration-500`} />

              <div className="flex items-center gap-4 relative z-10 min-w-0 flex-1">
                <div className={`w-13 h-13 rounded-2xl ${card.accentBg} flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform shadow-2xs`}>
                  <Icon className="w-6.5 h-6.5" />
                </div>

                <div className="min-w-0 flex-1">
                  <h3 className="font-bold text-base md:text-lg text-on-surface leading-tight">
                    {lang === "es" ? card.titleEs : card.titleEn}
                  </h3>
                  <p className="text-xs md:text-sm text-on-surface-variant font-normal mt-1 leading-snug line-clamp-2">
                    {lang === "es" ? card.descEs : card.descEn}
                  </p>
                </div>
              </div>

              <div className="relative z-10 shrink-0 ml-3">
                <div className="w-8.5 h-8.5 rounded-full bg-surface-container flex items-center justify-center text-on-surface-variant group-hover:bg-primary group-hover:text-white transition-all shadow-2xs">
                  <ChevronRight className="w-4.5 h-4.5 group-hover:translate-x-0.5 transition-transform" />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
