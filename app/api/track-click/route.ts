import { NextRequest, NextResponse } from "next/server";
import { markLeadInSheet } from "@/lib/sheetsTracker";

const SITE_ORIGIN = "https://language-tool-six.vercel.app";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const email = searchParams.get("email") || "";
  const to = searchParams.get("to") || "/demo";

  if (email) {
    await markLeadInSheet(email, "I");
  }

  // Only redirect within this site, so the link can't be abused as an open redirect.
  let destination = `${SITE_ORIGIN}/demo`;
  try {
    const url = new URL(to, SITE_ORIGIN);
    if (url.origin === SITE_ORIGIN) destination = url.toString();
  } catch {
    // malformed "to" → default destination
  }

  return NextResponse.redirect(destination, 302);
}
