import { NextRequest, NextResponse } from "next/server";
import { google } from "googleapis";

// 1x1 Transparent GIF Buffer (43 bytes)
const TRANSPARENT_GIF = Buffer.from(
  "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
  "base64"
);

async function logOpenToSheet(email: string, biz: string) {
  try {
    const serviceAccountJson = process.env.GOOGLE_SERVICE_ACCOUNT_JSON;
    if (!serviceAccountJson) return;

    const credentials = JSON.parse(serviceAccountJson);
    const auth = new google.auth.GoogleAuth({
      credentials,
      scopes: ["https://www.googleapis.com/auth/spreadsheets"],
    });

    const sheets = google.sheets({ version: "v4", auth });
    const spreadsheetId = "1twWEsJ6jpAUEDd0zpF8lWOgkNoFWPjpRrlZV34gqkn4";

    // Fetch spreadsheet data
    const res = await sheets.spreadsheets.values.get({
      spreadsheetId,
      range: "Sheet1!A:I",
    });

    const rows = res.data.values || [];
    const normEmail = email.toLowerCase().trim();
    
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
      // Update Column H (Opened Email - Col 8)
      await sheets.spreadsheets.values.update({
        spreadsheetId,
        range: `Sheet1!H${targetRowIndex}`,
        valueInputOption: "USER_ENTERED",
        requestBody: { values: [[openValue]] },
      });
      console.log(`✅ Logged email open for ${email} on row ${targetRowIndex}`);
    }
  } catch (err) {
    console.error("⚠️ Open tracking logging error:", err);
  }
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const email = searchParams.get("email") || "";
  const biz = searchParams.get("biz") || "";

  if (email) {
    // Log asynchronously to Google Sheet
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
