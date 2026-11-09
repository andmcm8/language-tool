"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  ArrowRightLeft,
  Mic,
  MicOff,
  Volume2,
  Copy,
  Check,
  X,
  Sparkles,
  Loader2,
  Tv,
  Star,
  CreditCard,
  Utensils,
  Clock,
  Wheat,
} from "lucide-react";

interface TranslatorTabProps {
  lang: "es" | "en";
}

const PHRASE_CATEGORIES = [
  { id: "all", labelEs: "Todas", labelEn: "All", icon: Sparkles },
  { id: "order", labelEs: "Pedir", labelEn: "Ordering", icon: Utensils },
  { id: "diet", labelEs: "Alergias y dieta", labelEn: "Allergies & diet", icon: Wheat },
  { id: "pay", labelEs: "Pagar", labelEn: "Paying", icon: CreditCard },
  { id: "table", labelEs: "Mesa y horarios", labelEn: "Table & hours", icon: Clock },
];

const CATEGORIZED_PHRASES = [
  {
    cat: "order",
    en: "Could we see the menu, please?",
    es: "¿Nos puede traer el menú, por favor?",
    phoneticEs: "Nohs PWEH-deh trah-EHR ehl meh-NOO, pohr fah-VOHR?",
    phoneticEn: "Kud ui si de me-niu, pliis?",
  },
  {
    cat: "order",
    en: "I would like to order this one.",
    es: "Quisiera pedir este platillo.",
    phoneticEs: "Kee-SYEH-rah peh-DEER EHS-teh plah-TEE-yoh.",
    phoneticEn: "Ai wud laik tu or-der dis uan.",
  },
  {
    cat: "order",
    en: "What do you recommend?",
    es: "¿Qué nos recomienda?",
    phoneticEs: "Keh nohs reh-koh-MYEHN-dah?",
    phoneticEn: "Uat du iu re-ko-mend?",
  },
  {
    cat: "order",
    en: "Is this dish spicy?",
    es: "¿Este platillo es picante?",
    phoneticEs: "EHS-teh plah-TEE-yoh ehs pee-KAHN-teh?",
    phoneticEn: "Is dis dish spai-si?",
  },
  {
    cat: "order",
    en: "Could I have it to go?",
    es: "¿Me lo puede preparar para llevar?",
    phoneticEs: "Meh loh PWEH-deh preh-pah-RAHR PAH-rah yeh-VAHR?",
    phoneticEn: "Kud ai jav it tu gou?",
  },
  {
    cat: "diet",
    en: "I have a food allergy.",
    es: "Tengo una alergia alimentaria.",
    phoneticEs: "TEHN-goh OO-nah ah-LEHR-hyah ah-lee-mehn-TAH-ryah.",
    phoneticEn: "Ai jav e fud a-ler-yi.",
  },
  {
    cat: "diet",
    en: "Does this contain nuts, dairy or gluten?",
    es: "¿Esto contiene nueces, lácteos o gluten?",
    phoneticEs: "EHS-toh kohn-TYEH-neh NWEH-sehs, LAHK-teh-ohs oh GLOO-tehn?",
    phoneticEn: "Das dis kon-tein nats, de-ri or glu-ten?",
  },
  {
    cat: "diet",
    en: "Do you have vegetarian options?",
    es: "¿Tienen opciones vegetarianas?",
    phoneticEs: "TYEH-nehn ohp-SYOH-nehs beh-heh-tah-RYAH-nahs?",
    phoneticEn: "Du iu jav ve-yi-te-ri-an op-shons?",
  },
  {
    cat: "diet",
    en: "Can you make it without meat?",
    es: "¿Lo pueden hacer sin carne?",
    phoneticEs: "Loh PWEH-dehn ah-SEHR seen KAHR-neh?",
    phoneticEn: "Kan iu meik it uid-aut miit?",
  },
  {
    cat: "pay",
    en: "Could we have the check, please?",
    es: "¿Nos trae la cuenta, por favor?",
    phoneticEs: "Nohs TRAH-eh lah KWEHN-tah, pohr fah-VOHR?",
    phoneticEn: "Kud ui jav de chek, pliis?",
  },
  {
    cat: "pay",
    en: "Can I pay with a card?",
    es: "¿Puedo pagar con tarjeta?",
    phoneticEs: "PWEH-doh pah-GAHR kohn tahr-HEH-tah?",
    phoneticEn: "Kan ai pei uid e kard?",
  },
  {
    cat: "pay",
    en: "Can we split the bill?",
    es: "¿Podemos dividir la cuenta?",
    phoneticEs: "poh-DEH-mohs dee-bee-DEER lah KWEHN-tah?",
    phoneticEn: "Kan ui split de bil?",
  },
  {
    cat: "pay",
    en: "Is the tip included?",
    es: "¿La propina está incluida?",
    phoneticEs: "Lah proh-PEE-nah ehs-TAH een-kloo-EE-dah?",
    phoneticEn: "Is de tip in-klu-did?",
  },
  {
    cat: "table",
    en: "A table for two, please.",
    es: "Una mesa para dos, por favor.",
    phoneticEs: "OO-nah MEH-sah PAH-rah dohs, pohr fah-VOHR.",
    phoneticEn: "E tei-bol for tu, pliis.",
  },
  {
    cat: "table",
    en: "What are your hours today?",
    es: "¿Cuál es su horario de hoy?",
    phoneticEs: "Kwahl ehs soo oh-RAH-ryoh deh oy?",
    phoneticEn: "Uat ar iur au-ers tu-dei?",
  },
  {
    cat: "table",
    en: "Where are the restrooms?",
    es: "¿Dónde están los baños?",
    phoneticEs: "DOHN-deh ehs-TAHN lohs BAH-nyohs?",
    phoneticEn: "Uer ar de rest-rums?",
  },
];

/* Curated dictionary for English -> Spanish phonetic respelling */
const EN_TO_ES_PHONETICS: Record<string, string> = {
  // Pronouns & Contractions
  i: "ai", im: "aim", "i'm": "aim", me: "mi", my: "mai",
  you: "iu", your: "iur", youre: "iur", "you're": "iur",
  he: "ji", his: "jis", him: "jim", she: "shi", her: "jer",
  it: "it", its: "its", "it's": "its", we: "ui", our: "auer",
  us: "as", they: "dei", their: "der", them: "dem",

  // Numbers & Quantities
  "1": "uan", "2": "tu", "3": "zri", "4": "for", "5": "faiv",
  "6": "siks", "7": "se-ven", "8": "eit", "9": "nain", "10": "ten",
  "11": "i-le-ven", "12": "tuelv", "15": "fif-tiin", "20": "tuen-ti",
  "25": "tuen-ti faiv", "50": "fif-ti", "100": "uan jan-dred",
  one: "uan", two: "tu", three: "zri", four: "for", five: "faiv",
  six: "siks", seven: "se-ven", eight: "eit", nine: "nain", ten: "ten",
  half: "jaf", quarter: "kuor-ter", pound: "paund", pounds: "paunds",
  lb: "paund", lbs: "paunds", oz: "auns", ounce: "auns", ounces: "aun-ses",
  slice: "slais", slices: "slai-ses", piece: "piis", pieces: "pii-ses", dozen: "da-zen",

  // Common Verbs & Auxiliaries
  would: "wud", could: "kud", should: "shud", like: "laik", want: "uont",
  need: "niid", have: "jav", has: "jas", had: "jad", do: "du", does: "das",
  did: "did", dont: "dount", "don't": "dount", is: "is", are: "ar", was: "uas",
  were: "uer", be: "bi", been: "bin", can: "kan", cant: "kant", "can't": "kant",
  will: "uil", wont: "uount", "won't": "uount", give: "giv", take: "teik",
  make: "meik", get: "get", put: "put", see: "sii", look: "luk", come: "kam",
  go: "gou", cut: "kat", sliced: "slaisd", shaved: "sheivd", chopped: "chopt",
  cooked: "kukt", baked: "beikt", fried: "fraid", grilled: "grild", pay: "pei",
  buy: "bai", sell: "sel", cost: "kost", accept: "ak-sept", open: "ou-pen",
  close: "klous", closed: "klousd", restock: "ri-stok", bring: "bring",
  show: "shou", help: "jelp", ask: "ask", call: "kol", know: "nou", think: "zink",

  // Food, Deli & Grocery
  ham: "jam", turkey: "ter-ki", beef: "biif", pork: "pork", chicken: "chi-ken",
  meat: "miit", bacon: "bei-kon", sausage: "so-sedzh", cheese: "chiis",
  cheddar: "che-dar", swiss: "suis", provolone: "pro-vo-loun", american: "a-me-ri-kan",
  bread: "bred", white: "uait", wheat: "uiit", rye: "rai", roll: "roul", rolls: "rouls",
  sandwich: "san-duich", sub: "sab", wrap: "rap", salad: "sa-lad", soup: "suup",
  egg: "eg", eggs: "egs", butter: "ba-ter", milk: "milk", water: "ua-ter",
  coffee: "ko-fi", tea: "tii", soda: "sou-da", juice: "yus", beer: "biir", wine: "uain",
  fruit: "frut", apple: "a-pl", banana: "ba-na-na", orange: "o-randzh",
  vegetables: "vedzh-te-bls", tomato: "to-mei-to", tomatoes: "to-mei-tos",
  onion: "o-nion", onions: "o-nions", lettuce: "le-tis", pickle: "pi-kl", pickles: "pi-kls",
  mayo: "mei-o", mustard: "mas-tard", ketchup: "ke-chap", sauce: "sos",
  oil: "oil", vinegar: "vi-ne-gar", salt: "solt", pepper: "pe-per", sugar: "shu-gar",

  // Adjectives
  thin: "dzin", thick: "dzik", hot: "jot", cold: "kold", warm: "uorm",
  fresh: "fresh", good: "gud", bad: "bad", sweet: "suiit", spicy: "spai-si",
  mild: "maild", small: "smol", medium: "mi-diom", large: "lary", extra: "eks-tra",
  little: "li-tl", more: "mor", less: "les", big: "big", new: "niu",

  // Prepositions, Conjunctions & Articles
  the: "de", a: "e", an: "an", and: "and", or: "or", of: "ov", to: "tu",
  in: "in", on: "on", at: "at", for: "for", with: "wid", without: "wid-aut",
  from: "from", by: "bai", about: "a-baut", as: "as", if: "if", than: "dan",
  then: "den", but: "bat", so: "sou",

  // Interrogatives & Adverbs
  where: "uer", what: "uat", when: "uen", why: "uai", who: "ju", how: "jau",
  much: "mach", many: "me-ni", here: "jiir", there: "der", now: "nau",
  today: "tu-dei", tonight: "tu-nait", tomorrow: "tu-mo-rou", yesterday: "ies-ter-dei",
  always: "ol-ueis", never: "ne-ver", please: "pliis", thank: "zenk", thanks: "zenks",
  yes: "ies", no: "nou", not: "not", very: "ve-ri", too: "tu", also: "ol-sou",

  // Store & Shopping Terms
  store: "stor", shop: "shop", market: "mar-ket", bakery: "bei-ke-ri",
  deli: "de-li", counter: "kaun-ter", aisle: "ail", cash: "kash", card: "kard",
  cards: "kards", credit: "kre-dit", debit: "de-bit", ebt: "i-bi-ti", snap: "snap",
  change: "cheindzh", receipt: "ri-siit", bag: "bag", box: "boks", total: "tou-tal",
  bill: "bil", check: "chek", price: "prais", dollar: "do-lar", dollars: "do-lars",
  cent: "sent", cents: "sents", hours: "au-ers", sunday: "san-dei", sundays: "san-deis",
  monday: "man-dei", mondays: "man-deis", tuesday: "tius-dei", wednesday: "uens-dei",
  thursday: "zers-dei", friday: "frai-dei", saturday: "sa-ter-dei", holiday: "jo-li-dei",
  holidays: "jo-li-deis", bathroom: "baz-rum", restroom: "rest-rum",
  groceries: "gro-se-ris", minimum: "mi-ni-mum", purchase: "per-ches",
};

function getRuleBasedPhonetic(rawWord: string): string {
  let w = rawWord.toLowerCase();
  w = w
    .replace(/tion\b/g, "shon")
    .replace(/sion\b/g, "shon")
    .replace(/ture\b/g, "cher")
    .replace(/ight\b/g, "ait")
    .replace(/igh/g, "ai")
    .replace(/eigh/g, "ei")
    .replace(/augh/g, "af")
    .replace(/ough/g, "of")
    .replace(/\bkn/g, "n")
    .replace(/\bwr/g, "r")
    .replace(/\bwh/g, "u")
    .replace(/ph/g, "f")
    .replace(/th/g, "d")
    .replace(/sh/g, "sh")
    .replace(/ch/g, "ch")
    .replace(/ck/g, "k")
    .replace(/qu/g, "ku")
    .replace(/ee/g, "i")
    .replace(/ea/g, "i")
    .replace(/oo/g, "u")
    .replace(/ou/g, "au")
    .replace(/ow\b/g, "ou")
    .replace(/ow/g, "au")
    .replace(/oa/g, "ou")
    .replace(/ai/g, "ei")
    .replace(/ay/g, "ei")
    .replace(/oy/g, "oi")
    .replace(/oi/g, "oi")
    .replace(/aw/g, "o")
    .replace(/au/g, "o")
    .replace(/ew/g, "iu")
    .replace(/\bh([aeiou])/g, "j$1")
    .replace(/\bw/g, "u")
    .replace(/w\b/g, "u")
    .replace(/c([eiy])/g, "s$1")
    .replace(/c([aou])/g, "k$1")
    .replace(/c\b/g, "k")
    .replace(/g([ei])/g, "y$1")
    .replace(/j/g, "y")
    .replace(/a([bcdfghjklmnpqrstvwxz])e\b/g, "ei$1")
    .replace(/i([bcdfghjklmnpqrstvwxz])e\b/g, "ai$1")
    .replace(/o([bcdfghjklmnpqrstvwxz])e\b/g, "ou$1")
    .replace(/u([bcdfghjklmnpqrstvwxz])e\b/g, "iu$1")
    .replace(/y\b/g, "i");
  return w;
}

function getEnglishPhoneticForSpanish(text: string): string {
  if (!text) return "";
  return text.replace(/([A-Za-z0-9']+)|([^A-Za-z0-9'\s]+)/g, (match, word, punct) => {
    if (punct) return punct;
    if (!word) return match;

    const lower = word.toLowerCase();
    let phoneticWord = EN_TO_ES_PHONETICS[lower];
    if (!phoneticWord) {
      phoneticWord = getRuleBasedPhonetic(word);
    }

    if (/^\d+$/.test(word)) {
      return phoneticWord;
    }
    if (word === word.toUpperCase() && word.length > 1) {
      return phoneticWord.toUpperCase();
    } else if (word[0] === word[0].toUpperCase()) {
      return phoneticWord.charAt(0).toUpperCase() + phoneticWord.slice(1);
    }
    return phoneticWord;
  });
}

function getSpanishPhoneticForEnglish(text: string): string {
  if (!text) return "";
  return text
    .replace(/¿/g, "")
    .replace(/ce|ci/gi, "seh")
    .replace(/ca|co|cu/gi, "kah")
    .replace(/ll/gi, "y")
    .replace(/j/gi, "h")
    .replace(/gui|gue/gi, "gee")
    .replace(/que|qui/gi, "keh")
    .replace(/ch/gi, "ch")
    .replace(/ñ/gi, "ny")
    .replace(/\s+/g, " ")
    .trim();
}

/* Helper to generate readable phonetic hint */
function getPhoneticHint(text: string, isSpanish: boolean): string {
  if (!text) return "";

  // Check preset phrases first for curated high-fidelity phonetics
  const clean = text.trim().toLowerCase();
  for (const p of CATEGORIZED_PHRASES) {
    if (isSpanish && p.es.toLowerCase().trim() === clean) {
      return p.phoneticEs;
    }
    if (!isSpanish && p.en.toLowerCase().trim() === clean) {
      return p.phoneticEn;
    }
  }

  // Target is Spanish -> provide English speaker phonetics
  if (isSpanish) {
    return getSpanishPhoneticForEnglish(text);
  }

  // Target is English -> provide Spanish speaker phonetics
  return getEnglishPhoneticForSpanish(text);
}

export default function TranslatorTab({ lang }: TranslatorTabProps) {
  const [sourceLang, setSourceLang] = useState<"en" | "es">("en");
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [starredPhrases, setStarredPhrases] = useState<string[]>([]);
  const [showCounterDisplay, setShowCounterDisplay] = useState(false);

  const recognitionRef = useRef<any>(null);
  const targetLang = sourceLang === "en" ? "es" : "en";

  /* ---------- Real-Time / On-Demand Translation ---------- */
  const handleTranslate = async (textToTranslate?: string) => {
    const text = (textToTranslate !== undefined ? textToTranslate : inputText).trim();
    if (!text) {
      setTranslatedText("");
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text,
          targetLang,
        }),
      });

      const data = await res.json();
      const resultText = data.translation || data.translated || text;
      setTranslatedText(resultText);
    } catch {
      setTranslatedText(text);
    } finally {
      setIsLoading(false);
    }
  };

  const isSwappingRef = useRef(false);

  /* ISSUE #1: TRANSLATE AUTOMATICALLY AS YOU TYPE (LIKE GOOGLE TRANSLATE) */
  useEffect(() => {
    if (isSwappingRef.current) return;
    const text = inputText.trim();
    if (!text) {
      setTranslatedText("");
      return;
    }

    const timer = setTimeout(() => {
      handleTranslate(text);
    }, 150); // 150ms instant debounce for live translation

    return () => clearTimeout(timer);
  }, [inputText, sourceLang]);

  /* ---------- Language Direction Switcher ---------- */
  const swapLanguages = () => {
    isSwappingRef.current = true;
    const newSource = sourceLang === "en" ? "es" : "en";
    setSourceLang(newSource);

    const currentInput = inputText;
    const currentTrans = translatedText;
    setInputText(currentTrans);
    setTranslatedText(currentInput);

    setTimeout(() => {
      isSwappingRef.current = false;
    }, 350);
  };

  const latestTranscriptRef = useRef<string>("");

  /* ---------- Speech-to-Text (Voice Dictation) ---------- */
  const toggleListening = () => {
    if (typeof window === "undefined") return;

    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        lang === "es"
          ? "Reconocimiento de voz no soportado en este navegador."
          : "Speech recognition not supported in this browser."
      );
      return;
    }

    if (isListening) {
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    try {
      latestTranscriptRef.current = "";
      const recognition = new SpeechRecognition();
      recognition.lang = sourceLang === "en" ? "en-US" : "es-ES";
      recognition.interimResults = true;
      recognition.continuous = false;

      recognition.onstart = () => {
        setIsListening(true);
        latestTranscriptRef.current = "";
      };

      recognition.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0].transcript)
          .join("");
        latestTranscriptRef.current = transcript;
        setInputText(transcript);
      };

      recognition.onerror = () => setIsListening(false);

      recognition.onend = () => {
        setIsListening(false);
        const voiceText = latestTranscriptRef.current.trim();
        if (voiceText) {
          handleTranslate(voiceText);
        }
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch {
      setIsListening(false);
    }
  };

  /* ---------- Text-to-Speech (Audio Pronunciation) ---------- */
  const speakText = (text: string, speakLang: "es" | "en") => {
    if (typeof window === "undefined" || !("speechSynthesis" in window) || !text) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = speakLang === "es" ? "es-ES" : "en-US";
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  /* ---------- Copy to Clipboard ---------- */
  const copyTranslation = () => {
    if (!translatedText) return;
    navigator.clipboard.writeText(translatedText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  /* ---------- Star/Unstar Phrase ---------- */
  const toggleStar = (phrase: string) => {
    if (starredPhrases.includes(phrase)) {
      setStarredPhrases(starredPhrases.filter((p) => p !== phrase));
    } else {
      setStarredPhrases([...starredPhrases, phrase]);
    }
  };

  const filteredPhrases = CATEGORIZED_PHRASES.filter(
    (p) => selectedCategory === "all" || p.cat === selectedCategory
  );

  const phoneticHint = translatedText
    ? getPhoneticHint(translatedText, targetLang === "es")
    : "";

  return (
    <div className="w-full max-w-md md:max-w-2xl lg:max-w-4xl mx-auto p-4 lg:px-10 lg:pt-10 pb-32 lg:pb-10 flex flex-col gap-3">
      {/* LANGUAGE DIRECTION BAR */}
      <div className="bg-white rounded-full border border-white shadow-soft p-2 flex items-center justify-between">
        <div className="flex-1 text-center font-extrabold text-xs text-slate-800 uppercase tracking-wide">
          {sourceLang === "en" ? "English" : "Español"}
        </div>

        <button
          onClick={swapLanguages}
          className="p-2 rounded-xl bg-slate-100 text-[#0A5CFF] hover:bg-blue-50 hover:scale-105 transition-all shadow-2xs"
          title="Swap Languages / Cambiar Idioma"
        >
          <ArrowRightLeft className="w-4 h-4" />
        </button>

        <div className="flex-1 text-center font-extrabold text-xs text-slate-800 uppercase tracking-wide">
          {targetLang === "es" ? "Español" : "English"}
        </div>
      </div>

      {/* ISSUE #2 LAYOUT FIX: OUTPUT TRANSLATION CARD PLACED FIRST (VISIBLE ABOVE MOBILE KEYBOARD) */}
      <div className="bg-slate-900 text-white rounded-2xl border border-slate-800 shadow-md p-3.5 space-y-2 relative">
        <div className="flex items-center justify-between text-xs font-black tracking-wider text-blue-400 uppercase">
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            <span>{targetLang === "es" ? "Traducción (Español)" : "Translation (English)"}</span>
          </span>

          {isLoading && <Loader2 className="w-3.5 h-3.5 text-blue-400 animate-spin" />}

          {translatedText && !isLoading && (
            <div className="flex items-center gap-1.5">
              {/* Full-Screen Show Counter Display Button */}
              <button
                onClick={() => setShowCounterDisplay(true)}
                className="px-2 py-0.5 rounded-lg bg-blue-500/20 text-blue-300 border border-blue-500/40 text-[10px] font-extrabold flex items-center gap-1 hover:bg-blue-500/30 transition-all"
                title="Show giant text on counter display"
              >
                <Tv className="w-3 h-3 text-blue-400" />
                <span>{lang === "es" ? "Ver Grande" : "Show Counter"}</span>
              </button>

              <button
                onClick={copyTranslation}
                className="p-1 rounded-lg bg-white/10 hover:bg-white/20 text-slate-300 transition-colors"
                title="Copy / Copiar"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>

              <button
                onClick={() => speakText(translatedText, targetLang)}
                className="p-1 rounded-lg bg-white/10 hover:bg-white/20 text-blue-400 transition-colors"
                title="Listen / Escuchar"
              >
                <Volume2 className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>

        <div className="space-y-1">
          <div className="min-h-[46px] text-base font-bold leading-relaxed text-slate-100">
            {translatedText ? (
              translatedText
            ) : (
              <span className="text-slate-500 font-normal italic text-sm">
                {lang === "es"
                  ? "Traduce automáticamente al escribir…"
                  : "Translates automatically as you type…"}
              </span>
            )}
          </div>

          {/* Phonetic Pronunciation Guide (Full Text Wrapping & No Emojis) */}
          {translatedText && phoneticHint && (
            <div className="pt-2 border-t border-white/10 flex items-start gap-2 text-xs text-amber-300/90 font-medium">
              <span className="font-bold text-[10px] uppercase tracking-wider text-amber-400/90 shrink-0 pt-0.5">
                {targetLang === "es" ? "Pronunciation:" : "Pronunciación:"}
              </span>
              <span className="italic whitespace-normal break-words leading-snug">{phoneticHint}</span>
            </div>
          )}
        </div>
      </div>

      {/* INPUT CARD (Text Area + Voice Dictation + Clear) */}
      <div className="bg-white rounded-[28px] border border-white shadow-soft p-4 space-y-2 relative">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500">
          <span>{sourceLang === "en" ? "Source Text" : "Texto de Origen"}</span>
          {inputText && (
            <button
              onClick={() => {
                setInputText("");
                setTranslatedText("");
              }}
              className="text-slate-400 hover:text-slate-600 flex items-center gap-1 text-[11px]"
            >
              <X className="w-3.5 h-3.5" />
              <span>{lang === "es" ? "Borrar" : "Clear"}</span>
            </button>
          )}
        </div>

        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={
            sourceLang === "en"
              ? "Type or speak text..."
              : "Escriba o hable..."
          }
          rows={3}
          className="w-full text-base font-medium text-slate-900 placeholder:text-slate-400 bg-transparent border-0 focus:outline-none focus:ring-0 resize-none"
        />

        <div className="flex items-center justify-between pt-1.5 border-t border-slate-100">
          <div className="flex items-center gap-2">
            {/* Voice Dictation Button */}
            <button
              onClick={toggleListening}
              className={`p-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all ${
                isListening
                  ? "bg-rose-500 text-white animate-pulse"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4 text-[#0A5CFF]" />}
              <span>{isListening ? (lang === "es" ? "Escuchando…" : "Listening…") : (lang === "es" ? "Hablar" : "Voice")}</span>
            </button>

            {/* Audio Listen for Source */}
            {inputText && (
              <button
                onClick={() => speakText(inputText, sourceLang)}
                className="p-2 rounded-xl bg-slate-100 text-slate-600 hover:text-[#0A5CFF] transition-colors"
                title="Listen / Escuchar"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* CATEGORIZED STORE PHRASES WITH STAR FAVORITES */}
      <div className="space-y-2 pt-1">
        <div className="flex items-center justify-between">
          <span className="text-xs font-black text-slate-800 uppercase tracking-wider">
            {lang === "es" ? "Frases útiles para el restaurante" : "Useful restaurant phrases"}
          </span>
        </div>

        {/* Category Filter Chips */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
          {PHRASE_CATEGORIES.map((cat) => {
            const Icon = cat.icon;
            const isSelected = selectedCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold flex items-center gap-1.5 shrink-0 transition-all ${
                  isSelected
                    ? "bg-[#0A5CFF] text-white shadow-2xs"
                    : "bg-white text-on-surface-variant border border-white shadow-soft hover:text-on-surface"
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{lang === "es" ? cat.labelEs : cat.labelEn}</span>
              </button>
            );
          })}
        </div>

        {/* Preset Phrase Cards - Full length of page without truncation */}
        <div className="space-y-2 pb-6 lg:space-y-0 lg:grid lg:grid-cols-2 lg:gap-3">
          {filteredPhrases.map((phrase, idx) => {
            const displayPhrase = sourceLang === "en" ? phrase.en : phrase.es;
            const targetPhrase = sourceLang === "en" ? phrase.es : phrase.en;
            const isStarred = starredPhrases.includes(displayPhrase);

            return (
              <div
                key={idx}
                onClick={() => {
                  setInputText(displayPhrase);
                  setTranslatedText(targetPhrase);
                }}
                className="p-4 bg-white border border-white shadow-soft rounded-3xl flex items-center justify-between gap-2 hover:shadow-lift cursor-pointer transition-all shadow-2xs group"
              >
                <div className="space-y-0.5 text-left">
                  <div className="text-[14px] font-bold text-on-surface group-hover:text-primary transition-colors">
                    {displayPhrase}
                  </div>
                  <div className="text-[13px] font-medium text-on-surface-variant italic">
                    {targetPhrase}
                  </div>
                </div>

                <div className="flex items-center gap-1 shrink-0">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleStar(displayPhrase);
                    }}
                    className={`p-1.5 rounded-lg transition-colors ${
                      isStarred ? "text-amber-500 bg-amber-50" : "text-slate-300 hover:text-amber-400"
                    }`}
                  >
                    <Star className="w-4 h-4 fill-current" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      speakText(targetPhrase, targetLang);
                    }}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-[#0A5CFF] hover:bg-blue-50 transition-colors"
                  >
                    <Volume2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* FULL-SCREEN COUNTER DISPLAY MODAL (GIANT TEXT FOR CASHIER/CUSTOMER) */}
      {showCounterDisplay && (
        <div className="fixed inset-0 z-50 bg-slate-950/95 backdrop-blur-xl flex flex-col justify-between p-6 animate-in fade-in zoom-in-95 duration-200">
          {/* Top Bar */}
          <div className="flex items-center justify-between text-white border-b border-white/10 pb-4">
            <div className="flex items-center gap-2">
              <Tv className="w-5 h-5 text-blue-400" />
              <span className="text-xs font-black uppercase tracking-widest text-blue-400">
                {lang === "es" ? "Pantalla de Mostrador" : "Counter Display"}
              </span>
            </div>

            <button
              onClick={() => setShowCounterDisplay(false)}
              className="p-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Main Giant Text Display */}
          <div className="flex-1 flex flex-col items-center justify-center text-center px-4">
            <span className="text-xs font-extrabold text-blue-400 uppercase tracking-widest mb-3">
              {targetLang === "es" ? "Traducción para Mostrador:" : "Counter Translation:"}
            </span>

            <div className="text-3xl md:text-5xl font-black text-white leading-tight tracking-wide drop-shadow-md">
              {translatedText || inputText}
            </div>

            {inputText && (
              <div className="text-sm font-semibold text-slate-400 italic mt-6 border-t border-white/10 pt-3 max-w-lg">
                "{inputText}"
              </div>
            )}
          </div>

          {/* Bottom Action Controls */}
          <div className="flex items-center justify-center gap-3 pt-4 border-t border-white/10">
            <button
              onClick={() => speakText(translatedText || inputText, targetLang)}
              className="py-3 px-6 rounded-2xl bg-[#0A5CFF] text-white font-extrabold text-sm flex items-center gap-2 shadow-lg hover:brightness-110 transition-all"
            >
              <Volume2 className="w-5 h-5" />
              <span>{lang === "es" ? "Escuchar en Voz Alta" : "Speak Out Loud"}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
