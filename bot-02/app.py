from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# ──────────────────────────────────────────────
# DUMMY DENTAL KNOWLEDGE BASE
# ──────────────────────────────────────────────

DENTAL_RESPONSES = {
    "brushing": [
        "**Brushing Tips from Dr. Denta 🪥**\n\nBrush your teeth at least **twice a day** — morning and before bed. Use a soft-bristled toothbrush and fluoride toothpaste.\n\n- Hold the brush at a **45° angle** to your gums\n- Use gentle, circular motions — never scrub hard\n- Brush for a full **2 minutes** each session\n- Don't forget your tongue — it harbors bacteria too!\n\nReplace your toothbrush every **3–4 months**, or sooner if bristles are frayed.",
    ],
    "floss": [
        "**Flossing: The Step Most People Skip 🧵**\n\nFlossing removes plaque and food from between teeth where your toothbrush simply cannot reach. You should floss **at least once a day**, ideally before bedtime.\n\n- Use about **18 inches** of floss, winding most around your middle fingers\n- Gently slide it between teeth using a **C-shape** motion around each tooth\n- Don't snap it into the gums — be gentle!\n\nIf traditional floss is tricky, try **floss picks** or a **water flosser**. Any flossing is better than none.",
    ],
    "cavity": [
        "**About Cavities (Dental Caries) 🔍**\n\nCavities are permanently damaged areas in your tooth enamel caused by bacteria, sugary foods, and poor oral hygiene. Early signs include:\n\n- **Tooth sensitivity** to hot, cold, or sweet foods\n- Visible **holes or pits** in teeth\n- **Mild to sharp pain** when biting\n- **Brown, black, or white staining** on a tooth surface\n\nIf you suspect a cavity, see your dentist soon. Early cavities can be treated with a simple **filling**, but untreated ones may require a crown or root canal.",
        "**Signs You Might Have a Cavity**\n\nCavities don't always hurt right away — that's what makes them sneaky! Common warning signs:\n\n- Toothache or **spontaneous pain** with no obvious cause\n- **Sensitivity** when eating something sweet, hot, or cold\n- A **visible hole** or dark spot on your tooth\n- Pain when you **bite down**\n\nOnly a dentist can confirm a cavity with an X-ray. Small cavities are cheap and quick to fix — large ones are not!",
    ],
    "whitening": [
        "**Teeth Whitening Options ✨**\n\nThere are several safe ways to brighten your smile:\n\n- **In-office whitening** (dentist-applied): Fastest results, usually 1–2 shades in one visit using professional-grade peroxide gel\n- **Take-home trays** (from your dentist): Custom-fitted trays with whitening gel worn for 1–2 hours daily over 2 weeks\n- **Over-the-counter strips**: Accessible and affordable, though results are more gradual\n- **Whitening toothpaste**: Removes surface stains only, doesn't change underlying tooth color\n\n⚠️ Whitening won't work on **crowns, veneers, or fillings**. Always consult your dentist before starting.",
    ],
    "braces": [
        "**Braces vs. Invisalign — Which Is Right for You? 😁**\n\n**Traditional Braces:**\n- Metal brackets bonded to teeth with wires\n- Best for **complex alignment issues**\n- Always working (you can't remove them)\n- More noticeable appearance\n- Typically **$3,000–$7,000**\n\n**Invisalign (Clear Aligners):**\n- Removable clear plastic trays\n- Great for **mild to moderate** issues\n- Nearly invisible\n- Must be worn **20–22 hours/day** for effectiveness\n- Typically **$4,000–$8,000**\n\nYour orthodontist will recommend the best option based on your specific bite and alignment needs.",
    ],
    "implant": [
        "**Dental Implants — A Permanent Tooth Replacement 🔩**\n\nImplants are titanium posts surgically placed into the jawbone, acting as an artificial tooth root. They're topped with a crown that looks and functions like a natural tooth.\n\n**Pros:**\n- **Permanent** — can last a lifetime with proper care\n- Preserves **jawbone** (prevents bone loss)\n- Looks and feels completely natural\n\n**The Process:**\n1. Implant placement (surgery)\n2. Healing/osseointegration (3–6 months)\n3. Abutment and crown fitting\n\nCost: typically **$3,000–$5,000 per tooth**. Good bone density is required — your dentist will evaluate this.",
    ],
    "toothache": [
        "**Toothache — What To Do 🚨**\n\nA toothache can signal anything from sensitivity to an abscess. Immediate relief steps:\n\n- **Rinse** with warm salt water to reduce inflammation\n- Take **over-the-counter pain relievers** (ibuprofen works well for dental pain)\n- Apply a **cold pack** to your cheek — 20 min on, 20 off\n- Avoid **very hot, cold, or sweet** foods that trigger pain\n- **Clove oil** (eugenol) can temporarily numb the area\n\n⚠️ **See a dentist promptly** — especially if you have fever, swelling, or pain radiating to your jaw/ear. These can indicate a serious infection.",
    ],
    "gum": [
        "**Gum (Periodontal) Health 🩸**\n\nHealthy gums are **firm, pink**, and don't bleed during brushing. Warning signs of gum disease:\n\n- **Bleeding** when you brush or floss\n- **Red, swollen, or tender** gums\n- Persistent **bad breath**\n- Gums **pulling away** from teeth\n- **Loose teeth** in adults\n\nGum disease progresses from **gingivitis** (reversible) to **periodontitis** (requires professional treatment). Daily flossing and cleanings every 6 months are your best prevention.",
    ],
    "bad breath": [
        "**Bad Breath (Halitosis) — Causes & Solutions 🌬️**\n\nBad breath usually originates from bacteria on the **tongue, teeth, and gums**. Common causes:\n\n- **Poor oral hygiene** — bacteria produce sulfur compounds\n- **Dry mouth** — saliva washes away bacteria; less saliva = more odor\n- **Certain foods** — garlic, onions, coffee\n- **Gum disease** or **cavities**\n\n**Solutions:**\n- Brush *and* scrape your tongue daily\n- Drink plenty of water\n- Chew sugar-free gum to stimulate saliva\n- Regular dental checkups to rule out gum disease",
    ],
    "root canal": [
        "**Root Canal Treatment — Demystified 🦷**\n\nA root canal removes infected or damaged pulp to save the tooth from extraction. Modern root canals are **no more painful than getting a filling**.\n\n**The Procedure:**\n1. Local anesthesia is applied — you'll be numb\n2. A small opening is made in the tooth\n3. Infected pulp is removed and canals are cleaned\n4. Canals are filled and sealed\n5. A **crown** is usually placed afterward\n\n**Recovery:** Mild soreness for 1–2 days, manageable with OTC pain relievers. Most people return to normal activities the next day.",
    ],
    "children": [
        "**Children's Dental Health 👶**\n\nGood habits start early!\n\n- **First tooth = first dentist visit** — schedule within 6 months of the first tooth\n- Start brushing as soon as teeth appear, using a **rice-grain amount** of fluoride toothpaste\n- At age 3, switch to a **pea-sized amount**\n- Begin **flossing** when two teeth touch\n- Limit **sugary drinks** — juice and milk left on teeth overnight cause cavities\n- **Sealants** at age 6–7 protect molars from decay\n\nChildren should visit the dentist **every 6 months**. Making visits positive early prevents dental anxiety for life!",
    ],
    "checkup": [
        "**How Often Should You Visit the Dentist? 📅**\n\nThe standard recommendation is **every 6 months**. These visits include:\n\n- **Professional cleaning** — removes tartar that brushing can't\n- **X-rays** (typically once a year) — catch hidden decay\n- **Oral cancer screening** — quick and painless\n- **Gum measurement** — tracking gum health\n\nSome people need visits every **3–4 months** — those with gum disease, high cavity risk, or compromised immune systems. Prevention is always cheaper than treatment!",
    ],
    "diet": [
        "**Foods That Help (and Hurt) Your Teeth 🍎**\n\n**Tooth-friendly foods:**\n- **Cheese & dairy** — calcium, neutralizes acid\n- **Leafy greens** — rich in calcium and folic acid\n- **Apples & carrots** — crunchy, stimulates saliva\n- **Water (fluoridated)** — rinses away bacteria\n\n**Foods to limit:**\n- **Sugary snacks & drinks** — feed cavity-causing bacteria\n- **Citrus fruits & soda** — acidic, erodes enamel\n- **Sticky candies** — cling to teeth for hours\n\nTip: After eating acidic or sugary foods, rinse with water and wait **30 minutes** before brushing.",
    ],
    "sensitive": [
        "**Tooth Sensitivity — Why It Happens 😬**\n\nSensitivity occurs when **dentin** (the layer beneath enamel) becomes exposed, causing sharp pain with hot, cold, sweet, or acidic foods.\n\n**Common causes:**\n- **Worn enamel** from aggressive brushing or acidic diet\n- **Receding gums** exposing root surfaces\n- **Cracked teeth** or **teeth grinding** (bruxism)\n\n**Relief options:**\n- Use **sensitivity toothpaste** (potassium nitrate or stannous fluoride)\n- Switch to a **soft-bristled toothbrush**\n- Avoid highly acidic foods\n- Ask your dentist about **fluoride varnish** for severe cases",
    ],
}

GREETINGS = [
    "Hello! I'm **Dr. Denta**, your AI dental assistant 🦷\n\nI'm here to answer your dental health questions. You can ask me about:\n- Brushing and flossing techniques\n- Cavities, gum disease, or bad breath\n- Dental procedures like root canals or implants\n- Teeth whitening or braces\n- Children's dental health\n\nWhat's on your mind today?",
    "Hi there! Welcome to your dental consultation with **Dr. Denta** 😊\n\nFeel free to ask about any dental concern — hygiene tips, symptoms, procedures, or anything else oral-health related. How can I help you today?",
]

FALLBACK_RESPONSES = [
    "That's a great question! Here are some general dental health fundamentals:\n\n- **Brush twice daily** with fluoride toothpaste\n- **Floss once a day** to clean between teeth\n- **Visit your dentist every 6 months** for a checkup and cleaning\n- **Drink water** throughout the day to rinse away bacteria\n- **Limit sugary snacks and drinks**\n\nFor specific concerns or symptoms, I always recommend scheduling an appointment with a licensed dentist. Is there a specific topic I can help you with?",
    "Great question! For detailed advice on that, a licensed dentist is always your best resource.\n\nIn the meantime, maintaining oral health comes down to these fundamentals:\n\n- **Consistent brushing and flossing** — the foundation of everything\n- **Regular professional cleanings** every 6 months\n- **A tooth-friendly diet** low in sugar and acid\n- **Staying hydrated** — saliva is your mouth's natural defense\n\nFeel free to ask me about specific topics like cavities, gum disease, whitening, braces, or implants!",
]

KEYWORDS = {
    "brushing": ["brush", "brushing", "toothbrush", "technique", "how to brush"],
    "floss": ["floss", "flossing", "between teeth", "interdental"],
    "cavity": ["cavity", "cavities", "decay", "filling", "hole in tooth", "tooth decay", "caries"],
    "whitening": ["whiten", "whitening", "white teeth", "bleach", "brighten", "stain"],
    "braces": ["brace", "braces", "invisalign", "aligner", "orthodont", "crooked teeth", "straight"],
    "implant": ["implant", "implants", "missing tooth", "tooth replacement", "artificial tooth"],
    "toothache": ["toothache", "tooth pain", "throbbing", "ache", "hurts", "sore tooth"],
    "gum": ["gum", "gums", "bleed", "bleeding", "periodon", "gingivit", "swollen gum"],
    "bad breath": ["bad breath", "halitosis", "smell", "odor", "breath"],
    "root canal": ["root canal", "pulp", "infected tooth", "nerve", "endodont"],
    "children": ["child", "children", "kid", "baby", "infant", "toddler", "pediatric"],
    "checkup": ["checkup", "check up", "how often", "cleaning", "appointment", "dentist visit"],
    "diet": ["diet", "food", "eat", "drink", "sugar", "nutrition", "what to avoid"],
    "sensitive": ["sensitive", "sensitivity", "sharp pain", "sting", "tingle", "cold hurts", "hot hurts"],
}

GREETING_KEYWORDS = ["hello", "hi", "hey", "good morning", "good evening", "howdy", "greetings", "start"]


def find_response(user_message: str) -> str:
    msg = user_message.lower()

    # Greetings
    if any(kw in msg for kw in GREETING_KEYWORDS) and len(msg.split()) <= 5:
        return random.choice(GREETINGS)

    # Keyword matching
    for topic, keywords in KEYWORDS.items():
        if any(kw in msg for kw in keywords):
            responses = DENTAL_RESPONSES.get(topic, [])
            if responses:
                return random.choice(responses)

    return random.choice(FALLBACK_RESPONSES)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    user_message = messages[-1].get("content", "") if messages else ""

    # Simulate a brief thinking delay
    time.sleep(0.6)

    reply = find_response(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=5002)