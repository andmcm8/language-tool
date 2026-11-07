import { google } from "googleapis";

/* ================================================================
   OUTREACH TRACKING → GOOGLE SHEET
   Credentials come from environment variables (never commit keys):
     GOOGLE_SERVICE_ACCOUNT_EMAIL
     GOOGLE_PRIVATE_KEY        (the "private_key" value; literal \n is fine)
     TRACKING_SPREADSHEET_ID   (optional, defaults to the outreach sheet)
   If they are missing, tracking is skipped and the routes still respond.
   ================================================================ */
const DEFAULT_SPREADSHEET_ID = "1twWEsJ6jpAUEDd0zpF8lWOgkNoFWPjpRrlZV34gqkn4";

/** Marks the row whose column B matches `email` with "YES (timestamp)" in `column`. */
export async function markLeadInSheet(email: string, column: "H" | "I"): Promise<void> {
  const clientEmail = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const privateKey = process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, "\n");
  if (!clientEmail || !privateKey) {
    console.warn("Sheet tracking skipped: GOOGLE_SERVICE_ACCOUNT_EMAIL / GOOGLE_PRIVATE_KEY not set.");
    return;
  }

  try {
    const auth = new google.auth.JWT({
      email: clientEmail,
      key: privateKey,
      scopes: ["https://www.googleapis.com/auth/spreadsheets"],
    });
    const sheets = google.sheets({ version: "v4", auth });
    const spreadsheetId = process.env.TRACKING_SPREADSHEET_ID || DEFAULT_SPREADSHEET_ID;

    const res = await sheets.spreadsheets.values.get({ spreadsheetId, range: "Sheet1!A:I" });
    const rows = res.data.values || [];
    const normEmail = email.toLowerCase().trim();

    const idx = rows.findIndex((row, i) => i > 0 && row?.[1]?.toLowerCase().trim() === normEmail);
    if (idx < 1) return;

    const timestamp = new Date().toLocaleString("en-US", { timeZone: "America/New_York" });
    await sheets.spreadsheets.values.update({
      spreadsheetId,
      range: `Sheet1!${column}${idx + 1}`,
      valueInputOption: "USER_ENTERED",
      requestBody: { values: [[`YES (${timestamp})`]] },
    });
  } catch (err: any) {
    console.warn("Sheet tracking notice:", err?.message || err);
  }
}
