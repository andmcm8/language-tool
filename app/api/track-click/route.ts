import { NextRequest, NextResponse } from "next/server";
import { google } from "googleapis";

const SERVICE_ACCOUNT_CREDENTIALS = {
  type: "service_account",
  project_id: "alconio",
  private_key_id: "REMOVED_SECRET",
  private_key: "REMOVED_SECRET",
  client_email: "duotaps@alconio.iam.gserviceaccount.com",
  client_id: "106794621529861444597",
};

async function logClickToSheet(email: string, biz: string) {
  try {
    const auth = new google.auth.JWT({
      email: SERVICE_ACCOUNT_CREDENTIALS.client_email,
      key: SERVICE_ACCOUNT_CREDENTIALS.private_key,
      scopes: ["https://www.googleapis.com/auth/spreadsheets"],
    });

    const sheets = google.sheets({ version: "v4", auth });
    const spreadsheetId = "1twWEsJ6jpAUEDd0zpF8lWOgkNoFWPjpRrlZV34gqkn4";

    const res = await sheets.spreadsheets.values.get({
      spreadsheetId,
      range: "Sheet1!A:I",
    });

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
    const clickValue = `YES (${timestamp})`;

    if (targetRowIndex > 0) {
      await sheets.spreadsheets.values.update({
        spreadsheetId,
        range: `Sheet1!I${targetRowIndex}`,
        valueInputOption: "USER_ENTERED",
        requestBody: { values: [[clickValue]] },
      });
      console.log(`✅ Logged demo link click for ${email} on row ${targetRowIndex}`);
    }
  } catch (err: any) {
    console.warn("Click tracking background notice:", err?.message || err);
  }
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const email = searchParams.get("email") || "";
  const biz = searchParams.get("biz") || "";
  const to = searchParams.get("to") || "/demo";

  if (email) {
    await logClickToSheet(email, biz);
  }

  const destination = to.startsWith("http")
    ? to
    : `https://language-tool-six.vercel.app${to.startsWith("/") ? to : "/" + to}`;

  return NextResponse.redirect(destination, 302);
}
