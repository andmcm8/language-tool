import { getAllMerchants } from "@/lib/merchants";
import HomeDirectory, { PlaceSummary } from "@/components/HomeDirectory";

export default function HomePage() {
  // Runs on the server: only the fields the directory cards need are sent to the browser.
  const places: PlaceSummary[] = getAllMerchants().map(({ storeInfo: s }) => ({
    storeInfo: {
      id: s.id,
      name: s.name,
      tagline: s.tagline,
      address: s.address,
      phone: s.phone,
      hours: { monday_friday: s.hours?.monday_friday },
    },
  }));

  return <HomeDirectory places={places} />;
}
