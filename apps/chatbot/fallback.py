"""Agricultural knowledge base for the CornHouse chatbot.

Provides specific, actionable maize farming advice for farmers in Cameroon
when a response is needed without the external AI backend.
"""

import re
from typing import Optional


def get_fallback_reply(message: Optional[str]) -> str:  # noqa: C901
    if not message:
        return (
            "Hello! I'm your CornHouse agricultural assistant. "
            "Ask me anything about maize farming — planting, pests, fertilizers, harvesting, or market prices."
        )

    m = message.lower()

    # ── Greetings (use word boundaries for short tokens to avoid matching 'hi' in 'which') ──
    _greet_long = ("hello", "bonjour", "salut", "good morning", "good afternoon")
    _greet_short = (r"\bhi\b", r"\bhey\b")
    if any(k in m for k in _greet_long) or any(re.search(p, m) for p in _greet_short):
        return (
            "Hello! I'm your CornHouse agricultural assistant, here to help you grow better maize. "
            "You can ask me about planting schedules, pest control, fertilizer, irrigation, harvesting, "
            "storage, or market prices. What would you like to know?"
        )

    # ── Planting / seeds / sowing ───────────────────────────────────────────────
    if any(k in m for k in ("plant", "planting", "seed", "sow", "sowing", "germination", "seedling", "nursery")):
        return (
            "🌱 **Maize Planting Guide for Cameroon:**\n\n"
            "• **Best seasons:** March–April (long rains) and August–September (short rains).\n"
            "• **Seed depth:** Plant 2–3 cm deep in well-drained, loamy soil.\n"
            "• **Spacing:** 75 cm between rows, 25–30 cm between plants.\n"
            "• **Germination:** Expect seedlings in 5–10 days when soil temperature is 18–32°C.\n"
            "• **Seed rate:** Use 15–20 kg of certified seed per hectare.\n"
            "• **Tip:** Choose drought-tolerant hybrid varieties like POSPMS or Oba Super for higher yields."
        )

    # ── Pests / insects ─────────────────────────────────────────────────────────
    if any(k in m for k in ("pest", "insect", "bug", "worm", "caterpillar", "armyworm",
                             "fall armyworm", "aphid", "borer", "stemborer", "weevil")):
        return (
            "🐛 **Pest Management for Maize:**\n\n"
            "• **Fall Armyworm (FAW):** The most destructive pest. Look for ragged leaf edges and frass "
            "in the whorl. Apply neem-based biopesticides or Emamectin benzoate (Proclaim) early.\n"
            "• **Stem borers:** Check for dead hearts and entry holes. Use Carbofuran granules in the "
            "whorl at 3–4 weeks.\n"
            "• **Aphids:** Spray with diluted neem oil (5 ml/L water) or insecticidal soap.\n"
            "• **Storage weevils:** Sun-dry grain to below 13% moisture; use hermetic bags or PICS bags.\n"
            "• **Prevention:** Rotate crops yearly, destroy crop residues, and scout fields weekly."
        )

    # ── Disease / fungal / blight / virus ──────────────────────────────────────
    if any(k in m for k in ("disease", "blight", "rust", "fungus", "mould", "mold",
                             "smut", "streak", "mosaic", "virus")):
        return (
            "🦠 **Maize Disease Management:**\n\n"
            "• **Gray leaf spot & Northern blight:** Use resistant varieties; avoid overhead irrigation.\n"
            "• **Maize streak virus (MSV):** Transmitted by leafhoppers — control with imidacloprid seed dressing.\n"
            "• **Ear rots (Fusarium/Aspergillus):** Harvest promptly when husks dry; avoid field moisture at maturity.\n"
            "• **Smut:** Remove and destroy galls before they burst; avoid mechanical injury to plants.\n"
            "• **General tip:** Apply foliar fungicide (e.g., Mancozeb) during tasseling if disease pressure is high."
        )

    # ── Fertilizer / nutrients ──────────────────────────────────────────────────
    if any(k in m for k in ("fertil", "manure", "compost", "npk", "nitrogen",
                             "phosphorus", "potassium", "nutrient", "urea", "dap", "top dress")):
        return (
            "🧪 **Fertilizer Guide for Maize in Cameroon:**\n\n"
            "• **Basal application (at planting):** Apply 60 kg/ha of DAP (18-46-0) or NPK 15-15-15.\n"
            "• **Top dressing (3–4 weeks after planting):** Apply 100 kg/ha of Urea (46-0-0) for nitrogen boost.\n"
            "• **Second top dressing (7–8 weeks):** Add another 50 kg/ha Urea at tasseling stage.\n"
            "• **Organic:** Incorporate 5–10 tonnes/ha of well-composted manure before planting.\n"
            "• **Soil test:** Get a soil test for precise recommendations — contact your local MINADER extension office.\n"
            "• **Warning:** Do not over-apply nitrogen — it causes leafy growth but poor grain fill."
        )

    # ── Fertilizer / nutrients (checked before water to catch NPK/urea) ─────────
    if any(k in m for k in ("fertil", "manure", "compost", "npk", "nitrogen",
                             "phosphorus", "potassium", "nutrient", "urea", "dap", "top dress")):
        return (
            "🧪 **Fertilizer Guide for Maize in Cameroon:**\n\n"
            "• **Basal application (at planting):** Apply 60 kg/ha of DAP (18-46-0) or NPK 15-15-15.\n"
            "• **Top dressing (3–4 weeks after planting):** Apply 100 kg/ha of Urea (46-0-0) for nitrogen boost.\n"
            "• **Second top dressing (7–8 weeks):** Add another 50 kg/ha Urea at tasseling stage.\n"
            "• **Organic:** Incorporate 5–10 tonnes/ha of well-composted manure before planting.\n"
            "• **Soil test:** Get a soil test for precise recommendations — contact your local MINADER extension office.\n"
            "• **Warning:** Do not over-apply nitrogen — it causes leafy growth but poor grain fill."
        )

    # ── Storage / aflatoxin (checked before water to catch 'moisture' in storage context) ──
    if any(k in m for k in ("stor", "silo", "aflatoxin", "mycotoxin", "preserve", "warehouse", "hermetic", "pics bag")):
        return (
            "🏚️ **Maize Storage Best Practices:**\n\n"
            "• **Moisture:** Dry grain to below 13% before storage to prevent mould and aflatoxin.\n"
            "• **Hermetic storage:** Use PICS bags (triple-layer) or metal silos to eliminate oxygen "
            "and prevent weevils without chemicals.\n"
            "• **Fumigation:** If using conventional bags, apply Phostoxin tablets (aluminium phosphide) "
            "— handle with care, it is toxic.\n"
            "• **Aflatoxin:** Never store visibly mouldy grain — it contains carcinogenic aflatoxins. Discard or compost it.\n"
            "• **Duration:** Well-dried grain in hermetic bags can be safely stored for 12–18 months."
        )

    # ── Irrigation / water / rainfall / drought ─────────────────────────────────
    if any(k in m for k in ("water", "rain", "irrigat", "drought", "moisture", "flood")):
        return (
            "💧 **Water & Irrigation Tips:**\n\n"
            "• Maize needs about 500–800 mm of rainfall during the growing season.\n"
            "• **Critical stages:** Ensure adequate moisture during germination, tasseling, and grain fill.\n"
            "• **Drought stress:** If rain fails for 2+ weeks during tasseling, plants can lose 50% yield. "
            "Use drought-tolerant varieties (e.g., DTMA hybrids) in low-rainfall areas.\n"
            "• **Flooding:** Ensure good field drainage; waterlogged soil for 48+ hours can kill roots.\n"
            "• **Tip:** Mulching with crop residue retains soil moisture and reduces irrigation needs by 30%."
        )

    # ── Harvest / yield / maturity ──────────────────────────────────────────────
    if any(k in m for k in ("harvest", "harvesting", "mature", "maturity", "cob", "grain", "drying", "yield")):
        return (
            "🌽 **Harvesting Maize:**\n\n"
            "• **Signs of maturity:** Black layer forms at the base of the grain; husks turn brown and dry.\n"
            "• **Timing:** Most varieties mature in 90–120 days after planting.\n"
            "• **Moisture at harvest:** Harvest at 20–25% grain moisture; dry down to 13% before storage.\n"
            "• **Drying:** Spread cobs on raised drying racks in the sun for 7–14 days or use a grain dryer.\n"
            "• **Yield targets:** Good management can yield 3–6 tonnes/ha of shelled grain.\n"
            "• **Shelling:** Use a hand sheller or mechanical sheller to minimise grain damage."
        )

    # ── Market / price / sell ───────────────────────────────────────────────────
    if any(k in m for k in ("market", "price", "sell", "selling", "profit", "income", "money", "buyer", "trader")):
        return (
            "📈 **Maize Marketing Tips:**\n\n"
            "• **Best selling time:** Prices are highest 3–5 months after harvest when supply drops — "
            "avoid panic selling at harvest.\n"
            "• **Check prices:** Monitor MINCOMMERCE price boards or call aggregators in Douala, "
            "Yaoundé, and Bafoussam markets.\n"
            "• **Group selling:** Join a farmer cooperative to negotiate better prices in bulk.\n"
            "• **Value addition:** Drying and grading your grain can add a 15–25% price premium over "
            "raw wet grain.\n"
            "• **CornHouse marketplace:** List your produce on the CornHouse marketplace to reach "
            "certified buyers directly."
        )

    # ── Soil / land preparation / tillage / weeds ────────────────────────────────
    if any(k in m for k in ("soil", "land", "till", "plough", "prepare", "clear", "weed", "herbicide", "hoe")):
        return (
            "🌍 **Soil Preparation & Weed Control:**\n\n"
            "• **Land prep:** Plough 20–25 cm deep 2–3 weeks before planting to break hardpan and bury weeds.\n"
            "• **pH:** Maize prefers soil pH of 5.8–7.0. Apply agricultural lime if soil is too acidic.\n"
            "• **Pre-emergence herbicide:** Apply Atrazine (2 L/ha) within 3 days of planting before "
            "weeds emerge.\n"
            "• **Post-emergence:** Use Primextra Gold or hand-weed at 2–3 and 5–6 weeks after planting.\n"
            "• **Crop rotation:** Rotate with legumes (groundnut, soybean) to improve soil nitrogen naturally."
        )

    # ── Variety / hybrid / seed type ─────────────────────────────────────────────
    if any(k in m for k in ("variety", "hybrid", "improved", "open pollinated", "opv", "seed type")):
        return (
            "🌾 **Recommended Maize Varieties for Cameroon:**\n\n"
            "• **Hybrids (high yield):** DK8031, H614D, SC403 — yield 5–8 t/ha under good management.\n"
            "• **OPVs (open-pollinated):** Oba Super 1 & 2, TZSR-W — can save seed; yield 3–5 t/ha.\n"
            "• **Drought-tolerant:** DTMA, WE3128 — for areas with irregular rainfall.\n"
            "• **Early maturing:** CMS 8704 — matures in 85–90 days, good for short rain seasons.\n"
            "• **Source:** Buy certified seed from IRAD Cameroon, Pioneer, or Syngenta-authorised dealers only."
        )

    # ── Grant / finance / loan ────────────────────────────────────────────────────
    if any(k in m for k in ("grant", "loan", "finance", "fund", "support", "subsidy", "credit", "bank")):
        return (
            "💰 **Financial Support for Farmers:**\n\n"
            "• **CornHouse Grants:** Apply for farming grants through the CornHouse Finance section — "
            "track your application status in your dashboard.\n"
            "• **Government:** MINADER and PNDP offer farmer support programmes — contact your local "
            "agricultural delegate.\n"
            "• **Microfinance:** CamCCUL and Advans Cameroun offer agricultural loans with flexible terms.\n"
            "• **Tip:** Keep farm records (planting dates, costs, yields) to strengthen your loan application."
        )

    # ── Default: helpful overview ─────────────────────────────────────────────────
    return (
        "🌽 **CornHouse Agricultural Assistant:**\n\n"
        "I can help you with all aspects of maize farming in Cameroon. Here are topics I advise on:\n\n"
        "• 🌱 **Planting** — timing, spacing, seed selection\n"
        "• 🐛 **Pests & Diseases** — identification and control\n"
        "• 🧪 **Fertilizers** — NPK recommendations, composting\n"
        "• 💧 **Irrigation & Water** — drought management\n"
        "• 🌽 **Harvesting** — maturity signs, drying, yield\n"
        "• 🏚️ **Storage** — aflatoxin prevention, hermetic bags\n"
        "• 📈 **Markets** — pricing, selling strategies\n"
        "• 💰 **Grants & Finance** — CornHouse grants, loans\n\n"
        "Just type your question and I'll give you specific advice!"
    )
