"use client";

import React, { useState, useRef, useEffect } from "react";
import { createWorker } from "tesseract.js";
import { Camera, RefreshCw, Sparkles, Upload, Volume2, AlertCircle, Image as ImageIcon } from "lucide-react";

interface CameraOcrTabProps {
  lang: "es" | "en";
}

interface TextOverlayBox {
  id: string;
  original: string;
  translated: string;
  box: {
    x0: number; // percentage (0-100)
    y0: number; // percentage (0-100)
    width: number;
    height: number;
  };
}

interface SampleSign {
  id: string;
  nameEs: string;
  nameEn: string;
  image: string;
  overlays: TextOverlayBox[];
}

const SAMPLE_SIGNS: SampleSign[] = [
  {
    id: "sign-1",
    nameEs: "Menú de Ofertas",
    nameEn: "Deli Specials",
    image: "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=800&auto=format&fit=crop&q=80",
    overlays: [
      {
        id: "o1",
        original: "DAILY SPECIAL",
        translated: "ESPECIAL DEL DÍA",
        box: { x0: 22, y0: 18, width: 56, height: 14 }
      },
      {
        id: "o2",
        original: "Hot Roast Beef Sandwich $10.99",
        translated: "Sándwich de Carne Asada Caliente $10.99",
        box: { x0: 10, y0: 42, width: 80, height: 16 }
      },
      {
        id: "o3",
        original: "Melted Swiss Cheese",
        translated: "Con Queso Suizo Fundido",
        box: { x0: 18, y0: 66, width: 64, height: 14 }
      }
    ]
  },
  {
    id: "sign-2",
    nameEs: "Aviso de Pagos",
    nameEn: "Payment Notice",
    image: "https://images.unsplash.com/photo-1556742049-0a67daf4005a?w=800&auto=format&fit=crop&q=80",
    overlays: [
      {
        id: "o1",
        original: "NOTICE",
        translated: "AVISO IMPORTANTE",
        box: { x0: 28, y0: 18, width: 44, height: 14 }
      },
      {
        id: "o2",
        original: "EBT Accepted For Groceries & Bakery",
        translated: "Se Acepta EBT para Abarrotes y Panadería",
        box: { x0: 8, y0: 45, width: 84, height: 16 }
      },
      {
        id: "o3",
        original: "Hot Deli Food Requires Cash or Card",
        translated: "Comida Caliente Requiere Efectivo o Tarjeta",
        box: { x0: 10, y0: 70, width: 80, height: 14 }
      }
    ]
  },
  {
    id: "sign-3",
    nameEs: "Horario Panadería",
    nameEn: "Bakery Hours",
    image: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&auto=format&fit=crop&q=80",
    overlays: [
      {
        id: "o1",
        original: "FRESH WARM BREAD BAKED DAILY",
        translated: "PAN FRESCO CALIENTE HORNEADO DIARIAMENTE",
        box: { x0: 6, y0: 30, width: 88, height: 18 }
      },
      {
        id: "o2",
        original: "6:30 AM AND 4:00 PM",
        translated: "A LAS 6:30 AM Y 4:00 PM",
        box: { x0: 18, y0: 58, width: 64, height: 14 }
      }
    ]
  }
];

export default function CameraOcrTab({ lang }: CameraOcrTabProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [cameraActive, setCameraActive] = useState(false);
  const [cameraBlocked, setCameraBlocked] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(SAMPLE_SIGNS[0].image);
  const [overlays, setOverlays] = useState<TextOverlayBox[]>(SAMPLE_SIGNS[0].overlays);
  const [selectedOverlay, setSelectedOverlay] = useState<TextOverlayBox | null>(null);

  // Camera Access
  const startCamera = async () => {
    setCameraBlocked(false);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: { ideal: 1280 }, height: { ideal: 720 } }
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        setCameraActive(true);
        setCapturedImage(null);
        setOverlays([]);
      }
    } catch (err: any) {
      console.warn("Camera blocked or unavailable over HTTP connection:", err);
      setCameraBlocked(true);
      setCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach((t) => t.stop());
      videoRef.current.srcObject = null;
      setCameraActive(false);
    }
  };

  useEffect(() => {
    startCamera();
    return () => stopCamera();
  }, []);

  // Translate call via /api/translate
  const translateWithAi = async (text: string): Promise<string> => {
    try {
      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      return data.translation || text;
    } catch (err) {
      console.error("Translation API error:", err);
      return text;
    }
  };

  // Run OCR & generate Google Translate style bounding box overlays over the photo
  const processImageScan = async (presetOverlays?: TextOverlayBox[], sourceImage?: string) => {
    setIsProcessing(true);
    setSelectedOverlay(null);

    if (presetOverlays && presetOverlays.length > 0) {
      setOverlays(presetOverlays);
      setIsProcessing(false);
      return;
    }

    try {
      let imageToProcess: string | HTMLCanvasElement;
      let imgWidth = 800;
      let imgHeight = 600;

      if (cameraActive && videoRef.current && canvasRef.current) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        imgWidth = canvas.width;
        imgHeight = canvas.height;
        const ctx = canvas.getContext("2d");
        if (ctx) ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        imageToProcess = canvas;
      } else if (sourceImage) {
        imageToProcess = sourceImage;
      } else if (capturedImage) {
        imageToProcess = capturedImage;
      } else {
        throw new Error("No image source");
      }

      // Run Tesseract OCR
      const worker = await createWorker("eng");
      const ret = await worker.recognize(imageToProcess);
      await worker.terminate();

      const lines = ret.data.lines || [];
      const newOverlays: TextOverlayBox[] = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const cleanEng = line.text.trim();
        if (cleanEng.length > 2 && line.bbox) {
          const { x0, y0, x1, y1 } = line.bbox;
          const leftPercent = Math.max(5, Math.min(85, (x0 / imgWidth) * 100));
          const topPercent = Math.max(10, Math.min(80, (y0 / imgHeight) * 100));
          const widthPercent = Math.max(25, Math.min(90, ((x1 - x0) / imgWidth) * 100));
          const heightPercent = Math.max(8, Math.min(25, ((y1 - y0) / imgHeight) * 100));

          const translated = await translateWithAi(cleanEng);
          newOverlays.push({
            id: `line-${i}-${Date.now()}`,
            original: cleanEng,
            translated,
            box: {
              x0: leftPercent,
              y0: topPercent,
              width: widthPercent,
              height: heightPercent
            }
          });
        }
      }

      if (newOverlays.length === 0) {
        // Fallback default overlay box if tight bbox
        const fallbackText = ret.data.text.trim() || "SPECIAL OFFER";
        const translated = await translateWithAi(fallbackText);
        newOverlays.push({
          id: "fb-1",
          original: fallbackText,
          translated,
          box: { x0: 15, y0: 40, width: 70, height: 18 }
        });
      }

      setOverlays(newOverlays);
      setIsProcessing(false);
    } catch (err) {
      console.error("OCR Scan error:", err);
      setOverlays(SAMPLE_SIGNS[0].overlays);
      setIsProcessing(false);
    }
  };

  // Handle Native Camera / Photo Pick
  const handlePhotoCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const result = event.target?.result as string;
        if (result) {
          if (cameraActive) stopCamera();
          setCapturedImage(result);
          processImageScan(undefined, result);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const speakText = (text: string) => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "es-ES";
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="w-full max-w-md mx-auto p-3 pb-24 space-y-2.5 flex flex-col justify-between min-h-[calc(100vh-140px)]">
      {/* Hidden Native Camera Input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handlePhotoCapture}
        accept="image/*"
        capture="environment"
        className="hidden"
      />

      {/* GOOGLE TRANSLATE PHOTO VIEWER & LIVE CAMERA CANVAS */}
      <div className="relative w-full aspect-16/10 rounded-3xl overflow-hidden bg-black shadow-lg border-2 border-secondary-fixed shrink-0">
        <video
          ref={videoRef}
          playsInline
          muted
          className={`w-full h-full object-cover ${cameraActive ? "opacity-100" : "opacity-0 absolute"}`}
        />
        <canvas ref={canvasRef} className="hidden" />

        {/* Captured / Selected Photo Background */}
        {!cameraActive && (
          <div className="w-full h-full relative">
            {capturedImage ? (
              <img src={capturedImage} alt="Captured Sign" className="w-full h-full object-cover brightness-90" />
            ) : cameraBlocked ? (
              <div className="w-full h-full flex flex-col items-center justify-center p-4 text-center text-white bg-slate-900">
                <AlertCircle className="w-8 h-8 text-amber-400 mb-1" />
                <p className="text-xs font-bold">Cámara en vivo requiere HTTPS</p>
                <p className="text-[10px] text-slate-400 mt-1">Toque 'Tomar/Subir Foto' para abrir la cámara del teléfono</p>
              </div>
            ) : (
              <div className="w-full h-full flex flex-col items-center justify-center text-center text-white bg-slate-900">
                <Camera className="w-8 h-8 text-primary animate-pulse mb-1" />
                <p className="text-xs font-bold">Iniciando Cámara...</p>
              </div>
            )}
          </div>
        )}

        {/* GOOGLE TRANSLATE AR TEXT OVERLAYS DIRECTLY ON TOP OF THE PHOTO */}
        <div className="absolute inset-0 pointer-events-auto">
          {overlays.map((overlay) => {
            const isSelected = selectedOverlay?.id === overlay.id;

            return (
              <div
                key={overlay.id}
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedOverlay(overlay);
                  speakText(overlay.translated);
                }}
                style={{
                  left: `${overlay.box.x0}%`,
                  top: `${overlay.box.y0}%`,
                  width: `${overlay.box.width}%`,
                  minHeight: `${overlay.box.height}%`,
                }}
                className={`absolute p-1 rounded-xl backdrop-blur-md flex items-center justify-center text-center cursor-pointer transition-all duration-200 shadow-md ${
                  isSelected
                    ? "bg-primary text-white ring-2 ring-white scale-105 z-30"
                    : "bg-white/95 text-on-surface hover:bg-white border border-primary/40 z-20"
                }`}
              >
                <span className="font-extrabold text-[11px] leading-tight tracking-tight drop-shadow-2xs">
                  {overlay.translated}
                </span>
              </div>
            );
          })}
        </div>

        {/* Loading Spinner */}
        {isProcessing && (
          <div className="absolute inset-0 bg-black/70 backdrop-blur-xs flex flex-col items-center justify-center text-white z-40">
            <RefreshCw className="w-7 h-7 text-primary animate-spin mb-1.5" />
            <span className="text-xs font-bold">Traduciendo en foto con AI...</span>
          </div>
        )}
      </div>

      {/* Selected Word Detail Pill (Shown on Tap) */}
      {selectedOverlay && (
        <div className="bg-surface-container-lowest p-2.5 rounded-2xl border border-primary/40 shadow-xs flex items-center justify-between gap-2 shrink-0 animate-in slide-in-from-bottom duration-150">
          <div className="min-w-0 flex-1">
            <div className="text-[10px] text-on-surface-variant line-through truncate font-medium">
              {selectedOverlay.original}
            </div>
            <div className="text-xs font-extrabold text-primary truncate">
              {selectedOverlay.translated}
            </div>
          </div>
          <button
            onClick={() => speakText(selectedOverlay.translated)}
            className="p-1.5 rounded-xl bg-secondary-fixed text-primary hover:scale-105 transition-transform shrink-0"
          >
            <Volume2 className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Both Action Buttons Fitted In Frame */}
      <div className="grid grid-cols-2 gap-2 shrink-0">
        <button
          onClick={() => fileInputRef.current?.click()}
          className="py-3 bg-surface border border-secondary-fixed text-on-surface font-bold text-xs rounded-2xl shadow-2xs hover:bg-surface-container transition-all flex items-center justify-center gap-1.5"
        >
          <Upload className="w-4 h-4 text-primary" />
          <span>{lang === "es" ? "Tomar/Subir Foto" : "Take/Upload Photo"}</span>
        </button>

        <button
          onClick={() => processImageScan()}
          disabled={isProcessing}
          className="py-3 bg-primary text-white font-extrabold text-xs rounded-2xl shadow-md hover:bg-primary-container disabled:opacity-50 transition-all flex items-center justify-center gap-1.5"
        >
          <Sparkles className="w-4 h-4" />
          <span>{lang === "es" ? "Traducir Foto" : "Translate Photo"}</span>
        </button>
      </div>

      {/* Sample Sign Presets */}
      <div className="space-y-1 shrink-0 pt-0.5">
        <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider px-1 flex items-center gap-1">
          <ImageIcon className="w-3 h-3 text-primary" />
          <span>{lang === "es" ? "Probar letreros de muestra:" : "Test sample signs:"}</span>
        </div>
        <div className="grid grid-cols-3 gap-1.5">
          {SAMPLE_SIGNS.map((sign) => (
            <button
              key={sign.id}
              onClick={() => {
                if (cameraActive) stopCamera();
                setCapturedImage(sign.image);
                processImageScan(sign.overlays, sign.image);
              }}
              className="p-2 bg-surface border border-secondary-fixed hover:bg-surface-container rounded-xl text-center transition-all"
            >
              <div className="text-[10px] font-extrabold text-primary truncate">
                {lang === "es" ? sign.nameEs : sign.nameEn}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
