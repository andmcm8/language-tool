"use client";

import React, { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { MerchantConfig } from "@/types/merchant";
import Header from "@/components/Header";
import BottomNav, { TabType } from "@/components/BottomNav";
import LandingView from "@/components/LandingView";
import CatalogTab from "@/components/CatalogTab";
import TranslatorTab from "@/components/TranslatorTab";
import AiAssistantTab from "@/components/AiAssistantTab";

interface StorefrontProps {
  merchant: MerchantConfig;
}

function MerchantStorefrontContent({ merchant }: StorefrontProps) {
  const searchParams = useSearchParams();

  // Allow URL to specify tab (e.g. ?tab=catalog or ?view=catalog).
  // Default to the menu so a shared link lands straight on it.
  const requestedTab = searchParams.get("tab") || searchParams.get("view");
  const initialTab: TabType =
    requestedTab === "home" ? "home" :
    requestedTab === "camera" || requestedTab === "translator" ? "camera" :
    requestedTab === "assistant" ? "assistant" :
    "catalog";

  const [activeTab, setActiveTab] = useState<TabType>(initialTab);

  // Allow URL to specify language (?lang=es or ?lang=en, defaults to en)
  const requestedLang = searchParams.get("lang");
  const initialLang: "es" | "en" = requestedLang === "es" ? "es" : "en";
  const [lang, setLang] = useState<"es" | "en">(initialLang);

  return (
    <div className="min-h-screen flex flex-col text-on-surface">
      <Header merchant={merchant} lang={lang} setLang={setLang} activeTab={activeTab} setActiveTab={setActiveTab} />

      <main key={activeTab} className={`flex-1 flex flex-col animate-rise lg:pl-[21rem] xl:pl-[22.75rem] ${activeTab === "assistant" ? "" : "pb-28 lg:pb-10"}`}>
        {activeTab === "home" && <LandingView merchant={merchant} setActiveTab={setActiveTab} lang={lang} />}
        {activeTab === "catalog" && <CatalogTab merchant={merchant} lang={lang} />}
        {activeTab === "camera" && <TranslatorTab lang={lang} />}
        {activeTab === "assistant" && <AiAssistantTab merchant={merchant} lang={lang} />}
      </main>

      <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} lang={lang} />
    </div>
  );
}

export default function MerchantStorefront({ merchant }: StorefrontProps) {
  return (
    <Suspense fallback={<div className="min-h-screen" />}>
      <MerchantStorefrontContent merchant={merchant} />
    </Suspense>
  );
}
