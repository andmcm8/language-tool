import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getMerchantById, isRemovedPlace } from "@/lib/merchants";
import MerchantStorefront from "@/components/MerchantStorefront";

interface PageProps {
  params: { merchantId: string };
}

export function generateMetadata({ params }: PageProps): Metadata {
  if (isRemovedPlace(params.merchantId)) return { title: "Not found | DuoTaps" };
  const { storeInfo } = getMerchantById(params.merchantId);
  return {
    title: `${storeInfo.name} — Bilingual Menu | DuoTaps`,
    description: storeInfo.tagline,
  };
}

export default function MerchantPage({ params }: PageProps) {
  if (isRemovedPlace(params.merchantId)) notFound();
  // Resolved on the server so the browser only receives this one merchant's menu.
  const merchant = getMerchantById(params.merchantId);
  return <MerchantStorefront merchant={merchant} />;
}
