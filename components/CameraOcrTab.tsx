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
  Copy,
  Check,
  Volume2,
  Eye,
  EyeOff,
  Zap,
  ZoomIn,
  ArrowRightLeft,
  SunMedium,
  Scan,
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
   IMAGE PREPROCESSING WITH ADAPTIVE LOCAL THRESHOLDING
   ================================================================ */
function preprocessForOcr(srcCanvas: HTMLCanvasElement, contrastBoost: boolean = false): HTMLCanvasElement {
  const w = srcCanvas.width;
  const h = srcCanvas.height;
  const ocrCanvas = document.createElement("canvas");
  ocrCanvas.width = w;
  ocrCanvas.height = h;
  const ctx = ocrCanvas.getContext("2d")!;
  ctx.drawImage(srcCanvas, 0, 0);

  const imageData = ctx.getImageData(0, 0, w, h);
  const d = imageData.data;

  let min = 255, max = 0;
  const grayBuf = new Uint8Array(w * h);

  for (let i = 0, j = 0; i < d.length; i += 4, j++) {
    const gray = Math.round(0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]);
    grayBuf[j] = gray;
    if (gray < min) min = gray;
    if (gray > max) max = gray;
  }

  const range = max - min || 1;
  const windowSize = Math.max(15, Math.floor(Math.min(w, h) / 32));
  const halfWin = Math.floor(windowSize / 2);
  const thresholdDelta = contrastBoost ? 14 : 8;

  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const idx = y * w + x;
      const pixelIdx = idx * 4;

      const val = Math.round(((grayBuf[idx] - min) / range) * 255);

      let sum = 0;
      let count = 0;
      for (let wy = Math.max(0, y - halfWin); wy <= Math.min(h - 1, y + halfWin); wy += 4) {
        for (let wx = Math.max(0, x - halfWin); wx <= Math.min(w - 1, x + halfWin); wx += 4) {
          sum += grayBuf[wy * w + wx];
          count++;
        }
      }
      const localAvg = count > 0 ? sum / count : 128;
      const binarized = val < localAvg - thresholdDelta ? 0 : 255;

      d[pixelIdx] = d[pixelIdx + 1] = d[pixelIdx + 2] = binarized;
    }
  }

  ctx.putImageData(imageData, 0, 0);
  return ocrCanvas;
}

/* ================================================================
   LEVENSHTEIN EDIT DISTANCE ENGINE
   ================================================================ */
function levenshteinDistance(a: string, b: string): number {
  if (a === b) return 0;
  if (a.length === 0) return b.length;
  if (b.length === 0) return a.length;

  const matrix: number[][] = [];
  for (let i = 0; i <= b.length; i++) matrix[i] = [i];
  for (let j = 0; j <= a.length; j++) matrix[0][j] = j;

  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }
  return matrix[b.length][a.length];
}

const CONTEXT_PAIRS: [string, string][] = [
  ["spaghetti", "meatballs"],
  ["spaghetti", "meatball"],
  ["macaroni", "cheese"],
  ["garlic", "bread"],
  ["garlic", "knots"],
  ["chips", "salsa"],
  ["chips", "guacamole"],
  ["tacos", "salsa"],
  ["tacos", "guacamole"],
  ["empanadas", "beef"],
  ["empanadas", "chicken"],
  ["bandeja", "paisa"],
  ["pan", "bono"],
  ["tres", "leches"],
  ["flan", "leche"],
  ["fish", "chips"],
  ["rice", "beans"],
  ["ham", "cheese"],
  ["bread", "butter"],
  ["bacon", "eggs"],
  ["peanut", "butter"],
  ["burger", "fries"],
  ["chicken", "wings"],
  ["chicken", "tenders"],
  ["chicken", "nuggets"],
  ["chicken", "waffles"],
  ["chicken", "soup"],
  ["pork", "chops"],
  ["pork", "belly"],
  ["sweet", "plantains"],
  ["green", "plantains"],
  ["mashed", "potatoes"],
  ["potato", "salad"],
  ["macaroni", "salad"],
  ["caesar", "salad"],
  ["greek", "salad"],
  ["clam", "chowder"],
  ["lobster", "roll"],
  ["crab", "cakes"],
  ["shrimp", "cocktail"],
  ["apple", "pie"],
  ["chocolate", "cake"],
  ["ice", "cream"],
  ["iced", "tea"],
  ["iced", "coffee"],
  ["prescription", "refill"],
  ["prescription", "transfer"],
  ["screen", "repair"],
  ["screen", "replacement"],
  ["battery", "replacement"],
  ["oil", "change"],
  ["car", "wash"],
  ["dry", "cleaning"],
  ["express", "checkout"],
  ["customer", "service"],
  ["fitting", "room"],
  ["gift", "card"],
  ["wheelchair", "accessible"],
];

const KNOWN_WORDS = new Set([
  "spaghetti","meatballs","meatball","lasagna","ravioli","fettuccine","penne",
  "macaroni","noodle","noodles","marinara","alfredo","parmesan","mozzarella",
  "linguine","ziti","bolognese","carbonara","tortellini","gnocchi","pesto",
  "ricotta","provolone","calzone","pizza","pasta","garlic","knots","knot",
  "taco","tacos","burrito","burritos","quesadilla","quesadillas","empanada",
  "empanadas","arepa","arepas","tamal","tamales","tortilla","tortillas",
  "guacamole","salsa","totopos","nachos","ceviche","paella","sancocho",
  "pupusa","pupusas","churros","flan","tostones","maduros","chicharron",
  "chorizo","carnitas","barbacoa","birria","pastor","asada","mofongo",
  "horchata","jamaica","tamarindo",
  "burger","cheeseburger","fries","tenders","nuggets","wings","sauce",
  "bbq","buffalo","ribs","chops","tenderloin","sirloin","brisket",
  "lobster","crab","shrimp","calamari","clam","chowder","salmon","tuna",
  "cod","catfish","oysters","mussels","cocktail",
  "pancakes","waffles","toast","bagel","croissant","donut","muffin",
  "cookies","pastry","cake","pie","brownie","cupcake","bacon","sausage",
  "ham","omelet","omelette","syrup",
  "daily","special","specials","fresh","hot","cold","warm","baked","fried",
  "grilled","roasted","roast","melted","steamed","homemade","handmade",
  "open","closed","hours","notice","warning","caution","welcome",
  "please","thank","parking","restroom","bathroom","employees","only",
  "push","pull","exit","entrance","sale","discount","price","free",
  "cash","card","credit","debit","accepted","required","payment",
  "delivery","pickup","order","menu","combo","meal","plate","serving",
  "bread","meat","chicken","beef","pork","fish","cheese","rice",
  "beans","eggs","milk","butter","cream","sugar","salt",
  "salad","soup","sandwich","water","juice","coffee","espresso",
  "latte","cappuccino","soda","beer","wine","drink","drinks","bakery","deli",
  "grocery","produce","dairy","frozen","canned","dry","snacks","candy","chips",
  "small","medium","large","extra","regular","double","half",
  "pound","dozen","each","per","included","includes","available",
  "limited","while","supplies","last","first","second","batch",
  "today","now","new","best","store","market","service","customer",
  "phone","call","information","help","floor","aisle",
  "organic","natural","gluten","spicy","sweet","delicious",
  "breakfast","lunch","dinner","appetizer","dessert","side",
  "monday","tuesday","wednesday","thursday","friday","saturday","sunday",
  "pharmacy","prescription","repair","warranty","screen","battery",
  "plantain","plantains","avocado","tomato","onion","lettuce","pepper","corn","banana",
  "orange","lemon","lime","apple","mango","coconut","pineapple",
  "with","without","and","the","for","all","our","your","this","that",
  "refill","transfer","replacement","oil","change","wash","cleaning",
  "express","checkout","fitting","room","rooms","gift","cards","accessible",
  "wheelchair","restrooms","elevator","stairs","upstairs","downstairs",
]);

const OCR_SUBS: Record<string, string[]> = {
  "0": ["O","o"], "O": ["0"], "o": ["0"],
  "1": ["I","l","i"], "I": ["1","l"], "l": ["1","I","i"],
  "5": ["S","s"], "S": ["5"], "s": ["5"],
  "8": ["B"], "B": ["8"],
  "6": ["G","b"], "G": ["6"],
  "2": ["Z","z"], "Z": ["2"], "z": ["2"],
  "3": ["E","e"], "E": ["3"], "e": ["3"],
  "|": ["I","l","1"],
  "]": ["I","l"],
  "[": ["I","l"],
};

function correctOcrWord(word: string, lineContextText: string = ""): string {
  const cleanWord = word.trim();
  const lower = cleanWord.toLowerCase().replace(/[^a-z0-9]/g, "");
  if (lower.length < 2) return word;
  if (KNOWN_WORDS.has(lower)) return word;

  const lowerLine = lineContextText.toLowerCase();

  for (const [wordA, wordB] of CONTEXT_PAIRS) {
    if (lowerLine.includes(wordA) || lowerLine.includes(wordB)) {
      const targetPartner = lowerLine.includes(wordA) ? wordB : wordA;
      const dist = levenshteinDistance(lower, targetPartner);
      if (dist <= 3 && lower.length >= 4) {
        if (cleanWord === cleanWord.toUpperCase()) return targetPartner.toUpperCase();
        if (cleanWord[0] === cleanWord[0].toUpperCase()) {
          return targetPartner.charAt(0).toUpperCase() + targetPartner.slice(1);
        }
        return targetPartner;
      }
    }
  }

  for (let pos = 0; pos < cleanWord.length; pos++) {
    const ch = cleanWord[pos];
    const subs = OCR_SUBS[ch];
    if (!subs) continue;
    for (const sub of subs) {
      const candidate = cleanWord.slice(0, pos) + sub + cleanWord.slice(pos + 1);
      const candidateLower = candidate.toLowerCase().replace(/[^a-z0-9]/g, "");
      if (KNOWN_WORDS.has(candidateLower)) return candidate;
    }
  }

  let bestMatch = "";
  let minDistance = 3;

  KNOWN_WORDS.forEach((dictWord) => {
    if (Math.abs(dictWord.length - lower.length) <= 2) {
      const dist = levenshteinDistance(lower, dictWord);
      if (dist < minDistance && dist <= 2) {
        minDistance = dist;
        bestMatch = dictWord;
      }
    }
  });

  if (bestMatch && minDistance <= 2) {
    if (cleanWord === cleanWord.toUpperCase()) return bestMatch.toUpperCase();
    if (cleanWord[0] === cleanWord[0].toUpperCase()) {
      return bestMatch.charAt(0).toUpperCase() + bestMatch.slice(1);
    }
    return bestMatch;
  }

  return word;
}

function correctOcrLine(line: string): string {
  const words = line.split(/\s+/);
  return words
    .map((w) => correctOcrWord(w, line))
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

  const [showOriginal, setShowOriginal] = useState(false);
  const [copied, setCopied] = useState(false);
  const [torchActive, setTorchActive] = useState(false);
  const [contrastBoost, setContrastBoost] = useState(false);
  const [targetLang, setTargetLang] = useState<"es" | "en">("es");
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const [detectedRegions, setDetectedRegions] = useState<TextRegion[]>([]);

  const [focusPoint, setFocusPoint] = useState<{ x: number; y: number } | null>(null);

  /* ---------- Camera helpers ---------- */
  const startCamera = useCallback(async () => {
    setCameraBlocked(false);
    setHasResult(false);
    setShowOriginal(false);
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

  const toggleTorch = async () => {
    if (!videoRef.current?.srcObject) return;
    const stream = videoRef.current.srcObject as MediaStream;
    const track = stream.getVideoTracks()[0];
    if (track && "applyConstraints" in track) {
      try {
        const nextState = !torchActive;
        await track.applyConstraints({
          // @ts-ignore - advanced torch constraint
          advanced: [{ torch: nextState }],
        });
        setTorchActive(nextState);
      } catch (err) {
        console.warn("Torch not supported on this device/browser:", err);
      }
    }
  };

  const handleViewportTap = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cameraActive || hasResult) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setFocusPoint({ x, y });
    setTimeout(() => setFocusPoint(null), 1000);
  };

  /* ---------- Gemini Vision OCR + Translation ---------- */
  const visionTranslate = async (
    base64: string
  ): Promise<{ original: string; translated: string }[]> => {
    try {
      const res = await fetch("/api/vision-translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imageBase64: base64, targetLang }),
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
        body: JSON.stringify({ text, targetLang }),
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

    const clean = regions.filter((r) => {
      const orig = r.original.trim();
      const trans = r.translated.trim();
      if (!orig || !trans) return false;

      const boxW = r.bbox.x1 - r.bbox.x0;
      const boxH = r.bbox.y1 - r.bbox.y0;

      if (boxW < 18 || boxH < 10) return false;

      if (/^page\s+\d+$/i.test(orig) || /^revised:?\s*[\d\/]+$/i.test(orig)) return false;
      if (/^[\d\s\.\/\-\,\!\?\#\%\*\@]+$/.test(orig) && !orig.includes("$")) return false;

      if (orig.length <= 2 && !orig.includes("$")) {
        const lower = orig.toLowerCase();
        if (!["no", "si", "in", "on", "at", "to", "or", "el", "la", "un"].includes(lower)) {
          return false;
        }
      }

      const words = orig.split(/\s+/);
      const invalidWords = words.filter((w) => /^[^\w]+$/.test(w) || (w.length > 5 && !/[aeiouy]/i.test(w)));
      if (invalidWords.length > words.length / 2) return false;

      return true;
    });

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
    setDetectedRegions(regions);

    for (const region of regions) {
      const { bbox } = region;
      const padX = 6;
      const padY = 3;

      const boxW = Math.max(24, bbox.x1 - bbox.x0 + padX * 2);
      const boxH = Math.max(16, bbox.y1 - bbox.y0 + padY * 2);
      const x0 = Math.max(0, bbox.x0 - padX);
      const y0 = Math.max(0, bbox.y0 - padY);

      // Clean, modern translucent card overlay for maximum readability
      const [r, g, b] = sampleBgColor(ctx, bbox, w, h);
      const isDarkBg = luminance(r, g, b) < 0.5;
      const bgStr = isDarkBg ? "rgba(15, 23, 42, 0.92)" : "rgba(255, 255, 255, 0.94)";
      const textColor = isDarkBg ? "#ffffff" : "#0f172a";
      const borderColor = isDarkBg ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 62, 199, 0.3)";

      ctx.fillStyle = bgStr;
      ctx.strokeStyle = borderColor;
      ctx.lineWidth = 1;

      ctx.beginPath();
      if (typeof ctx.roundRect === "function") {
        ctx.roundRect(x0, y0, boxW, boxH, 6);
      } else {
        ctx.rect(x0, y0, boxW, boxH);
      }
      ctx.fill();
      ctx.stroke();

      let fontSize = Math.max(10, Math.min(boxH * 0.7, 42));
      ctx.font = `bold ${fontSize}px "Segoe UI", system-ui, -apple-system, sans-serif`;

      while (ctx.measureText(region.translated).width > boxW - 6 && fontSize > 8) {
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
      ctx.fillText(region.translated, x0 + 3, cy, boxW - 6);
      ctx.restore();
    }
  };

  /* ---------- Column & Line Break Aware OCR Word Segmentation ---------- */
  const groupWordsIntoColumnLines = (words: any[]): { text: string; bbox: { x0: number; y0: number; x1: number; y1: number }; confidence?: number }[] => {
    if (!words || words.length === 0) return [];

    const validWords = words.filter(
      (w) => w.text && w.text.trim().length > 0 && w.bbox && (w.bbox.x1 - w.bbox.x0) > 2
    );

    if (validWords.length === 0) return [];

    validWords.sort((a, b) => a.bbox.y0 - b.bbox.y0);

    const rows: any[][] = [];
    for (const w of validWords) {
      let placed = false;
      for (const row of rows) {
        const avgY0 = row.reduce((sum, item) => sum + item.bbox.y0, 0) / row.length;
        const avgH = row.reduce((sum, item) => sum + (item.bbox.y1 - item.bbox.y0), 0) / row.length;
        if (Math.abs(w.bbox.y0 - avgY0) < Math.max(7, avgH * 0.5)) {
          row.push(w);
          placed = true;
          break;
        }
      }
      if (!placed) {
        rows.push([w]);
      }
    }

    const lineBlocks: { text: string; bbox: { x0: number; y0: number; x1: number; y1: number }; confidence?: number }[] = [];

    for (const row of rows) {
      row.sort((a, b) => a.bbox.x0 - b.bbox.x0);
      let currentBlockWords: any[] = [];

      for (let i = 0; i < row.length; i++) {
        const w = row[i];
        if (currentBlockWords.length === 0) {
          currentBlockWords.push(w);
        } else {
          const prevW = currentBlockWords[currentBlockWords.length - 1];
          const gap = w.bbox.x0 - prevW.bbox.x1;
          const avgCharWidth = (prevW.bbox.x1 - prevW.bbox.x0) / Math.max(1, prevW.text.length);
          const columnGapThreshold = Math.max(40, avgCharWidth * 3.2);

          if (gap > columnGapThreshold) {
            const blockText = currentBlockWords.map((item) => item.text.trim()).join(" ");
            const minX0 = Math.min(...currentBlockWords.map((item) => item.bbox.x0));
            const minY0 = Math.min(...currentBlockWords.map((item) => item.bbox.y0));
            const maxX1 = Math.max(...currentBlockWords.map((item) => item.bbox.x1));
            const maxY1 = Math.max(...currentBlockWords.map((item) => item.bbox.y1));

            lineBlocks.push({
              text: correctOcrLine(blockText),
              bbox: { x0: minX0, y0: minY0, x1: maxX1, y1: maxY1 },
            });

            currentBlockWords = [w];
          } else {
            currentBlockWords.push(w);
          }
        }
      }

      if (currentBlockWords.length > 0) {
        const blockText = currentBlockWords.map((item) => item.text.trim()).join(" ");
        const minX0 = Math.min(...currentBlockWords.map((item) => item.bbox.x0));
        const minY0 = Math.min(...currentBlockWords.map((item) => item.bbox.y0));
        const maxX1 = Math.max(...currentBlockWords.map((item) => item.bbox.x1));
        const maxY1 = Math.max(...currentBlockWords.map((item) => item.bbox.y1));

        lineBlocks.push({
          text: correctOcrLine(blockText),
          bbox: { x0: minX0, y0: minY0, x1: maxX1, y1: maxY1 },
        });
      }
    }

    return lineBlocks.filter((b) => b.text.trim().length > 1);
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

      const ocrCanvas = preprocessForOcr(srcCanvas, contrastBoost);

      const tesseractPromise = (async () => {
        try {
          const worker = await createWorker("eng");
          const ret = await worker.recognize(ocrCanvas);
          await worker.terminate();

          // Use column-aware word segmentation to prevent line merging across menu columns
          const words = (ret.data as any).words || [];
          if (words.length > 0) {
            return groupWordsIntoColumnLines(words);
          }

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
    setShowOriginal(false);
    setDetectedRegions([]);
    startCamera();
  };

  const copyAllText = () => {
    if (detectedRegions.length === 0) return;
    const fullText = detectedRegions.map((r) => r.translated).join("\n");
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const speakFullDocument = () => {
    if (detectedRegions.length === 0 || typeof window === "undefined" || !("speechSynthesis" in window)) return;
    const fullText = detectedRegions.map((r) => r.translated).join(". ");
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(fullText);
    utterance.lang = targetLang === "es" ? "es-ES" : "en-US";
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
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

      {/* PORTRAIT CAMERA & RESULT CANVAS VIEWPORT */}
      <div
        onClick={handleViewportTap}
        className="relative w-full aspect-[3/4] rounded-2xl overflow-hidden bg-black shadow-lg border border-white/10 cursor-pointer group"
      >
        {/* Live Camera Stream */}
        <video
          ref={videoRef}
          playsInline
          muted
          style={{ transform: `scale(${zoomLevel})`, transformOrigin: "center" }}
          className={`w-full h-full object-cover transition-transform duration-200 ${
            cameraActive && !hasResult ? "" : "hidden"
          }`}
        />

        {/* Real-Time Laser Scan Line Beam Animation */}
        {cameraActive && !hasResult && !isProcessing && (
          <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-primary to-transparent opacity-80 shadow-md animate-bounce pointer-events-none z-10" />
        )}

        {/* Tap-to-Focus Reticle Visual Animation */}
        {focusPoint && (
          <div
            style={{ left: focusPoint.x - 24, top: focusPoint.y - 24 }}
            className="absolute w-12 h-12 border-2 border-amber-400 rounded-full animate-ping pointer-events-none z-30"
          />
        )}

        {/* Original Image View (When Toggle is Active) */}
        {hasResult && showOriginal && srcCanvasRef.current && (
          <img
            src={srcCanvasRef.current.toDataURL()}
            alt="Original Untouched"
            className="w-full h-full object-cover bg-slate-900"
          />
        )}

        {/* Translated Canvas View */}
        <canvas
          ref={resultCanvasRef}
          className={`w-full h-full object-cover bg-slate-900 ${
            hasResult && !showOriginal ? "" : "hidden"
          }`}
        />

        {/* Top Control Bar Overlay (Language Switcher + Torch + Boost + Zoom) */}
        {cameraActive && !hasResult && !isProcessing && (
          <div className="absolute top-3 inset-x-3 flex items-center justify-between z-20 pointer-events-auto gap-1">
            {/* Language Direction Switcher */}
            <button
              onClick={(e) => {
                e.stopPropagation();
                setTargetLang(targetLang === "es" ? "en" : "es");
              }}
              className="px-3 py-1.5 rounded-full bg-black/65 backdrop-blur-md text-white text-[11px] font-extrabold border border-white/20 flex items-center gap-1.5 hover:bg-black/80 transition-all shadow-sm"
            >
              <span>{targetLang === "es" ? "English" : "Español"}</span>
              <ArrowRightLeft className="w-3 h-3 text-primary" />
              <span>{targetLang === "es" ? "Español" : "English"}</span>
            </button>

            <div className="flex items-center gap-1">
              {/* Contrast Boost Toggle */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setContrastBoost(!contrastBoost);
                }}
                className={`p-2 rounded-full backdrop-blur-md transition-all shadow-md ${
                  contrastBoost
                    ? "bg-primary text-white ring-2 ring-white"
                    : "bg-black/60 text-white hover:bg-black/80"
                }`}
                title="Boost Contrast for Dim Text"
              >
                <SunMedium className="w-4 h-4" />
              </button>

              {/* Flash / Torch Toggle */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  toggleTorch();
                }}
                className={`p-2 rounded-full backdrop-blur-md transition-all shadow-md ${
                  torchActive
                    ? "bg-amber-400 text-slate-900 ring-2 ring-white"
                    : "bg-black/60 text-white hover:bg-black/80"
                }`}
                title="Toggle Flashlight"
              >
                <Zap className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Viewfinder Guideline Reticle */}
        {cameraActive && !hasResult && !isProcessing && (
          <div className="absolute inset-4 border-2 border-dashed border-white/50 rounded-xl pointer-events-none flex items-end justify-center pb-3">
            <span className="px-3.5 py-1.5 rounded-full bg-black/65 text-white text-xs font-semibold backdrop-blur-sm shadow-sm flex items-center gap-1.5">
              <Scan className="w-3.5 h-3.5 text-primary animate-pulse" />
              <span>
                {targetLang === "es"
                  ? "Escaneando en vivo → Toque Traducir"
                  : "Scanning live → Tap Translate"}
              </span>
            </span>
          </div>
        )}

        {/* Processing Spinner Overlay */}
        {isProcessing && (
          <div className="absolute inset-0 bg-black/75 backdrop-blur-sm flex flex-col items-center justify-center text-white z-30">
            <RefreshCw className="w-8 h-8 text-primary animate-spin mb-2" />
            <span className="text-xs font-bold">{statusText}</span>
          </div>
        )}

        {/* Camera Permission Blocked Warning */}
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
      </div>

      {/* RESULT CONTROL TOOLBAR (Original Toggle + Copy + Listen) */}
      {hasResult && detectedRegions.length > 0 && (
        <div className="bg-surface border border-secondary-fixed p-2 rounded-2xl flex items-center justify-between gap-2 shadow-2xs">
          <button
            onClick={() => setShowOriginal(!showOriginal)}
            className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition-all ${
              showOriginal
                ? "bg-amber-500/10 text-amber-600 border border-amber-500/30"
                : "bg-primary/10 text-primary border border-primary/30"
            }`}
          >
            {showOriginal ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
            <span>{showOriginal ? "Ver Traducción" : "Ver Original"}</span>
          </button>

          <button
            onClick={copyAllText}
            className="p-2.5 rounded-xl bg-surface-container border border-secondary-fixed text-on-surface hover:text-primary transition-colors flex items-center gap-1"
            title="Copiar texto traducido"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-500" /> : <Copy className="w-4 h-4" />}
          </button>

          <button
            onClick={speakFullDocument}
            className="p-2.5 rounded-xl bg-secondary-fixed text-primary hover:scale-105 transition-transform"
            title="Escuchar pronunciación"
          >
            <Volume2 className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* MAIN ACTION BUTTONS */}
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

      {/* CLEAN STRUCTURED TRANSLATION BREAKDOWN LIST (100% Readable & Organized) */}
      {hasResult && detectedRegions.length > 0 && (
        <div className="space-y-2 pt-1 animate-in fade-in slide-in-from-bottom-2 duration-300">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-black text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <Scan className="w-3.5 h-3.5 text-[#003ec7]" />
              <span>{lang === "es" ? "Traducción Estructurada" : "Structured Translation"}</span>
            </span>
            <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">
              {detectedRegions.length} {lang === "es" ? "elementos" : "items"}
            </span>
          </div>

          <div className="space-y-2 max-h-72 overflow-y-auto pr-0.5">
            {detectedRegions.map((region, idx) => (
              <div
                key={idx}
                className="p-3 bg-white rounded-2xl border border-slate-200 shadow-2xs hover:border-[#003ec7]/40 transition-all space-y-1 text-left"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="font-extrabold text-xs text-slate-900 leading-snug">
                    {region.translated}
                  </div>
                  <button
                    onClick={() => {
                      if (typeof window !== "undefined" && "speechSynthesis" in window) {
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance(region.translated);
                        utterance.lang = targetLang === "es" ? "es-ES" : "en-US";
                        window.speechSynthesis.speak(utterance);
                      }
                    }}
                    className="p-1 rounded-lg text-slate-400 hover:text-[#003ec7] hover:bg-blue-50 transition-colors shrink-0"
                    title="Pronounce / Pronunciar"
                  >
                    <Volume2 className="w-3.5 h-3.5" />
                  </button>
                </div>

                <div className="text-[11px] font-medium text-slate-500 italic border-t border-slate-100 pt-1">
                  "{region.original}"
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
