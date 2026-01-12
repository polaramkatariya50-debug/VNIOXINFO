# ======================================================
# SMART VALUE PICKER (N/A ISSUE FIX – CORE)
# ======================================================

def pick(src, *keys, default="N/A"):
    if not isinstance(src, dict):
        return default
    for k in keys:
        val = src.get(k)
        if val not in (None, "", [], {}):
            return val
    return default


def footer():
    return (
        "\n══════════════════════════════════\n"
        "          BUY API - @SUBHXCOSMO\n"
        "══════════════════════════════════\n"
        "══════════════════════════════════\n"
        "          MADE BY - @LingTech_Dev\n"
        "══════════════════════════════════"
    )


def wrap(prefix, text):
    if not text or text == "N/A":
        return f"{prefix} N/A\n"
    parts = [p.strip() for p in str(text).split(",")]
    out = f"{prefix} {parts[0]}\n"
    for p in parts[1:]:
        out += f"┃                 {p}\n"
    return out


# ======================================================
# 1️⃣ INDIAN NUMBER INFO
# ======================================================

def fmt_india_number(d):
    res = pick(d, "result", default={}).get("result", [])

    out = (
        "══════════════  I N D I A N   N U M B E R   I N F O R M A T I O N  ══════════════\n\n"
    )

    if not res:
        return out + "┃ ❌ No records found\n" + footer()

    for i, r in enumerate(res, 1):
        out += (
            f"┃ 🔹 RESULT {i}\n"
            f"┃ 👤 Name        : {pick(r,'name')}\n"
            f"┃ 📞 Mobile      : {pick(r,'mobile')}\n"
            f"┃ 👨‍👦 Father     : {pick(r,'father_name')}\n"
        )
        out += wrap("┃ 📍 Address     :", pick(r, "address"))
        out += (
            f"┃ 📱 Alt Mobile  : {pick(r,'alt_mobile')}\n"
            f"┃ 📡 Circle      : {pick(r,'circle')}\n"
            f"┃ 🆔 ID Number   : {pick(r,'id_number')}\n"
            f"┃ 📧 Email       : {pick(r,'email')}\n"
            f"┃ 🆔 Record ID   : {pick(r,'id')}\n"
        )
        if i != len(res):
            out += "┃\n┃────────────────────────────────\n"

    return out + footer()


# ======================================================
# 2️⃣ PAKISTAN NUMBER INFO
# ======================================================

def fmt_pakistan_number(d):
    records = pick(d, "data", default=[])

    out = (
        "══════════════ 🇵🇰  P A K I S T A N  🇵🇰 ══════════════\n\n"
        "┃ 🔹 PHONE LOOKUP\n"
        f"┃ 📞 Searched Phone : {pick(d,'number')}\n"
        "┃\n"
    )

    if not records:
        return out + "┃ ❌ No records found\n" + footer()

    for i, r in enumerate(records, 1):
        out += (
            "┃────────────────────────────────\n"
            f"┃ 🔹 RECORD {i}\n"
            f"┃ 👤 Name        : {pick(r,'name')}\n"
            f"┃ 📞 Mobile      : {pick(r,'mobile')}\n"
            f"┃ 🆔 CNIC        : {pick(r,'cnic')}\n"
        )
        out += wrap("┃ 📍 Address     :", pick(r, "address"))
        out += "┃ 🌍 Country     : Pakistan\n┃\n"

    return out + footer()


# ======================================================
# 3️⃣ VEHICLE FULL INFORMATION
# ======================================================

def fmt_vehicle_info(d):
    src = d.get("data") or d.get("result") or d

    out = (
        "╔══════════════════════════════════╗\n"
        f"║     🚗 VEHICLE DETAILS: {pick(src,'registration_no','rc_number')}     ║\n"
        "╚══════════════════════════════════╝\n\n"
    )

    out += (
        "┌─ 👤 OWNER INFORMATION ─┐\n"
        f" Owner Name     : {pick(src,'owner_name','name')}\n"
        f" Father’s Name  : {pick(src,'father_name')}\n"
        "└───────────────────────┘\n\n"
    )

    out += (
        "┌─ 🏠 ADDRESS DETAILS ─┐\n"
        f" Address : {pick(src,'address')}\n"
        f" City    : {pick(src,'city')}\n"
        f" State   : {pick(src,'state')}\n"
        f" Pincode : {pick(src,'pincode')}\n"
        "└───────────────────────┘\n\n"
    )

    out += (
        "┌─ 🔧 VEHICLE SPECIFICATIONS ─┐\n"
        f" Manufacturer  : {pick(src,'manufacturer','maker')}\n"
        f" Model         : {pick(src,'model')}\n"
        f" Vehicle Class : {pick(src,'vehicle_class')}\n"
        f" Fuel Type     : {pick(src,'fuel_type')}\n"
        "└───────────────────────┘\n\n"
    )

    out += (
        "┌─ 📋 REGISTRATION DETAILS ─┐\n"
        f" Registration No. : {pick(src,'registration_no')}\n"
        f" Registration Dt.: {pick(src,'registration_date')}\n"
        f" Registered RTO  : {pick(src,'rto')}\n"
        "└───────────────────────┘\n\n"
    )

    out += (
        "┌─ 🛡 INSURANCE STATUS ─┐\n"
        f" Insurance Valid Till : {pick(src,'insurance_valid_till')}\n"
        f" Status               : {pick(src,'insurance_status')}\n"
        "└───────────────────────┘\n\n"
    )

    return out + footer()


# ======================================================
# 4️⃣ VEHICLE → OWNER MOBILE
# ======================================================

def fmt_vehicle_owner_number(d):
    src = d.get("data") or d.get("result") or d

    out = (
        "╔══════════════════════════════════╗\n"
        "║   🚗 VEHICLE NUM TO OWNER NUM   ║\n"
        "╚══════════════════════════════════╝\n\n"
        "┌─ 🔍 MAPPING DETAILS ─┐\n"
        f" Vehicle Number : {pick(src,'vehicle_number')}\n"
        f" Mobile Number  : {pick(src,'mobile_number')}\n"
        "└───────────────────────┘\n\n"
        "┌─ ℹ️ STATUS INFO ─┐\n"
        " Mapping Type : Vehicle → Owner Mobile\n"
        f" Record Status: {pick(src,'status','SUCCESS')}\n"
        "└───────────────────────┘\n\n"
    )

    return out + footer()


# ======================================================
# 5️⃣ AADHAAR → FAMILY INFO
# ======================================================

def fmt_aadhaar_family_info(d):
    src = d.get("data") or d.get("result") or d
    members = pick(src, "family_members", default=[])

    out = (
        "══════════════  A A D H A A R   T O   F A M I L Y   I N F O R M A T I O N  ══════════════\n\n"
        f"┃ 🆔 Ration Card No. : {pick(src,'ration_card_no')}\n"
        f"┃ 🏛 State           : {pick(src,'state')}\n"
        f"┃ 🗺 District        : {pick(src,'district')}\n"
        "┃\n"
        "┃ 🔹 FAMILY MEMBERS\n\n"
    )

    for i, m in enumerate(members, 1):
        out += (
            f"┃ 👤 Member {i}\n"
            f"┃ 👤 Name        : {pick(m,'name')}\n"
            f"┃ ⚧ Gender       : {pick(m,'gender')}\n"
            f"┃ 🔗 Relation     : {pick(m,'relationship')}\n"
            "┃\n"
        )

    return out + footer()


# ======================================================
# 6️⃣ FREE FIRE UID INFO
# ======================================================

def fmt_free_fire_info(d):
    src = d.get("data") or d

    out = (
        "╔══════════════════════════════════╗\n"
        "║     🎮 FREE FIRE ID INFORMATION     ║\n"
        "╚══════════════════════════════════╝\n\n"
        f" UID       : {pick(src,'uid')}\n"
        f" Nickname  : {pick(src,'nickname','name')}\n"
        f" Level     : {pick(src,'level')}\n"
        f" Likes     : {pick(src,'likes')}\n\n"
    )

    return out + footer()


# ======================================================
# 7️⃣ IFSC INFO
# ======================================================

def fmt_ifsc_info(d):
    src = d.get("data") or d

    out = (
        "══════════════  B A N K   I F S C   C O D E   I N F O R M A T I O N  ══════════════\n\n"
        f"┃ 🏦 Bank Name : {pick(src,'BANK')}\n"
        f"┃ 🌿 Branch    : {pick(src,'BRANCH')}\n"
        f"┃ 🔐 IFSC      : {pick(src,'IFSC')}\n"
        f"┃ 🧾 MICR      : {pick(src,'MICR')}\n"
    )

    return out + footer()


# ======================================================
# 8️⃣ CALL TRACE INFO
# ======================================================

def fmt_call_trace_info(d):
    src = d.get("data") or d

    out = (
        "╔══════════════════════════════════╗\n"
        "║   📞 INDIAN CALL TRACE INFORMATION   ║\n"
        "╚══════════════════════════════════╝\n\n"
        f" Mobile Number : {pick(src,'number')}\n"
        f" Operator      : {pick(src,'operator')}\n"
        f" State         : {pick(src,'state')}\n\n"
    )

    return out + footer()


# ======================================================
# 9️⃣ FAMPAY INFO
# ======================================================

def fmt_fampay_info(d):
    src = d.get("data") or d

    out = (
        "══════════════  F A M P A Y   I N F O R M A T I O N  ══════════════\n\n"
        f"┃ 🆔 Fam ID  : {pick(src,'id')}\n"
        f"┃ 👤 Name    : {pick(src,'name')}\n"
        f"┃ 📞 Phone   : {pick(src,'phone')}\n"
        f"┃ 📡 Source  : {pick(src,'source')}\n"
        f"┃ ✅ Status  : {pick(src,'status')}\n"
    )

    return out + footer()
