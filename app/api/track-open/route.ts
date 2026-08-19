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
  private_key_id: "d202fe495f732159ba815f9d06e2c400186e0eab",
  private_key: "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvk7amJ8GCX0me\nnsyHSQVkPST5BTybi987wnu8JCtk+cPHCEs4dFgiByY9El2A5shU6mEtWCqMyba7\nsb3oNoeR4jQvMZSZDBRqskXAVZ8as0FGqgU96+LPYjVVnKNDbTK5MKlQqfj9YVrA\n5jqSXMwwbv8gEZJDluWleVSnDaR2Ma39fi2TkJI33BqtIjyMC4MGQqKBJmlBMwcl\n9itPlVl4vq6nAb/3ZW1yDkoZ93M3UjLt+Oe8TTOA0XKS4HNIx5fEGoB/qj7Bf8Ze\n59PROBCY4SIDAdml3EpruiqLBHPP1/YTMPEWDt6xN41B7r/b3NZMz5EGkIoX1G/+\nIVSwIj2bAgMBAAECggEACgx2CX1rVacBeNAVhu/2xzK5Vn07vO/yQffStW+2ghbK\nDdlGK4AmeSVtRVUzP8jgPKfrZuPNukq4fXaMlr6O32+8VS/NFZNQ6dMJK0Wwj5/P\nGRhq/g0YPo6cMdRUrcERWZ2qMGvXTHJ8ILUsiKrspCBTfrDdbPvfvyrksujqJDos\nYhcBTbTV5lbpqPZCAojd2kYopjmsme7NfKy7raivPnKLuuhHe79XbVhC4b0f1geu\nM/4PJsUZmBfpuvH0P7tA43NTReVyxj/aecYiujK7tHUUkd2xiLr8bXBUZrIK4Uml\nqQsSKkrD1OzCMNm6Jx37u7EhSmQFPp8c747Uy6+2eQKBgQDa+YZeBmp2xdt1Q03L\nSoqTp2De+yFzx63wXvzYe9+3fE+iMplj1/WF4x+z2HYQeq3fyEKNIDzoYTgH74rK\nnclS3oh0SppUsuL6hhKyQPjYKnf52jPYcRoqSZdjvxI1uchf6QP1aC+UJLFKU4CX\ngnzPCg+eFe8NZDh1g6EKr600owKBgQDNQ7A7y5EVjWgsHcTn3k77jigaJ2l+afzj\nH6+TkibkMUCF7D7KcCr4UA861T8qThuCl9KCXc0WHOoLhDja18cF0YYrBOJeFR8s\n5z+u2BKue2Spa4Z75LKqypjc0UMpMKeEmYj15gZ1iM9Z1Wv2Q1230L64viYi09KE\n0vK+1fVqqQKBgCYj5iKEbZDIf6QaF/e7wQ1czwOnrDj1Y7eFY/b1BI96CIjQ1WTN\nncc3OzNhFZdjNtvOjsD0B4fWPyMqtvr5prJXbl8LC3yLN/u41JLVvEIyi3kqZ3Ng\np9ULwmGuSyaueFc0R+s7vWXJSlQO3UwGf2S0dOntGhk0Bp15UtiApuOPAoGAUXFA\n9IixmR6RLafmH6W6Kt9dk/r9RXYiK6+/x0qe+b18/2YcB9B3jCyfzlUcCdoR2kAI\n+0bif5qbVlRxBovE4M8gb+MxOekhhHyAbQw4ZVh6OSp7op68MT3PZxX0ktxGKzuL\n9xz8hRfyRY+DlaNnBO7jLYPst7bZ+W+FdyiHhnkCgYAy2ICTrqRTZzSeE6d6+iKK\n3qejjMiGtuXj64Ur7O5nRALKut+FQHwpcLBM3Qo/5fQYewlZzAWZ2qqypbrrSjGQ\nVJwGuxKDCFOisHWl2hE+C+fC1gWSRZ7nplpc+c2NKZl+iCbO2YimVHDrReBh67pN\niemPGQBepmj8WGacsGZYvQ==\n-----END PRIVATE KEY-----\n",
  client_email: "duotaps@alconio.iam.gserviceaccount.com",
  client_id: "106794621529861444597",
};

async function logOpenToSheet(email: string, biz: string) {
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
    const openValue = `YES (${timestamp})`;

    if (targetRowIndex > 0) {
      await sheets.spreadsheets.values.update({
        spreadsheetId,
        range: `Sheet1!H${targetRowIndex}`,
        valueInputOption: "USER_ENTERED",
        requestBody: { values: [[openValue]] },
      });
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
    await logOpenToSheet(email, biz);
  }

  return new Response(GIF_BYTES, {
    status: 200,
    headers: {
      "Content-Type": "image/gif",
      "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
      "Pragma": "no-cache",
      "Expires": "0",
    },
  });
}
