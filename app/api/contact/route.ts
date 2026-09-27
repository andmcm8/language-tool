import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { placeName, placeId, contactInfo, message } = body;

    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      placeName: placeName || "Unknown",
      placeId: placeId || "unknown",
      contactInfo: contactInfo || "",
      message: message || "",
    };

    console.log("📨 [CONTACT REQUEST RECEIVED]:", JSON.stringify(logEntry));

    // Append to local requests log file
    try {
      const logDir = path.join(process.cwd(), "data");
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      const logFile = path.join(logDir, "contact_requests.jsonl");
      fs.appendFileSync(logFile, JSON.stringify(logEntry) + "\n", "utf-8");
    } catch (fsErr) {
      console.error("Failed to write to contact log file:", fsErr);
    }

    return NextResponse.json({
      success: true,
      message: "Request received successfully. We will follow up shortly!",
    });
  } catch (error: any) {
    console.error("Contact API error:", error?.message);
    return NextResponse.json(
      { success: false, error: "Failed to process request" },
      { status: 500 }
    );
  }
}
