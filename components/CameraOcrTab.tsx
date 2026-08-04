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
   COMPONENT
   ================================================================ */
/* ================================================================
   IMAGE PREPROCESSING — dramatically improves Tesseract accuracy
   ================================================================ */
function preprocessForOcr(
  srcCanvas: HTMLCanvasElement
): HTMLCanvasElement {
  const w = srcCanvas.width;
  const h = srcCanvas.height;
  const ocrCanvas = document.createElement("canvas");
  ocrCanvas.width = w;
  ocrCanvas.height = h;
  const ctx = ocrCanvas.getContext("2d")!;
  ctx.drawImage(srcCanvas, 0, 0);

  const imageData = ctx.getImageData(0, 0, w, h);
  const d = imageData.data;

  // Step 1: Grayscale
  for (let i = 0; i < d.length; i += 4) {
    const gray = Math.round(0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]);
    d[i] = d[i + 1] = d[i + 2] = gray;
  }

  // Step 2: Contrast stretch (histogram stretch to 0–255)
  let min = 255,
    max = 0;
  for (let i = 0; i < d.length; i += 4) {
    if (d[i] < min) min = d[i];
    if (d[i] > max) max = d[i];
  }
  const range = max - min || 1;
  for (let i = 0; i < d.length; i += 4) {
    const stretched = Math.round(((d[i] - min) / range) * 255);
    d[i] = d[i + 1] = d[i + 2] = stretched;
  }

  // Step 3: Otsu threshold for binarisation
  const histogram = new Array(256).fill(0);
  const total = w * h;
  for (let i = 0; i < d.length; i += 4) histogram[d[i]]++;
  let sumAll = 0;
  for (let i = 0; i < 256; i++) sumAll += i * histogram[i];
  let sumB = 0,
    wB = 0,
    bestVariance = 0,
    threshold = 128;
  for (let t = 0; t < 256; t++) {
    wB += histogram[t];
    if (wB === 0) continue;
    const wF = total - wB;
    if (wF === 0) break;
    sumB += t * histogram[t];
    const mB = sumB / wB;
    const mF = (sumAll - sumB) / wF;
    const variance = wB * wF * (mB - mF) * (mB - mF);
    if (variance > bestVariance) {
      bestVariance = variance;
      threshold = t;
    }
  }
  for (let i = 0; i < d.length; i += 4) {
    const val = d[i] > threshold ? 255 : 0;
    d[i] = d[i + 1] = d[i + 2] = val;
  }

  ctx.putImageData(imageData, 0, 0);
  return ocrCanvas;
}

/* ================================================================
   OCR WORD CORRECTION — fixes common Tesseract misreads using
   context clues (dictionary look-up with letter substitution)
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
  "produce","dairy","frozen","snacks","candy","chips","cookies",
  "small","medium","large","extra","regular","double","half",
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

// Common OCR character confusions
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
  "{": ["("], "}": [")"],
};

function correctOcrWord(word: string): string {
  const lower = word.toLowerCase().replace(/[^a-z]/g, "");
  if (lower.length < 2) return word;
  if (KNOWN_WORDS.has(lower)) return word; // Already correct

  // Try single-character substitutions
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

  return word; // No correction found, return as-is
}

function correctOcrLine(line: string): string {
  return line
    .split(/\s+/)
    .map((w) => correctOcrWord(w))
    .join(" ");
}

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
    // Sample a ring of pixels just outside the bounding box
    const pad = 4;
    const pts: [number, number][] = [
      [Math.max(0, bbox.x0 - pad), bbox.y0],
      [Math.min(w - 1, bbox.x1 + pad), bbox.y0],
      [bbox.x0, Math.max(0, bbox.y0 - pad)],
      [bbox.x0, Math.min(h - 1, bbox.y1 + pad)],
      [Math.max(0, bbox.x0 - pad), Math.min(h - 1, bbox.y1 + pad)],
      [Math.min(w - 1, bbox.x1 + pad), Math.max(0, bbox.y0 - pad)],
      // also sample the midpoints of each edge
      [Math.max(0, bbox.x0 - pad), (bbox.y0 + bbox.y1) / 2],
      [Math.min(w - 1, bbox.x1 + pad), (bbox.y0 + bbox.y1) / 2],
    ];

    let rSum = 0,
      gSum = 0,
      bSum = 0,
      count = 0;
    for (const [px, py] of pts) {
      try {
        const d = ctx.getImageData(
          Math.round(px),
          Math.round(py),
          1,
          1
        ).data;
        rSum += d[0];
        gSum += d[1];
        bSum += d[2];
        count++;
      } catch {
        /* out of bounds */
      }
    }

    if (count === 0) return [255, 255, 255];
    return [
      Math.round(rSum / count),
      Math.round(gSum / count),
      Math.round(bSum / count),
    ];
  };

  const luminance = (r: number, g: number, b: number) =>
    (0.299 * r + 0.587 * g + 0.114 * b) / 255;

  /* ---------- Fuzzy string matching ---------- */
  const similarity = (a: string, b: string): number => {
    const wa = new Set(a.toLowerCase().split(/\s+/).filter(Boolean));
    const wb = new Set(b.toLowerCase().split(/\s+/).filter(Boolean));
    let inter = 0;
    wa.forEach((w) => {
      if (wb.has(w)) inter++;
    });
    const union = wa.size + wb.size - inter;
    return union === 0 ? 0 : inter / union;
  };

  /* ---------- CORE: paint-over translation on canvas ---------- */
  const paintTranslation = (
    srcCanvas: HTMLCanvasElement,
    regions: TextRegion[]
  ) => {
    const resCanvas = resultCanvasRef.current!;
    const w = srcCanvas.width;
    const h = srcCanvas.height;
    resCanvas.width = w;
    resCanvas.height = h;
    const ctx = resCanvas.getContext("2d")!;

    // Draw original image
    ctx.drawImage(srcCanvas, 0, 0);

    for (const region of regions) {
      const { bbox } = region;
      const pad = 3;

      // 1) Sample background colour
      const [r, g, b] = sampleBgColor(ctx, bbox, w, h);
      const bgStr = `rgb(${r},${g},${b})`;
      const textColor = luminance(r, g, b) > 0.5 ? "#111111" : "#f5f5f5";

      // 2) Paint over the original text with bg colour
      ctx.fillStyle = bgStr;
      ctx.fillRect(
        bbox.x0 - pad,
        bbox.y0 - pad,
        bbox.x1 - bbox.x0 + pad * 2,
        bbox.y1 - bbox.y0 + pad * 2
      );

      // 3) Size the translated text to fit the bounding box
      const boxW = bbox.x1 - bbox.x0 + pad * 2;
      const boxH = bbox.y1 - bbox.y0;
      let fontSize = Math.max(10, Math.min(boxH * 0.78, 56));
      ctx.font = `bold ${fontSize}px "Segoe UI", system-ui, -apple-system, sans-serif`;

      // Shrink until text fits the width
      while (
        ctx.measureText(region.translated).width > boxW &&
        fontSize > 8
      ) {
        fontSize -= 0.5;
        ctx.font = `bold ${fontSize}px "Segoe UI", system-ui, -apple-system, sans-serif`;
      }

      // 4) Draw the translated text
      ctx.fillStyle = textColor;
      ctx.textBaseline = "middle";
      const cy = (bbox.y0 + bbox.y1) / 2;
      ctx.fillText(region.translated, bbox.x0, cy, boxW);
    }
  };

  /* ================================================================
     MAIN PROCESSING PIPELINE
     ================================================================ */
  const processPhoto = async (imageSource?: string) => {
    setIsProcessing(true);
    setHasResult(false);
    setStatusText(
      lang === "es" ? "Capturando imagen…" : "Capturing image…"
    );

    try {
      const srcCanvas = srcCanvasRef.current!;
      const srcCtx = srcCanvas.getContext("2d")!;
      let imgW: number, imgH: number;

      /* ---- Load image onto source canvas ---- */
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

      /* ---- Step 1: Preprocess image + Tesseract OCR ---- */
      setStatusText(
        lang === "es" ? "Detectando texto…" : "Detecting text…"
      );

      // Create a preprocessed canvas (grayscale → contrast → binarise)
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
            }));
        } catch {
          return [];
        }
      })();

      /* ---- Step 2: Gemini Vision for accurate OCR + translation ---- */
      setStatusText(
        lang === "es" ? "Traduciendo con AI…" : "AI translating…"
      );
      const base64 = srcCanvas.toDataURL("image/jpeg", 0.85);
      const [visionResults, tesseractLines] = await Promise.all([
        visionTranslate(base64),
        tesseractPromise,
      ]);

      /* ---- Step 3: Match & merge into TextRegion[] ---- */
      let regions: TextRegion[] = [];

      if (tesseractLines.length > 0) {
        if (visionResults.length > 0) {
          // Match Gemini translations to Tesseract bounding boxes
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

          // Any remaining Tesseract lines → translate individually
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
          // Tesseract only (Gemini failed or returned empty)
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
        // Vision only — no bounding boxes; distribute evenly over image
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

      /* ---- Step 4: Paint the Google-Translate effect ---- */
      if (regions.length > 0) {
        setStatusText(
          lang === "es" ? "Renderizando…" : "Rendering…"
        );
        paintTranslation(srcCanvas, regions);
      } else {
        // No text found — just show the original photo
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
      setStatusText(
        lang === "es" ? "Error procesando imagen" : "Error processing image"
      );
    }
  };

  /* ---------- Demo sample sign (renders on canvas without real image) ---------- */
  const processSampleSign = (
    signLines: { original: string; translated: string }[]
  ) => {
    setIsProcessing(true);
    setHasResult(false);

    // Generate a fake "sign" image on the source canvas
    const srcCanvas = srcCanvasRef.current!;
    const w = 640;
    const h = 400;
    srcCanvas.width = w;
    srcCanvas.height = h;
    const ctx = srcCanvas.getContext("2d")!;

    // Draw a sign-like background
    ctx.fillStyle = "#faf8f0";
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = "#c8b888";
    ctx.lineWidth = 6;
    ctx.strokeRect(12, 12, w - 24, h - 24);

    // Draw each English text line
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

    // Now paint the translation over it
    paintTranslation(srcCanvas, regions);
    setHasResult(true);
    setIsProcessing(false);
  };

  /* ---------- File / camera upload ---------- */
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
    // Reset so user can re-select same file
    e.target.value = "";
  };

  /* ---------- Reset ---------- */
  const resetView = () => {
    setHasResult(false);
    setStatusText("");
    startCamera();
  };

  /* ================================================================
     RENDER
     ================================================================ */
  return (
    <div className="w-full max-w-md mx-auto p-3 pb-24 flex flex-col gap-2.5">
      {/* Hidden file input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handlePhotoCapture}
        accept="image/*"
        capture="environment"
        className="hidden"
      />
      {/* Hidden source canvas */}
      <canvas ref={srcCanvasRef} className="hidden" />

      {/* ---- MAIN VIEWPORT ---- */}
      <div className="relative w-full aspect-[4/3] rounded-2xl overflow-hidden bg-black shadow-lg border border-white/10">
        {/* Live camera */}
        <video
          ref={videoRef}
          playsInline
          muted
          className={`w-full h-full object-cover ${
            cameraActive && !hasResult ? "" : "hidden"
          }`}
        />

        {/* Result canvas — the Google-Translate-style output */}
        <canvas
          ref={resultCanvasRef}
          className={`w-full h-full object-contain bg-slate-900 ${
            hasResult ? "" : "hidden"
          }`}
        />

        {/* Camera blocked / loading states */}
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
                  {lang === "es"
                    ? "Iniciando cámara…"
                    : "Starting camera…"}
                </p>
              </>
            )}
          </div>
        )}

        {/* Viewfinder reticle */}
        {cameraActive && !hasResult && !isProcessing && (
          <div className="absolute inset-3 border-2 border-dashed border-white/50 rounded-xl pointer-events-none flex items-end justify-center pb-2">
            <span className="px-3 py-1 rounded-full bg-black/60 text-white text-[10px] font-semibold backdrop-blur-sm">
              {lang === "es"
                ? "Apunte al letrero → Toque Traducir"
                : "Point at sign → Tap Translate"}
            </span>
          </div>
        )}

        {/* Processing overlay */}
        {isProcessing && (
          <div className="absolute inset-0 bg-black/75 backdrop-blur-sm flex flex-col items-center justify-center text-white z-30">
            <RefreshCw className="w-8 h-8 text-primary animate-spin mb-2" />
            <span className="text-xs font-bold">{statusText}</span>
          </div>
        )}
      </div>

      {/* ---- ACTION BUTTONS ---- */}
      <div className="grid grid-cols-2 gap-2">
        {hasResult ? (
          <>
            <button
              onClick={resetView}
              className="py-3 bg-surface border border-secondary-fixed text-on-surface font-bold text-xs rounded-2xl flex items-center justify-center gap-1.5 transition-all hover:bg-surface-container"
            >
              <RotateCcw className="w-4 h-4 text-primary" />
              <span>
                {lang === "es" ? "Nueva Foto" : "New Photo"}
              </span>
            </button>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="py-3 bg-primary text-white font-extrabold text-xs rounded-2xl flex items-center justify-center gap-1.5 shadow-md transition-all hover:brightness-110"
            >
              <Upload className="w-4 h-4" />
              <span>
                {lang === "es" ? "Subir Otra" : "Upload Another"}
              </span>
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="py-3 bg-surface border border-secondary-fixed text-on-surface font-bold text-xs rounded-2xl flex items-center justify-center gap-1.5 transition-all hover:bg-surface-container"
            >
              <Upload className="w-4 h-4 text-primary" />
              <span>
                {lang === "es" ? "Subir Foto" : "Upload Photo"}
              </span>
            </button>
            <button
              onClick={() => processPhoto()}
              disabled={isProcessing || (!cameraActive && !cameraBlocked)}
              className="py-3 bg-primary text-white font-extrabold text-xs rounded-2xl disabled:opacity-50 flex items-center justify-center gap-1.5 shadow-md transition-all hover:brightness-110"
            >
              <Camera className="w-4 h-4" />
              <span>
                {lang === "es" ? "Traducir" : "Translate"}
              </span>
            </button>
          </>
        )}
      </div>

      {/* ---- SAMPLE SIGN PRESETS ---- */}
      <div className="space-y-1 pt-0.5">
        <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider px-1 flex items-center gap-1">
          <ImageIcon className="w-3 h-3 text-primary" />
          <span>
            {lang === "es"
              ? "Probar letreros de ejemplo:"
              : "Try sample signs:"}
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
