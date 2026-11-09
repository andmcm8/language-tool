"use client";

import React from "react";
import { LayoutGrid, BookOpen, Languages, MessageSquareText } from "lucide-react";

export type TabType = "home" | "catalog" | "camera" | "assistant";

interface BottomNavProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  lang: "es" | "en";
}

export const NAV_TABS = [
  { id: "home" as TabType, labelEs: "Inicio", labelEn: "Home", icon: LayoutGrid },
  { id: "catalog" as TabType, labelEs: "Menú", labelEn: "Menu", icon: BookOpen },
  { id: "camera" as TabType, labelEs: "Traductor", labelEn: "Translate", icon: Languages },
  { id: "assistant" as TabType, labelEs: "Asistente", labelEn: "Assistant", icon: MessageSquareText },
];

export default function BottomNav({ activeTab, setActiveTab, lang }: BottomNavProps) {
  const tabs = NAV_TABS;

  return (
    <nav
      aria-label="Primary"
      className="fixed inset-x-0 bottom-0 z-40 px-4 pointer-events-none lg:hidden"
      style={{ paddingBottom: "max(14px, env(safe-area-inset-bottom))" }}
    >
      <div className="pointer-events-auto mx-auto max-w-md rounded-full bg-navy p-1.5 shadow-float">
        <div className="flex items-center gap-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                aria-current={isActive ? "page" : undefined}
                aria-label={lang === "es" ? tab.labelEs : tab.labelEn}
                className={`flex h-12 items-center justify-center gap-1.5 rounded-full text-[13px] font-semibold transition-all duration-300 ${
                  isActive
                    ? "flex-[2.2] bg-white text-primary shadow-soft"
                    : "flex-1 text-white/60 hover:text-white"
                }`}
              >
                <Icon className="h-[19px] w-[19px] shrink-0" strokeWidth={isActive ? 2.4 : 2} />
                {isActive && <span className="truncate">{lang === "es" ? tab.labelEs : tab.labelEn}</span>}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
