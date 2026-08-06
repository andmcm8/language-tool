import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

/* ================================================================
   TRANSLATE ROUTE — Uses multiple engines in priority order:
   1. Gemini AI  (if valid AIzaSy... key is set)
   2. MyMemory Translation API  (FREE, no key needed, real MT engine)
   3. Local 200+ word dictionary  (offline fallback)
   ================================================================ */

/* ---------- ENGINE 1: Gemini AI ---------- */
async function tryGemini(text: string): Promise<string | null> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return null;

  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.0-flash",
      systemInstruction:
        "You are a professional English→Spanish translator. Output ONLY the translated Spanish text. No quotes, no explanations.",
    });
    const result = await model.generateContent(text);
    const translation = result.response.text().trim();
    return translation && translation !== text ? translation : null;
  } catch {
    return null;
  }
}

/* ---------- ENGINE 2: MyMemory Translation API (free, no key) ---------- */
async function tryMyMemory(text: string): Promise<string | null> {
  try {
    const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(
      text
    )}&langpair=en|es`;
    const res = await fetch(url, { signal: AbortSignal.timeout(6000) });
    const data = await res.json();
    const translated = data?.responseData?.translatedText;
    if (
      translated &&
      typeof translated === "string" &&
      translated.toUpperCase() !== text.toUpperCase() &&
      !translated.includes("PLEASE SELECT TWO LANGUAGES") &&
      !translated.includes("MYMEMORY WARNING")
    ) {
      // MyMemory sometimes returns ALL CAPS — match original casing style
      if (text === text.toUpperCase()) return translated.toUpperCase();
      if (
        text[0] === text[0].toUpperCase() &&
        text.slice(1) === text.slice(1).toLowerCase()
      ) {
        return (
          translated.charAt(0).toUpperCase() +
          translated.slice(1).toLowerCase()
        );
      }
      return translated;
    }
    return null;
  } catch {
    return null;
  }
}

/* ---------- ENGINE 3: Local word-by-word dictionary (offline fallback) ---------- */
const W: Record<string, string> = {
  welcome:"bienvenidos",hello:"hola",please:"por favor",yes:"sí",no:"no",
  good:"buen",morning:"mañana",afternoon:"tarde",evening:"noche",
  store:"tienda",shop:"tienda",market:"mercado",grocery:"abarrotes",
  entrance:"entrada",exit:"salida",parking:"estacionamiento",
  restroom:"baño",bathroom:"baño",floor:"piso",aisle:"pasillo",
  counter:"mostrador",register:"caja",checkout:"caja",
  hours:"horarios",hour:"hora",open:"abierto",closed:"cerrado",
  today:"hoy",daily:"diariamente",monday:"lunes",tuesday:"martes",
  wednesday:"miércoles",thursday:"jueves",friday:"viernes",
  saturday:"sábado",sunday:"domingo",until:"hasta",from:"desde",
  spaghetti: "espaguetis", meatballs: "albóndigas", meatball: "albóndiga",
  lasagna: "lasaña", ravioli: "ravioles", fettuccine: "fettuccine",
  penne: "penne", macaroni: "macarrones", noodle: "fideo", noodles: "fideos",
  marinara: "marinara", alfredo: "alfredo", parmesan: "parmesano",
  food:"comida",menu:"menú",meal:"comida",plate:"plato",
  bread:"pan",meat:"carne",beef:"res",steak:"bistec",pork:"cerdo",
  chicken:"pollo",ham:"jamón",fish:"pescado",cheese:"queso",
  milk:"leche",eggs:"huevos",egg:"huevo",rice:"arroz",beans:"frijoles",
  corn:"maíz",potato:"papa",potatoes:"papas",fries:"papas fritas",
  tomato:"tomate",onion:"cebolla",lettuce:"lechuga",avocado:"aguacate",
  salad:"ensalada",soup:"sopa",sandwich:"sándwich",burger:"hamburguesa",
  taco:"taco",tacos:"tacos",empanada:"empanada",empanadas:"empanadas",
  water:"agua",juice:"jugo",soda:"refresco",coffee:"café",tea:"té",
  beer:"cerveza",wine:"vino",drink:"bebida",drinks:"bebidas",
  sugar:"azúcar",salt:"sal",sauce:"salsa",butter:"mantequilla",
  cream:"crema",oil:"aceite",honey:"miel",
  fresh:"fresco",hot:"caliente",cold:"frío",warm:"tibio",
  baked:"horneado",fried:"frito",grilled:"a la parrilla",
  roast:"asado",roasted:"asado",melted:"fundido",homemade:"casero",
  organic:"orgánico",natural:"natural",spicy:"picante",sweet:"dulce",
  special:"especial",specials:"especiales",sale:"oferta",
  discount:"descuento",price:"precio",free:"gratis",new:"nuevo",
  notice:"aviso",warning:"advertencia",caution:"precaución",
  cash:"efectivo",card:"tarjeta",credit:"crédito",debit:"débito",
  payment:"pago",accepted:"aceptado",required:"requerido",
  delivery:"entrega",pickup:"recoger",order:"pedido",
  small:"pequeño",medium:"mediano",large:"grande",extra:"extra",
  regular:"regular",double:"doble",half:"medio",each:"cada uno",
  per:"por",included:"incluido",includes:"incluye",available:"disponible",
  bakery:"panadería",deli:"delicatessen",produce:"frutas y verduras",
  dairy:"lácteos",frozen:"congelados",snacks:"bocadillos",
  pharmacy:"farmacia",prescription:"receta",repair:"reparación",
  warranty:"garantía",screen:"pantalla",battery:"batería",
  push:"empuje",pull:"jale",employees:"empleados",only:"solo",
  customers:"clientes",service:"servicio",phone:"teléfono",
  the:"el",a:"un",and:"y",or:"o",with:"con",without:"sin",
  for:"para",of:"de",is:"es",are:"son",our:"nuestro",this:"este",
  all:"todos",made:"hecho",served:"servido",
};

const PHRASES: [RegExp, string][] = [
  // ---- Expanded Food & Restaurant Pairs ----
  [/\bSPAGHETTI AND MEATBALLS\b/gi, "ESPAGUETIS CON ALBÓNDIGAS"],
  [/\bSPAGHETTI WITH MEATBALLS\b/gi, "ESPAGUETIS CON ALBÓNDIGAS"],
  [/\bSPAGHETTI\b/gi, "ESPAGUETIS"],
  [/\bMEATBALLS?\b/gi, "ALBÓNDIGAS"],
  [/\bGARLIC BREAD\b/gi, "PAN DE AJO"],
  [/\bGARLIC KNOTS?\b/gi, "NUDOS DE AJO"],
  [/\bCHIPS AND SALSA\b/gi, "TOTOPOS CON SALSA"],
  [/\bCHIPS AND GUACAMOLE\b/gi, "TOTOPOS CON GUACAMOLE"],
  [/\bFRENCH FRIES\b/gi, "PAPAS FRITAS"],
  [/\bFRENCH TOAST\b/gi, "TOSTADAS FRANCESAS"],
  [/\bMASHED POTATOES\b/gi, "PURÉ DE PAPAS"],
  [/\bPOTATO SALAD\b/gi, "ENSALADA DE PAPA"],
  [/\bMACARONI SALAD\b/gi, "ENSALADA DE CODES"],
  [/\bMACARONI AND CHEESE\b/gi, "MACARRONES CON QUESO"],
  [/\bMAC AND CHEESE\b/gi, "MACARRONES CON QUESO"],
  [/\bBUFFALO WINGS\b/gi, "ALITAS BUFFALO"],
  [/\bBBQ RIBS\b/gi, "COSTILLAS A LA BARBACOA"],
  [/\bCHICKEN TENDERS\b/gi, "TIRAS DE POLLO"],
  [/\bCHICKEN NUGGETS\b/gi, "NUGGETS DE POLLO"],
  [/\bCHICKEN WINGS\b/gi, "ALITAS DE POLLO"],
  [/\bCHICKEN SOUP\b/gi, "SOPA DE POLLO"],
  [/\bCAESAR SALAD\b/gi, "ENSALADA CÉSAR"],
  [/\bGREEK SALAD\b/gi, "ENSALADA GRIEGA"],
  [/\bCLAM CHOWDER\b/gi, "CREMA DE ALMEJAS"],
  [/\bLOBSTER ROLL\b/gi, "ROLLO DE LANGOSTA"],
  [/\bCRAB CAKES?\b/gi, "PASTELES DE CANGREJO"],
  [/\bSHRIMP COCKTAIL\b/gi, "CÓCTEL DE CAMARONES"],
  [/\bFRIED CALAMARI\b/gi, "CALAMARES FRITOS"],
  [/\bSTEAK AND EGGS\b/gi, "BISTEC CON HUEVOS"],
  [/\bFISH AND CHIPS\b/gi, "PESCADO CON PAPAS"],
  [/\bAPPLE PIE\b/gi, "PASTEL DE MANZANA"],
  [/\bCHOCOLATE CAKE\b/gi, "PASTEL DE CHOCOLATE"],
  [/\bTRES LECHES\b/gi, "TRES LECHES"],
  [/\bFLAN DE LECHE\b/gi, "FLAN DE LECHE"],
  [/\bICE CREAM\b/gi, "HELADO"],
  [/\bICED TEA\b/gi, "TÉ HELADO"],
  [/\bICED COFFEE\b/gi, "CAFÉ HELADO"],
  [/\bHOT CHOCOLATE\b/gi, "CHOCOLATE CALIENTE"],
  [/\bSWEET PLANTAINS?\b/gi, "PLÁTANOS MADUROS"],
  [/\bGREEN PLANTAINS?\b/gi, "TOSTONES / PLÁTANOS VERDES"],
  [/\bCRISPY PORK BELLY\b/gi, "CHICHARRÓN CRUJIENTE"],
  [/\bPORK CHOPS\b/gi, "CHULETAS DE CERDO"],
  [/\bBANDEJA PAISA\b/gi, "BANDEJA PAISA"],

  // ---- Expanded Store & Service Terms ----
  [/\bPRESCRIPTION REFILL\b/gi, "REPOSITORIO DE RECETAS"],
  [/\bPRESCRIPTION TRANSFER\b/gi, "TRANSFERENCIA DE RECETAS"],
  [/\bSCREEN REPAIR\b/gi, "REPARACIÓN DE PANTALLA"],
  [/\bSCREEN REPLACEMENT\b/gi, "REEMPLAZO DE PANTALLA"],
  [/\bBATTERY REPLACEMENT\b/gi, "REEMPLAZO DE BATERÍA"],
  [/\bOIL CHANGE\b/gi, "CAMBIO DE ACEITE"],
  [/\bCAR WASH\b/gi, "LAVADO DE AUTOS"],
  [/\bDRY CLEANING\b/gi, "TINTORERÍA"],
  [/\bEXPRESS CHECKOUT\b/gi, "CAJA RÁPIDA"],
  [/\bCUSTOMER SERVICE\b/gi, "SERVICIO AL CLIENTE"],
  [/\bFITTING ROOMS?\b/gi, "PROBADORES"],
  [/\bGIFT CARDS?\b/gi, "TARJETAS DE REGALO"],
  [/\bWHEELCHAIR ACCESSIBLE\b/gi, "ACCESIBLE PARA SILLAS DE RUEDAS"],
  [/\bRESTROOMS?\b/gi, "BAÑOS"],
  [/\bDAILY SPECIALS?\b/gi,"ESPECIAL DEL DÍA"],
  [/\bHOT ROAST BEEF SANDWICH\b/gi,"SÁNDWICH DE CARNE ASADA CALIENTE"],
  [/\bROAST BEEF\b/gi,"CARNE ASADA"],
  [/\bMELTED SWISS CHEESE\b/gi,"QUESO SUIZO FUNDIDO"],
  [/\bFRESH BREAD\b/gi,"PAN FRESCO"],
  [/\bBAKED DAILY\b/gi,"HORNEADO DIARIAMENTE"],
  [/\bMADE FRESH DAILY\b/gi,"HECHO FRESCO DIARIAMENTE"],
  [/\bEBT ACCEPTED\b/gi,"SE ACEPTA EBT"],
  [/\bCASH ONLY\b/gi,"SOLO EFECTIVO"],
  [/\bCASH OR CARD\b/gi,"EFECTIVO O TARJETA"],
  [/\bNO PARKING\b/gi,"PROHIBIDO ESTACIONAR"],
  [/\bWET FLOOR\b/gi,"PISO MOJADO"],
  [/\bEMPLOYEES ONLY\b/gi,"SOLO EMPLEADOS"],
  [/\bTHANK YOU\b/gi,"GRACIAS"],
  [/\bFREE DELIVERY\b/gi,"ENTREGA GRATIS"],
  [/\bFREE WIFI\b/gi,"WIFI GRATIS"],
  [/\bNOW HIRING\b/gi,"SOLICITAMOS EMPLEADOS"],
  [/\bSOLD OUT\b/gi,"AGOTADO"],
  [/\bTAKE OUT\b/gi,"PARA LLEVAR"],
  [/\bTO GO\b/gi,"PARA LLEVAR"],
  [/\bICE CREAM\b/gi,"HELADO"],
  [/\bBLACK BEANS\b/gi,"FRIJOLES NEGROS"],
  [/\bWHITE RICE\b/gi,"ARROZ BLANCO"],
  [/\bFRIED EGG\b/gi,"HUEVO FRITO"],
];

function localTranslate(text: string): string {
  let result = text;
  for (const [p, r] of PHRASES) {
    result = result.replace(p, (m) =>
      m === m.toUpperCase() ? r.toUpperCase() : r
    );
  }
  result = result.replace(/[A-Za-zÀ-ÿ'']+/g, (word) => {
    const t = W[word.toLowerCase()];
    if (!t) return word;
    if (word === word.toUpperCase()) return t.toUpperCase();
    if (word[0] === word[0].toUpperCase())
      return t.charAt(0).toUpperCase() + t.slice(1);
    return t;
  });
  return result;
}

/* ================================================================
   ROUTE HANDLER
   ================================================================ */
export async function POST(req: NextRequest) {
  let text = "";
  try {
    const body = await req.json();
    text = (body.text || "").trim();
    if (!text) return NextResponse.json({ translation: "" });

    // 1) Try Gemini
    const gemini = await tryGemini(text);
    if (gemini) return NextResponse.json({ translation: gemini });

    // 2) Try MyMemory (free real MT engine, no key needed)
    const myMemory = await tryMyMemory(text);
    if (myMemory) return NextResponse.json({ translation: myMemory });

    // 3) Local dictionary fallback
    return NextResponse.json({ translation: localTranslate(text) });
  } catch (error: any) {
    console.error("Translate error:", error?.message);
    return NextResponse.json({
      translation: text ? localTranslate(text) : text,
    });
  }
}
