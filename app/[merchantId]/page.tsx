import type { Metadata } from "next";
import { getMerchantById } from "@/lib/merchants";
import MerchantStorefront from "@/components/MerchantStorefront";

interface PageProps {
  params: { merchantId: string };
}

export function generateMetadata({ params }: PageProps): Metadata {
  const { storeInfo } = getMerchantById(params.merchantId);
  return {
    title: `${storeInfo.name} — Bilingual Menu | DuoTaps`,
    description: storeInfo.tagline,
  };
}

export default function MerchantPage({ params }: PageProps) {
  // Resolved on the server so the browser only receives this one merchant's menu.
  const merchant = getMerchantById(params.merchantId);
  return <MerchantStorefront merchant={merchant} />;
}
