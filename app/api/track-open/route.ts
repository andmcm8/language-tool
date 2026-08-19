import { NextRequest, NextResponse } from "next/server";
import { google } from "googleapis";

// 1x1 Transparent GIF Buffer (43 bytes)
const TRANSPARENT_GIF = Buffer.from(
  "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
  "base64"
);

const SERVICE_ACCOUNT_CREDENTIALS = {
  type: "service_account",
  project_id: "alconio",
  private_key_id: "REMOVED_SECRET",
  private_key: "REMOVED_SECRET",
  client_email: "duotaps@alconio.iam.gserviceaccount.com",
  client_id: "106794621529861444597",
};

async function logOpenToSheet(email: string, biz: string) {
  try {
    const auth = new google.auth.GoogleAuth({
      credentials: SERVICE_ACCOUNT_CREDENTIALS,
      scopes: ["https://www.googleapis.com/auth/spreadsheets"],
    });

    const sheets = google.sheets({ version: "v4", auth });
    const spreadsheetId = "1twWEsJ6jpAUEDd0zpF8lWOgkNoFWPjpRrlZV34gqkn4";

    const res = await Promise.race([
      sheets.spreadsheets.values.get({
        spreadsheetId,
        range: "Sheet1!A:I",
      }),
      new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error("Sheets API Timeout")), 3000)
      ),
    ]);

    const rows = res.data.values || [];
    const normEmail = decodeURIComponent(email).toLowerCase().trim();

    let targetRowIndex = -1;
    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];
      if (row && row[1] && row[1].toLowerCase().trim() === normEmail) {
        targetRowIndex = i + 1; // 1-indexed for Sheets
        break;
      }
    }

    const timestamp = new Date().toLocaleString("en-US", { timeZone: "America/New_York" });
    const openValue = `YES (${timestamp})`;

    if (targetRowIndex > 0) {
      // Update Column H (Email Opened - Col 8) with timeout protection
      await Promise.race([
        sheets.spreadsheets.values.update({
          spreadsheetId,
          range: `Sheet1!H${targetRowIndex}`,
          valueInputOption: "USER_ENTERED",
          requestBody: { values: [[openValue]] },
        }),
        new Promise<never>((_, reject) =>
          setTimeout(() => reject(new Error("Sheets Update Timeout")), 3000)
        ),
      ]);
      console.log(`✅ Logged email open for ${email} on row ${targetRowIndex}`);
    }
  } catch (err: any) {
    console.warn("Open tracking background notice:", err?.message || err);
  }
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const email = searchParams.get("email") || "";
  const biz = searchParams.get("biz") || "";

  if (email) {
    // Non-blocking execution
    logOpenToSheet(email, biz).catch(() => {});
  }

  return new NextResponse(TRANSPARENT_GIF, {
    status: 200,
    headers: {
      "Content-Type": "image/gif",
      "Content-Length": "43",
      "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
      "Pragma": "no-cache",
      "Expires": "0",
    },
  });
}
