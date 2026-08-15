import { NextRequest, NextResponse } from "next/server";
import { google } from "googleapis";

async function logClickToSheet(email: string, biz: string) {
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
        targetRowIndex = i + 1;
        break;
      }
    }

    const timestamp = new Date().toLocaleString("en-US", { timeZone: "America/New_York" });
    const clickValue = `YES (${timestamp})`;

    if (targetRowIndex > 0) {
      // Update Column I (Clicked Link - Col 9)
      await sheets.spreadsheets.values.update({
        spreadsheetId,
        range: `Sheet1!I${targetRowIndex}`,
        valueInputOption: "USER_ENTERED",
        requestBody: { values: [[clickValue]] },
      });
      console.log(`✅ Logged demo link click for ${email} on row ${targetRowIndex}`);
    }
  } catch (err) {
    console.error("⚠️ Click tracking logging error:", err);
  }
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const email = searchParams.get("email") || "";
  const biz = searchParams.get("biz") || "";
  const to = searchParams.get("to") || "/demo";

  if (email) {
    logClickToSheet(email, biz).catch(() => {});
  }

  const destination = to.startsWith("http")
    ? to
    : `https://language-tool-six.vercel.app${to.startsWith("/") ? to : "/" + to}`;

  return NextResponse.redirect(destination, 302);
}
