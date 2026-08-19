import { NextRequest } from "next/server";
import { google } from "googleapis";

// 1x1 Transparent GIF Uint8Array (43 bytes)
const GIF_BYTES = new Uint8Array([
  0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 0x01, 0x00, 0x01, 0x00, 0x80, 0x00,
  0x00, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x21, 0xf9, 0x04, 0x01, 0x00,
  0x00, 0x00, 0x00, 0x2c, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
  0x00, 0x02, 0x02, 0x44, 0x01, 0x00, 0x3b
]);

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
        setTimeout(() => reject(new Error("Sheets API Timeout")), 2500)
      ),
    ]);

    const rows = res.data.values || [];
    const normEmail = decodeURIComponent(email).toLowerCase().trim();

    let targetRowIndex = -1;
    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];
      if (row && row[1] && row[1].toLowerCase().trim() === normEmail) {
        targetRowIndex = i + 1;
        break;
      }
    }

    const timestamp = new Date().toLocaleString("en-US", { timeZone: "America/New_York" });
    const openValue = `YES (${timestamp})`;

    if (targetRowIndex > 0) {
      await Promise.race([
        sheets.spreadsheets.values.update({
          spreadsheetId,
          range: `Sheet1!H${targetRowIndex}`,
          valueInputOption: "USER_ENTERED",
          requestBody: { values: [[openValue]] },
        }),
        new Promise<never>((_, reject) =>
          setTimeout(() => reject(new Error("Sheets Update Timeout")), 2500)
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
    logOpenToSheet(email, biz).catch(() => {});
  }

  return new Response(GIF_BYTES, {
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
