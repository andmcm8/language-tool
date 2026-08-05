"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import { createWorker } from "tesseract.js";
import {
  Camera,
  RefreshCw,
  Upload,
  AlertCircle,
  RotateCcw,
  Image as ImageIcon,
} from "lucide-react";

interface CameraOcrTabProps {
  lang: "es" | "en";
}

interface TextRegion {
  original: string;
  translated: string;
  bbox: { x0: number; y0: number; x1: number; y1: number };
  confidence?: number;
}

/* ================================================================
   SAMPLE SIGNS — demo data so users can test without a camera
   ================================================================ */
const SAMPLE_SIGNS = [
  {
    id: "sign-1",
    label: "Deli Specials",
    lines: [
      { original: "DAILY SPECIAL", translated: "ESPECIAL DEL DÍA" },
      {
        original: "Hot Roast Beef Sandwich $10.99",
        translated: "Sándwich de Carne Asada Caliente $10.99",
      },
      {
        original: "Melted Swiss Cheese & Pickles",
        translated: "Queso Suizo Fundido y Pepinillos",
      },
    ],
  },
  {
    id: "sign-2",
    label: "Payment Notice",
    lines: [
      { original: "NOTICE", translated: "AVISO" },
      {
        original: "EBT Accepted For Groceries",
        translated: "Se Acepta EBT para Abarrotes",
      },
      {
        original: "Hot Food Requires Cash or Card",
        translated: "Comida Caliente Requiere Efectivo o Tarjeta",
      },
    ],
  },
  {
    id: "sign-3",
    label: "Bakery Hours",
    lines: [
      {
        original: "FRESH BREAD BAKED DAILY",
        translated: "PAN FRESCO HORNEADO DIARIAMENTE",
      },
      {
        original: "First Batch 6:30 AM",
        translated: "Primera Hornada 6:30 AM",
      },
      {
        original: "Second Batch 4:00 PM",
        translated: "Segunda Hornada 4:00 PM",
      },
    ],
  },
];

/* ================================================================
   IMAGE PREPROCESSING WITH ADAPTIVE THRESHOLDING
   Dramatically improves handwriting & pen stroke recognition
   ================================================================ */
function preprocessForOcr(srcCanvas: HTMLCanvasElement): HTMLCanvasElement {
  const w = srcCanvas.width;
  const h = srcCanvas.height;
  const ocrCanvas = document.createElement("canvas");
  ocrCanvas.width = w;
  ocrCanvas.height = h;
  const ctx = ocrCanvas.getContext("2d")!;
  ctx.drawImage(srcCanvas, 0, 0);

  const imageData = ctx.getImageData(0, 0, w, h);
  const d = imageData.data;

  // Step 1: Grayscale & Contrast boost
  let min = 255, max = 0;
  const grayBuf = new Uint8Array(w * h);

  for (let i = 0, j = 0; i < d.length; i += 4, j++) {
    const gray = Math.round(0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]);
    grayBuf[j] = gray;
    if (gray < min) min = gray;
    if (gray > max) max = gray;
  }

  const range = max - min || 1;

  // Step 2: Adaptive Local Thresholding (ideal for handwriting & shadow gradients)
  const windowSize = Math.max(15, Math.floor(Math.min(w, h) / 32));
  const halfWin = Math.floor(windowSize / 2);

  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const idx = y * w + x;
      const pixelIdx = idx * 4;

      // Stretch contrast
      const val = Math.round(((grayBuf[idx] - min) / range) * 255);

      // Simple local adaptive threshold
      let sum = 0;
      let count = 0;
      for (let wy = Math.max(0, y - halfWin); wy <= Math.min(h - 1, y + halfWin); wy += 4) {
        for (let wx = Math.max(0, x - halfWin); wx <= Math.min(w - 1, x + halfWin); wx += 4) {
          sum += grayBuf[wy * w + wx];
          count++;
        }
      }
      const localAvg = count > 0 ? sum / count : 128;
      const binarized = val < localAvg - 8 ? 0 : 255;

      d[pixelIdx] = d[pixelIdx + 1] = d[pixelIdx + 2] = binarized;
    }
  }

  ctx.putImageData(imageData, 0, 0);
  return ocrCanvas;
}

/* ================================================================
   OCR WORD CORRECTION WITH CONTEXT CLUES
   ================================================================ */
const KNOWN_WORDS = new Set([
  "daily","special","specials","fresh","hot","cold","warm","baked","fried",
  "grilled","roasted","roast","melted","steamed","homemade","handmade",
  "open","closed","hours","notice","warning","caution","welcome",
  "please","thank","parking","restroom","bathroom","employees","only",
  "push","pull","exit","entrance","sale","discount","price","free",
  "cash","card","credit","debit","accepted","required","payment",
  "delivery","pickup","order","menu","combo","meal","plate","serving",
  "bread","meat","chicken","beef","pork","fish","cheese","rice",
  "beans","eggs","milk","butter","cream","sugar","salt","sauce",
  "salad","soup","sandwich","burger","tacos","water","juice","coffee",
  "soda","beer","wine","drink","drinks","bakery","deli","grocery",
  "produce","dairy","frozen","canned","dry","snacks","candy","chips",
  "cookies","small","medium","large","extra","regular","double","half",
  "pound","dozen","each","per","included","includes","available",
  "limited","while","supplies","last","first","second","batch",
  "today","now","new","best","store","market","service","customer",
  "phone","call","information","help","floor","aisle",
  "organic","natural","gluten","spicy","sweet","delicious",
  "breakfast","lunch","dinner","appetizer","dessert","side",
  "monday","tuesday","wednesday","thursday","friday","saturday","sunday",
  "pharmacy","prescription","repair","warranty","screen","battery",
  "empanada","empanadas","arepa","plantain","plantains","tortilla",
  "avocado","tomato","onion","lettuce","pepper","corn","banana",
  "orange","lemon","lime","apple","mango","coconut","pineapple",
  "with","without","and","the","for","all","our","your","this","that",
]);

const OCR_SUBS: Record<string, string[]> = {
  "0": ["O","o"], "O": ["0"], "o": ["0"],
  "1": ["I","l","i"], "I": ["1","l"], "l": ["1","I","i"],
  "5": ["S","s"], "S": ["5"], "s": ["5"],
  "8": ["B"], "B": ["8"],
  "6": ["G","b"], "G": ["6"],
  "2": ["Z","z"], "Z": ["2"], "z": ["2"],
  "|": ["I","l","1"],
  "]": ["I","l"],
  "[": ["I","l"],
};

function correctOcrWord(word: string): string {
  const lower = word.toLowerCase().replace(/[^a-z]/g, "");
  if (lower.length < 2) return word;
  if (KNOWN_WORDS.has(lower)) return word;

  for (let pos = 0; pos < word.length; pos++) {
    const ch = word[pos];
    const subs = OCR_SUBS[ch];
    if (!subs) continue;
    for (const sub of subs) {
      const candidate = word.slice(0, pos) + sub + word.slice(pos + 1);
      const candidateLower = candidate.toLowerCase().replace(/[^a-z]/g, "");
      if (KNOWN_WORDS.has(candidateLower)) return candidate;
    }
  }

  return word;
}

function correctOcrLine(line: string): string {
  return line
    .split(/\s+/)
    .map((w) => correctOcrWord(w))
    .join(" ");
}

/* ================================================================
   COMPONENT
   ================================================================ */
export default function CameraOcrTab({ lang }: CameraOcrTabProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const srcCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const resultCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [cameraActive, setCameraActive] = useState(false);
  const [cameraBlocked, setCameraBlocked] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [hasResult, setHasResult] = useState(false);
  const [statusText, setStatusText] = useState("");

  /* ---------- Camera helpers ---------- */
  const startCamera = useCallback(async () => {
    setCameraBlocked(false);
    setHasResult(false);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "environment",
          width: { ideal: 1920 },
          height: { ideal: 1080 },
        },
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        setCameraActive(true);
      }
    } catch {
      setCameraBlocked(true);
      setCameraActive(false);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (videoRef.current?.srcObject) {
      (videoRef.current.srcObject as MediaStream)
        .getTracks()
        .forEach((t) => t.stop());
      videoRef.current.srcObject = null;
      setCameraActive(false);
    }
  }, []);

  useEffect(() => {
    startCamera();
    return () => stopCamera();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ---------- Gemini Vision OCR + Translation ---------- */
  const visionTranslate = async (
    base64: string
  ): Promise<{ original: string; translated: string }[]> => {
    try {
      const res = await fetch("/api/vision-translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imageBase64: base64 }),
      });
      const data = await res.json();
      return data.lines || [];
    } catch {
      return [];
    }
  };

  /* ---------- Fallback line-by-line translation ---------- */
  const translateLine = async (text: string): Promise<string> => {
    try {
      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      return data.translation || text;
    } catch {
      return text;
    }
  };

  /* ---------- Canvas colour helpers ---------- */
  const sampleBgColor = (
    ctx: CanvasRenderingContext2D,
    bbox: { x0: number; y0: number; x1: number; y1: number },
    w: number,
    h: number
  ): [number, number, number] => {
    const pad = 4;
    const pts: [number, number][] = [
      [Math.max(0, bbox.x0 - pad), bbox.y0],
      [Math.min(w - 1, bbox.x1 + pad), bbox.y0],
      [bbox.x0, Math.max(0, bbox.y0 - pad)],
      [bbox.x0, Math.min(h - 1, bbox.y1 + pad)],
      [Math.max(0, bbox.x0 - pad), Math.min(h - 1, bbox.y1 + pad)],
      [Math.min(w - 1, bbox.x1 + pad), Math.max(0, bbox.y0 - pad)],
      [Math.max(0, bbox.x0 - pad), (bbox.y0 + bbox.y1) / 2],
      [Math.min(w - 1, bbox.x1 + pad), (bbox.y0 + bbox.y1) / 2],
    ];

    let rSum = 0, gSum = 0, bSum = 0, count = 0;
    for (const [px, py] of pts) {
      try {
        const d = ctx.getImageData(Math.round(px), Math.round(py), 1, 1).data;
        rSum += d[0]; gSum += d[1]; bSum += d[2]; count++;
      } catch {}
    }

    if (count === 0) return [255, 255, 255];
    return [Math.round(rSum / count), Math.round(gSum / count), Math.round(bSum / count)];
  };

  const luminance = (r: number, g: number, b: number) =>
    (0.299 * r + 0.587 * g + 0.114 * b) / 255;

  /* ---------- Fuzzy string matching ---------- */
  const similarity = (a: string, b: string): number => {
    const wa = new Set(a.toLowerCase().split(/\s+/).filter(Boolean));
    const wb = new Set(b.toLowerCase().split(/\s+/).filter(Boolean));
    let inter = 0;
    wa.forEach((w) => { if (wb.has(w)) inter++; });
    const union = wa.size + wb.size - inter;
    return union === 0 ? 0 : inter / union;
  };

  /* ---------- De-overlap & Clean Bounding Boxes ---------- */
  const deoverlapAndCleanRegions = (
    regions: TextRegion[],
    imgW: number,
    imgH: number
  ): TextRegion[] => {
    if (regions.length === 0) return [];

    // 1. Filter out junk OCR noise, footers, phantom blank paper textboxes
    const clean = regions.filter((r) => {
      const orig = r.original.trim();
      const trans = r.translated.trim();
      if (!orig || !trans) return false;

      // Filter phantom tiny noise boxes (e.g. 1-2 character random symbols on blank paper)
      const boxW = r.bbox.x1 - r.bbox.x0;
      const boxH = r.bbox.y1 - r.bbox.y0;

      // Drop extremely small random noise blobs
      if (boxW < 18 || boxH < 10) return false;

      // Ignore page numbers / footers
      if (/^page\s+\d+$/i.test(orig) || /^revised:?\s*[\d\/]+$/i.test(orig)) return false;
      if (/^[\d\s\.\/\-\,\!\?\#\%\*\@]+$/.test(orig) && !orig.includes("$")) return false; // Ignore pure non-price numbers/symbols

      // Filter isolated 1 or 2 letter noise fragments unless it's a known valid word
      if (orig.length <= 2 && !orig.includes("$")) {
        const lower = orig.toLowerCase();
        if (!["no", "si", "in", "on", "at", "to", "or", "el", "la", "un"].includes(lower)) {
          return false;
        }
      }

      // Filter gibberish letter sequences
      const words = orig.split(/\s+/);
      const invalidWords = words.filter((w) => /^[^\w]+$/.test(w) || (w.length > 5 && !/[aeiouy]/i.test(w)));
      if (invalidWords.length > words.length / 2) return false;

      return true;
    });

    // 2. Sort regions top-to-bottom by y0 coordinate
    clean.sort((a, b) => a.bbox.y0 - b.bbox.y0);

    const result: TextRegion[] = [];

    for (const item of clean) {
      const b = { ...item.bbox };
      b.x0 = Math.max(0, b.x0);
      b.y0 = Math.max(0, b.y0);
      b.x1 = Math.min(imgW, b.x1);
      b.y1 = Math.min(imgH, b.y1);

      let isDuplicate = false;
      for (const existing of result) {
        const eb = existing.bbox;

        const overlapX = Math.max(0, Math.min(b.x1, eb.x1) - Math.max(b.x0, eb.x0));
        const overlapY = Math.max(0, Math.min(b.y1, eb.y1) - Math.max(b.y0, eb.y0));
        const overlapArea = overlapX * overlapY;
        const areaB = (b.x1 - b.x0) * (b.y1 - b.y0);

        if (areaB > 0 && overlapArea / areaB > 0.4) {
          isDuplicate = true;
          break;
        }

        if (b.x0 < eb.x1 && b.x1 > eb.x0 && b.y0 >= eb.y0 && b.y0 < eb.y1 + 4) {
          const height = b.y1 - b.y0;
          b.y0 = eb.y1 + 4;
          b.y1 = b.y0 + height;
        }
      }

      if (!isDuplicate && b.y1 <= imgH + 20) {
        result.push({ ...item, bbox: b });
      }
    }

    return result;
  };

  /* ---------- CORE: paint-over translation on canvas ---------- */
  const paintTranslation = (
    srcCanvas: HTMLCanvasElement,
    rawRegions: TextRegion[]
  ) => {
    const resCanvas = resultCanvasRef.current!;
    const w = srcCanvas.width;
    const h = srcCanvas.height;
    resCanvas.width = w;
    resCanvas.height = h;
    const ctx = resCanvas.getContext("2d")!;

    ctx.drawImage(srcCanvas, 0, 0);

    const regions = deoverlapAndCleanRegions(rawRegions, w, h);

    for (const region of regions) {
      const { bbox } = region;
      const padX = 4;
      const padY = 2;

      const boxW = Math.max(20, bbox.x1 - bbox.x0 + padX * 2);
      const boxH = Math.max(14, bbox.y1 - bbox.y0 + padY * 2);
      const x0 = Math.max(0, bbox.x0 - padX);
      const y0 = Math.max(0, bbox.y0 - padY);

      const [r, g, b] = sampleBgColor(ctx, bbox, w, h);
      const bgStr = `rgba(${r},${g},${b}, 0.95)`;
      const textColor = luminance(r, g, b) > 0.5 ? "#000000" : "#ffffff";

      ctx.fillStyle = bgStr;
      ctx.beginPath();
      if (typeof ctx.roundRect === "function") {
        ctx.roundRect(x0, y0, boxW, boxH, 4);
      } else {
        ctx.rect(x0, y0, boxW, boxH);
      }
      ctx.fill();

      let fontSize = Math.max(9, Math.min(boxH * 0.75, 48));
      ctx.font = `bold ${fontSize}px "Segoe UI", system-ui, -apple-system, sans-serif`;

      while (ctx.measureText(region.translated).width > boxW - 4 && fontSize > 8) {
        fontSize -= 0.5;
        ctx.font = `bold ${fontSize}px "Segoe UI", system-ui, -apple-system, sans-serif`;
      }

      ctx.fillStyle = textColor;
      ctx.textBaseline = "middle";
      ctx.textAlign = "left";
      const cy = y0 + boxH / 2;

      ctx.save();
      ctx.beginPath();
      ctx.rect(x0, y0, boxW, boxH);
      ctx.clip();
      ctx.fillText(region.translated, x0 + 2, cy, boxW - 4);
      ctx.restore();
    }
  };

  /* ================================================================
     MAIN PROCESSING PIPELINE
     ================================================================ */
  const processPhoto = async (imageSource?: string) => {
    setIsProcessing(true);
    setHasResult(false);
    setStatusText(lang === "es" ? "Capturando imagen…" : "Capturing image…");

    try {
      const srcCanvas = srcCanvasRef.current!;
      const srcCtx = srcCanvas.getContext("2d")!;
      let imgW: number, imgH: number;

      if (imageSource) {
        const img = new Image();
        img.crossOrigin = "anonymous";
        await new Promise<void>((resolve, reject) => {
          img.onload = () => resolve();
          img.onerror = reject;
          img.src = imageSource;
        });
        const scale = Math.min(1, 1280 / img.naturalWidth);
        imgW = Math.round(img.naturalWidth * scale);
        imgH = Math.round(img.naturalHeight * scale);
        srcCanvas.width = imgW;
        srcCanvas.height = imgH;
        srcCtx.drawImage(img, 0, 0, imgW, imgH);
      } else if (cameraActive && videoRef.current) {
        const v = videoRef.current;
        imgW = v.videoWidth || 640;
        imgH = v.videoHeight || 480;
        srcCanvas.width = imgW;
        srcCanvas.height = imgH;
        srcCtx.drawImage(v, 0, 0, imgW, imgH);
        stopCamera();
      } else {
        throw new Error("No image source available");
      }

      setStatusText(lang === "es" ? "Detectando texto…" : "Detecting text…");

      const ocrCanvas = preprocessForOcr(srcCanvas);

      const tesseractPromise = (async () => {
        try {
          const worker = await createWorker("eng");
          const ret = await worker.recognize(ocrCanvas);
          await worker.terminate();
          return ret.data.lines
            .filter((l) => l.text.trim().length > 1 && l.bbox)
            .map((l) => ({
              text: correctOcrLine(l.text.trim()),
              bbox: l.bbox,
              confidence: l.confidence,
            }));
        } catch {
          return [];
        }
      })();

      setStatusText(lang === "es" ? "Traduciendo…" : "Translating…");
      const base64 = srcCanvas.toDataURL("image/jpeg", 0.85);
      const [visionResults, tesseractLines] = await Promise.all([
        visionTranslate(base64),
        tesseractPromise,
      ]);

      let regions: TextRegion[] = [];

      if (tesseractLines.length > 0) {
        if (visionResults.length > 0) {
          const used = new Set<number>();

          for (const vr of visionResults) {
            let bestIdx = -1;
            let bestScore = 0;

            for (let i = 0; i < tesseractLines.length; i++) {
              if (used.has(i)) continue;
              const score = similarity(vr.original, tesseractLines[i].text);
              if (score > bestScore) {
                bestScore = score;
                bestIdx = i;
              }
            }

            if (bestIdx >= 0 && bestScore > 0.25) {
              used.add(bestIdx);
              regions.push({
                original: vr.original,
                translated: vr.translated,
                bbox: tesseractLines[bestIdx].bbox,
              });
            }
          }

          for (let i = 0; i < tesseractLines.length; i++) {
            if (!used.has(i) && tesseractLines[i].text.length > 2) {
              const tr = await translateLine(tesseractLines[i].text);
              regions.push({
                original: tesseractLines[i].text,
                translated: tr,
                bbox: tesseractLines[i].bbox,
              });
            }
          }
        } else {
          for (const line of tesseractLines) {
            if (line.text.length > 2) {
              const tr = await translateLine(line.text);
              regions.push({
                original: line.text,
                translated: tr,
                bbox: line.bbox,
              });
            }
          }
        }
      } else if (visionResults.length > 0) {
        const lineH = imgH / (visionResults.length + 1);
        visionResults.forEach((vr, i) => {
          regions.push({
            original: vr.original,
            translated: vr.translated,
            bbox: {
              x0: Math.round(imgW * 0.05),
              y0: Math.round(lineH * (i + 0.5)),
              x1: Math.round(imgW * 0.95),
              y1: Math.round(lineH * (i + 0.5) + lineH * 0.55),
            },
          });
        });
      }

      if (regions.length > 0) {
        setStatusText(lang === "es" ? "Renderizando…" : "Rendering…");
        paintTranslation(srcCanvas, regions);
      } else {
        const resCanvas = resultCanvasRef.current!;
        resCanvas.width = imgW;
        resCanvas.height = imgH;
        resCanvas.getContext("2d")!.drawImage(srcCanvas, 0, 0);
      }

      setHasResult(true);
      setIsProcessing(false);
      setStatusText("");
    } catch (err) {
      console.error("processPhoto error:", err);
      setIsProcessing(false);
      setStatusText(lang === "es" ? "Error procesando imagen" : "Error processing image");
    }
  };

  const processSampleSign = (
    signLines: { original: string; translated: string }[]
  ) => {
    setIsProcessing(true);
    setHasResult(false);

    const srcCanvas = srcCanvasRef.current!;
    const w = 640;
    const h = 400;
    srcCanvas.width = w;
    srcCanvas.height = h;
    const ctx = srcCanvas.getContext("2d")!;

    ctx.fillStyle = "#faf8f0";
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = "#c8b888";
    ctx.lineWidth = 6;
    ctx.strokeRect(12, 12, w - 24, h - 24);

    const lineH = h / (signLines.length + 1);
    const regions: TextRegion[] = [];

    signLines.forEach((line, i) => {
      const isTitle = i === 0;
      const fontSize = isTitle ? 32 : 22;
      ctx.font = `bold ${fontSize}px "Segoe UI", system-ui, sans-serif`;
      ctx.fillStyle = "#1a1a1a";
      ctx.textBaseline = "middle";
      const cy = lineH * (i + 1);

      const measured = ctx.measureText(line.original);
      const textW = measured.width;
      const x = (w - textW) / 2;

      ctx.fillText(line.original, x, cy);

      regions.push({
        original: line.original,
        translated: line.translated,
        bbox: {
          x0: Math.round(x - 6),
          y0: Math.round(cy - fontSize * 0.6),
          x1: Math.round(x + textW + 6),
          y1: Math.round(cy + fontSize * 0.6),
        },
      });
    });

    paintTranslation(srcCanvas, regions);
    setHasResult(true);
    setIsProcessing(false);
  };

  const handlePhotoCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const result = ev.target?.result as string;
      if (result) {
        if (cameraActive) stopCamera();
        processPhoto(result);
      }
    };
    reader.readAsDataURL(file);
    e.target.value = "";
  };

  const resetView = () => {
    setHasResult(false);
    setStatusText("");
    startCamera();
  };

  return (
    <div className="w-full max-w-md mx-auto p-3 pb-24 flex flex-col gap-2.5">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handlePhotoCapture}
        accept="image/*"
        capture="environment"
        className="hidden"
      />
      <canvas ref={srcCanvasRef} className="hidden" />

      {/* TALLER VIEWPORT MATCHING PORTRAIT PHONES PERFECTLY */}
      <div className="relative w-full aspect-[3/4] rounded-2xl overflow-hidden bg-black shadow-lg border border-white/10">
        <video
          ref={videoRef}
          playsInline
          muted
          className={`w-full h-full object-cover ${
            cameraActive && !hasResult ? "" : "hidden"
          }`}
        />

        <canvas
          ref={resultCanvasRef}
          className={`w-full h-full object-cover bg-slate-900 ${
            hasResult ? "" : "hidden"
          }`}
        />

        {!cameraActive && !hasResult && !isProcessing && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-white bg-slate-900 p-4">
            {cameraBlocked ? (
              <>
                <AlertCircle className="w-8 h-8 text-amber-400 mb-2" />
                <p className="text-xs font-bold text-center">
                  {lang === "es"
                    ? "Cámara requiere HTTPS. Use el botón para subir foto."
                    : "Live camera requires HTTPS. Use the button to upload a photo."}
                </p>
              </>
            ) : (
              <>
                <Camera className="w-8 h-8 text-primary animate-pulse mb-1" />
                <p className="text-xs font-bold">
                  {lang === "es" ? "Iniciando cámara…" : "Starting camera…"}
                </p>
              </>
            )}
          </div>
        )}

        {cameraActive && !hasResult && !isProcessing && (
          <div className="absolute inset-4 border-2 border-dashed border-white/50 rounded-xl pointer-events-none flex items-end justify-center pb-3">
            <span className="px-3.5 py-1.5 rounded-full bg-black/65 text-white text-xs font-semibold backdrop-blur-sm shadow-sm">
              {lang === "es"
                ? "Apunte al letrero o texto → Toque Traducir"
                : "Point at sign or text → Tap Translate"}
            </span>
          </div>
        )}

        {isProcessing && (
          <div className="absolute inset-0 bg-black/75 backdrop-blur-sm flex flex-col items-center justify-center text-white z-30">
            <RefreshCw className="w-8 h-8 text-primary animate-spin mb-2" />
            <span className="text-xs font-bold">{statusText}</span>
          </div>
        )}
      </div>

      {/* ACTION BUTTONS */}
      <div className="grid grid-cols-2 gap-2">
        {hasResult ? (
          <>
            <button
              onClick={resetView}
              className="py-3 bg-surface border border-secondary-fixed text-on-surface font-bold text-xs rounded-2xl flex items-center justify-center gap-1.5 transition-all hover:bg-surface-container"
            >
              <RotateCcw className="w-4 h-4 text-primary" />
              <span>{lang === "es" ? "Nueva Foto" : "New Photo"}</span>
            </button>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="py-3 bg-primary text-white font-extrabold text-xs rounded-2xl flex items-center justify-center gap-1.5 shadow-md transition-all hover:brightness-110"
            >
              <Upload className="w-4 h-4" />
              <span>{lang === "es" ? "Subir Otra" : "Upload Another"}</span>
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="py-3 bg-surface border border-secondary-fixed text-on-surface font-bold text-xs rounded-2xl flex items-center justify-center gap-1.5 transition-all hover:bg-surface-container"
            >
              <Upload className="w-4 h-4 text-primary" />
              <span>{lang === "es" ? "Subir Foto" : "Upload Photo"}</span>
            </button>
            <button
              onClick={() => processPhoto()}
              disabled={isProcessing || (!cameraActive && !cameraBlocked)}
              className="py-3 bg-primary text-white font-extrabold text-xs rounded-2xl disabled:opacity-50 flex items-center justify-center gap-1.5 shadow-md transition-all hover:brightness-110"
            >
              <Camera className="w-4 h-4" />
              <span>{lang === "es" ? "Traducir" : "Translate"}</span>
            </button>
          </>
        )}
      </div>

      {/* SAMPLE SIGN PRESETS */}
      <div className="space-y-1 pt-0.5">
        <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider px-1 flex items-center gap-1">
          <ImageIcon className="w-3 h-3 text-primary" />
          <span>
            {lang === "es" ? "Probar letreros de ejemplo:" : "Try sample signs:"}
          </span>
        </div>
        <div className="grid grid-cols-3 gap-1.5">
          {SAMPLE_SIGNS.map((sign) => (
            <button
              key={sign.id}
              onClick={() => {
                if (cameraActive) stopCamera();
                processSampleSign(sign.lines);
              }}
              className="p-2 bg-surface border border-secondary-fixed hover:bg-surface-container rounded-xl text-center transition-all"
            >
              <div className="text-[10px] font-extrabold text-primary truncate">
                {sign.label}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
