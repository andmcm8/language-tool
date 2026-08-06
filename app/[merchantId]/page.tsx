"use client";

import React, { useState } from "react";
import { getMerchantById } from "@/lib/merchants";
import Header from "@/components/Header";
import BottomNav, { TabType } from "@/components/BottomNav";
import LandingView from "@/components/LandingView";
import CatalogTab from "@/components/CatalogTab";
import TranslatorTab from "@/components/TranslatorTab";
import AiAssistantTab from "@/components/AiAssistantTab";

interface PageProps {
  params: {
    merchantId: string;
  };
}

export default function MerchantStorefront({ params }: PageProps) {
  const merchant = getMerchantById(params.merchantId);
  const [activeTab, setActiveTab] = useState<TabType>("home");
  const [lang, setLang] = useState<"es" | "en">("es");

  return (
    <div className="min-h-screen flex flex-col bg-surface text-on-surface">
      {/* Header with dynamic merchant info */}
      <Header merchant={merchant} lang={lang} setLang={setLang} />

      {/* Main Content Body */}
      <main className="flex-1 flex flex-col">
        {activeTab === "home" && (
          <LandingView merchant={merchant} setActiveTab={setActiveTab} lang={lang} />
        )}
        {activeTab === "catalog" && (
          <CatalogTab merchant={merchant} lang={lang} />
        )}
        {activeTab === "camera" && <TranslatorTab lang={lang} />}
        {activeTab === "assistant" && <AiAssistantTab merchant={merchant} lang={lang} />}
      </main>

      {/* Fixed Mobile Navigation Tab Bar */}
      <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} lang={lang} />
    </div>
  );
}
