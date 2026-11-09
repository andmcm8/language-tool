"use client";

import React from "react";
import { TabType } from "./BottomNav";
import { MerchantConfig } from "@/types/merchant";
import { BookOpen, Languages, MessageSquareText, Mic, ArrowUpRight } from "lucide-react";

interface LandingViewProps {
  merchant: MerchantConfig;
  setActiveTab: (tab: TabType) => void;
  lang: "es" | "en";
}

export default function LandingView({ merchant, setActiveTab, lang }: LandingViewProps) {
  const cards = [
    {
      id: "catalog" as TabType,
      title: lang === "es" ? "Ver el menú" : "Browse the menu",
      desc: lang === "es" ? `Todo el menú de ${merchant.storeInfo.name}, en español` : `Everything at ${merchant.storeInfo.name}, in Spanish`,
      icon: BookOpen,
      primary: true,
    },
    {
      id: "camera" as TabType,
      title: lang === "es" ? "Traductor" : "Translator",
      desc: lang === "es" ? "Texto, voz y cámara en tiempo real" : "Text, voice and camera, live",
      icon: Languages,
    },
    {
      id: "assistant" as TabType,
      title: lang === "es" ? "Asistente con IA" : "AI assistant",
      desc: lang === "es" ? "Horarios, ubicación y preguntas del menú" : "Hours, location and menu questions",
      icon: MessageSquareText,
    },
    {
      id: "assistant" as TabType,
      title: lang === "es" ? "Asistente por voz" : "Voice assistant",
      desc: lang === "es" ? "Habla en español, manos libres" : "Hands-free spoken Spanish",
      icon: Mic,
    },
  ];

  return (
    <div className="w-full max-w-md mx-auto px-4 pt-5 space-y-3">
      <h2 className="px-1 text-[28px] leading-tight font-extrabold text-on-surface">
        {lang === "es" ? "¿Qué necesitas?" : "How can we help?"}
      </h2>
      {cards.map((card, i) => {
        const Icon = card.icon;
        return (
          <button
            key={i}
            onClick={() => setActiveTab(card.id)}
            className={`group w-full text-left flex items-center gap-4 rounded-3xl p-4 transition-all duration-200 active:scale-[0.99] ${
              card.primary
                ? "bg-brand-gradient text-white shadow-brand"
                : "bg-white border border-white shadow-soft hover:shadow-lift"
            }`}
          >
            <span className={`grid h-12 w-12 shrink-0 place-items-center rounded-2xl ${card.primary ? "bg-white/20" : "bg-primary-fixed text-primary"}`}>
              <Icon className="h-6 w-6" />
            </span>
            <span className="min-w-0 flex-1">
              <span className="block text-[16px] font-bold leading-tight">{card.title}</span>
              <span className={`mt-0.5 block text-[13px] leading-snug ${card.primary ? "text-blue-50/90" : "text-on-surface-variant"}`}>{card.desc}</span>
            </span>
            <ArrowUpRight className={`h-5 w-5 shrink-0 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5 ${card.primary ? "text-white" : "text-on-surface-variant"}`} />
          </button>
        );
      })}
    </div>
  );
}
