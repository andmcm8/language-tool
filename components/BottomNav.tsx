"use client";

import React from "react";
import { LayoutGrid, BookOpen, Camera, MessageSquareText } from "lucide-react";

export type TabType = "home" | "catalog" | "camera" | "assistant";

interface BottomNavProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  lang: "es" | "en";
}

export default function BottomNav({ activeTab, setActiveTab, lang }: BottomNavProps) {
  const tabs = [
    {
      id: "home" as TabType,
      labelEs: "Inicio",
      labelEn: "Home",
      icon: LayoutGrid,
    },
    {
      id: "catalog" as TabType,
      labelEs: "Catálogo",
      labelEn: "Catalog",
      icon: BookOpen,
    },
    {
      id: "camera" as TabType,
      labelEs: "Cámara OCR",
      labelEn: "Camera OCR",
      icon: Camera,
    },
    {
      id: "assistant" as TabType,
      labelEs: "Asistente AI",
      labelEn: "AI Assistant",
      icon: MessageSquareText,
    },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-surface-container-lowest/95 backdrop-blur-md border-t border-surface-container-high px-2 py-2 shadow-lg">
      <div className="max-w-md mx-auto grid grid-cols-4 gap-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex flex-col items-center justify-center py-1.5 px-1 rounded-2xl transition-all duration-200 ${
                isActive
                  ? "bg-secondary-fixed text-primary font-bold shadow-xs scale-102"
                  : "text-on-surface-variant hover:text-on-surface hover:bg-surface-container/50"
              }`}
            >
              <Icon
                className={`w-5 h-5 transition-transform duration-200 ${
                  isActive ? "scale-110 text-primary" : "text-on-surface-variant"
                }`}
              />
              <span className="text-[11px] font-medium leading-none mt-1 truncate">
                {lang === "es" ? tab.labelEs : tab.labelEn}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
