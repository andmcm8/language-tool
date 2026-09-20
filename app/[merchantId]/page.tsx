"use client";

import React, { useState, Suspense } from "react";
import { useParams, useSearchParams } from "next/navigation";
import { getMerchantById } from "@/lib/merchants";
import Header from "@/components/Header";
import BottomNav, { TabType } from "@/components/BottomNav";
import LandingView from "@/components/LandingView";
import CatalogTab from "@/components/CatalogTab";
import TranslatorTab from "@/components/TranslatorTab";
import AiAssistantTab from "@/components/AiAssistantTab";

interface PageProps {
  params?: {
    merchantId?: string;
  };
}

function MerchantStorefrontContent({ params }: PageProps) {
  const routerParams = useParams();
  const rawId = (routerParams?.merchantId as string) || params?.merchantId || "";
  const merchant = getMerchantById(rawId);
  const searchParams = useSearchParams();

  // Allow URL to specify tab (e.g. ?tab=catalog or ?view=catalog)
  // Default directly to "catalog" so sending /demo sends users straight to the menu!
  const requestedTab = searchParams.get("tab") || searchParams.get("view");
  const initialTab: TabType = (
    requestedTab === "home" ? "home" :
    requestedTab === "camera" || requestedTab === "translator" ? "camera" :
    requestedTab === "assistant" ? "assistant" :
    "catalog"
  );

  const [activeTab, setActiveTab] = useState<TabType>(initialTab);

  // Allow URL to specify language (?lang=es or ?lang=en, defaults to en)
  const requestedLang = searchParams.get("lang");
  const initialLang: "es" | "en" = requestedLang === "es" ? "es" : "en";
  const [lang, setLang] = useState<"es" | "en">(initialLang);

  const handleTabChange = (newTab: TabType) => {
    setActiveTab(newTab);
  };

  return (
    <div className="min-h-screen flex flex-col bg-surface text-on-surface">
      {/* Header with dynamic merchant info and manual ES/EN toggle */}
      <Header merchant={merchant} lang={lang} setLang={setLang} />

      {/* Main Content Body */}
      <main className="flex-1 flex flex-col">
        {activeTab === "home" && (
          <LandingView merchant={merchant} setActiveTab={handleTabChange} lang={lang} />
        )}
        {activeTab === "catalog" && (
          <CatalogTab merchant={merchant} lang={lang} />
        )}
        {activeTab === "camera" && <TranslatorTab lang={lang} />}
        {activeTab === "assistant" && <AiAssistantTab merchant={merchant} lang={lang} />}
      </main>

      {/* Fixed Mobile Navigation Tab Bar */}
      <BottomNav activeTab={activeTab} setActiveTab={handleTabChange} lang={lang} />
    </div>
  );
}

export default function MerchantStorefront({ params }: PageProps) {
  return (
    <Suspense fallback={<div className="min-h-screen bg-surface" />}>
      <MerchantStorefrontContent params={params} />
    </Suspense>
  );
}

