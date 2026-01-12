# =========================================================
# COMMON FOOTER (USED IN ALL API RESPONSES)
# =========================================================

def footer():
    return (
        "\n══════════════════════════════════\n"
        "          BUY API - @SUBHXCOSMO\n"
        "══════════════════════════════════\n"
        "══════════════════════════════════\n"
        "          MADE BY - @LingTech_Dev\n"
        "══════════════════════════════════"
    )


def wrap_addr(prefix, text):
    if not text:
        return f"{prefix} Not Available\n"
    parts = [p.strip() for p in str(text).split(",")]
    out = f"{prefix} {parts[0]}\n"
    for p in parts[1:]:
        out += f"┃                 {p}\n"
    return out


# =========================================================
# 1️⃣ INDIAN NUMBER INFORMATION
# =========================================================

def fmt_india_number(d):
    res = d.get("result", {}).get("result", [])

    out = (
        "══════════════  I N D I A N   N U M B E R   I N F O R M A T I O N  ══════════════\n\n"
    )

    if not res:
        return out + "┃ ❌ No records found\n" + footer()

    for i, r in enumerate(res, 1):
        out += (
            f"┃ 🔹 RESULT {i}\n"
            f"┃ 👤 Name        : {r.get('name','Not Available')}\n"
            f"┃ 📞 Mobile      : {r.get('mobile','Not Available')}\n"
            f"┃ 👨‍👦 Father     : {r.get('father_name','Not Available')}\n"
        )
        out += wrap_addr("┃ 📍 Address     :", r.get("address"))
        out += (
            f"┃ 📱 Alt Mobile  : {r.get('alt_mobile','Not Available')}\n"
            f"┃ 📡 Circle      : {r.get('circle','Not Available')}\n"
            f"┃ 🆔 ID Number   : {r.get('id_number','Not Available')}\n"
            f"┃ 📧 Email       : {r.get('email','Not Available')}\n"
            f"┃ 🆔 Record ID   : {r.get('id','Not Available')}\n"
        )
        if i != len(res):
            out += "┃\n┃────────────────────────────────\n"

    return out + footer()


# =========================================================
# 2️⃣ PAKISTAN NUMBER INFORMATION
# =========================================================

def fmt_pakistan_number(d):
    records = d.get("data", [])

    out = (
        "══════════════ 🇵🇰  P A K I S T A N  🇵🇰 ══════════════\n\n"
        "┃ 🔹 PHONE LOOKUP\n"
        f"┃ 📞 Searched Phone : {d.get('number','N/A')}\n"
        "┃\n"
    )

    for i, r in enumerate(records, 1):
        out += (
            "┃────────────────────────────────\n"
            f"┃ 🔹 RECORD {i}\n"
            f"┃ 👤 Name        : {r.get('name','N/A')}\n"
            f"┃ 📞 Mobile      : {r.get('mobile','N/A')}\n"
            f"┃ 🆔 CNIC        : {r.get('cnic','N/A')}\n"
        )
        out += wrap_addr("┃ 📍 Address     :", r.get("address"))
        out += "┃ 🌍 Country     : Pakistan\n┃\n"

    return out + footer()


# =========================================================
# 3️⃣ VEHICLE INFORMATION (FULL)
# =========================================================

def fmt_vehicle_info(d):
    data = d.get("data", {})

    out = (
        "╔══════════════════════════════════╗\n"
        f"║     🚗 VEHICLE DETAILS: {data.get('registration_no','N/A')}     ║\n"
        "╚══════════════════════════════════╝\n\n"
    )

    owner = data.get("owner", {})
    out += (
        "┌─ 👤 OWNER INFORMATION ─┐\n"
        f" Owner Name     : {owner.get('name','N/A')}\n"
        f" Also Known As  : {owner.get('alias','N/A')}\n"
        f" Father’s Name  : {owner.get('father','N/A')}\n"
        "└───────────────────────┘\n\n"
    )

    addr = data.get("address", {})
    out += (
        "┌─ 🏠 ADDRESS DETAILS ─┐\n"
        f" Address : {addr.get('address','N/A')}\n"
        f" City    : {addr.get('city','N/A')}\n"
        f" State   : {addr.get('state','N/A')}\n"
        f" Pincode : {addr.get('pincode','N/A')}\n"
        "└───────────────────────┘\n\n"
    )

    out += (
        "┌─ 🔧 VEHICLE SPECIFICATIONS ─┐\n"
        f" Manufacturer  : {data.get('manufacturer','N/A')}\n"
        f" Model         : {data.get('model','N/A')}\n"
        f" Vehicle Class : {data.get('vehicle_class','N/A')}\n"
        f" Fuel Type     : {data.get('fuel_type','N/A')}\n"
        "└───────────────────────┘\n\n"
    )

    reg = data.get("registration", {})
    out += (
        "┌─ 📋 REGISTRATION DETAILS ─┐\n"
        f" Registration No. : {reg.get('number','N/A')}\n"
        f" Registration Dt.: {reg.get('date','N/A')}\n"
        f" Registered RTO  : {reg.get('rto','N/A')}\n"
        "└───────────────────────┘\n\n"
    )

    ins = data.get("insurance", {})
    out += (
        "┌─ 🛡 INSURANCE STATUS ─┐\n"
        f" Insurance Valid Till : {ins.get('valid_till','N/A')}\n"
        f" Status               : {ins.get('status','N/A')}\n"
        "└───────────────────────┘\n\n"
    )

    return out + footer()


# =========================================================
# 4️⃣ VEHICLE → OWNER NUMBER
# =========================================================

def fmt_vehicle_owner_number(d):
    data = d.get("data", d)

    out = (
        "╔══════════════════════════════════╗\n"
        "║   🚗 VEHICLE NUM TO OWNER NUM   ║\n"
        "╚══════════════════════════════════╝\n\n"
        "┌─ 🔍 MAPPING DETAILS ─┐\n"
        f" Vehicle Number : {data.get('vehicle_number','N/A')}\n"
        f" Mobile Number  : {data.get('mobile_number','N/A')}\n"
        "└───────────────────────┘\n\n"
        "┌─ ℹ️ STATUS INFO ─┐\n"
        " Mapping Type : Vehicle → Owner Mobile\n"
        f" Record Status: {data.get('status','SUCCESS')}\n"
        "└───────────────────────┘\n\n"
    )

    return out + footer()


# =========================================================
# 5️⃣ AADHAAR → FAMILY INFORMATION
# =========================================================

def fmt_aadhaar_family_info(d):
    data = d.get("data", {})
    ration = data.get("ration_card", {})
    members = data.get("family_members", [])

    out = (
        "══════════════  A A D H A A R   T O   F A M I L Y   I N F O R M A T I O N  ══════════════\n\n"
        "┃ 🔹 SEARCH DETAILS\n"
        "┃ 🔍 Search Type       : AADHAAR\n"
        f"┃ ✅ Success           : {data.get('success','True')}\n"
        "┃\n"
        "┃ 🔹 RATION CARD DETAILS\n"
        f"┃ 🆔 Ration Card No.   : {ration.get('ration_card_no','N/A')}\n"
        f"┃ 🪪 Card Type         : {ration.get('card_type','N/A')}\n"
        f"┃ 📜 Scheme            : {ration.get('scheme','N/A')}\n"
        f"┃ 📅 Issue Date        : {ration.get('issue_date','N/A')}\n"
        f"┃ 🏛 State             : {ration.get('state','N/A')}\n"
        f"┃ 🗺 District          : {ration.get('district','N/A')}\n"
        f"┃ 🏠 Address           : {ration.get('address','N/A')}\n"
        "┃\n"
        "┃────────────────────────────────\n"
        "┃ 🔹 FAMILY MEMBERS\n\n"
    )

    for i, m in enumerate(members, 1):
        out += (
            f"┃ 👤 Member {i}\n"
            f"┃ 🆔 Member ID         : {m.get('member_id','N/A')}\n"
            f"┃ 👤 Name              : {m.get('name','N/A')}\n"
            f"┃ ⚧️ Gender            : {m.get('gender','N/A')}\n"
            f"┃ 🔐 Aadhaar (Masked)  : {m.get('aadhaar_masked','N/A')}\n"
            f"┃ 🔗 Relationship      : {m.get('relationship','N/A')}\n"
            f"┃ ✅ eKYC Status       : {m.get('ekyc_status','N/A')}\n"
            "┃\n"
        )

    return out + footer()


# =========================================================
# 6️⃣ FREE FIRE UID INFORMATION
# =========================================================

def fmt_free_fire_info(d):
    data = d.get("data", d)
    prof = data.get("profile", {})
    stats = data.get("stats", {})

    out = (
        "╔══════════════════════════════════╗\n"
        "║     🎮 FREE FIRE ID INFORMATION     ║\n"
        "╚══════════════════════════════════╝\n\n"
        f"📌 Data fetched for UID : {data.get('uid','N/A')}\n\n"
        "┌─ 👤 PROFILE DETAILS ─┐\n"
        f" Nickname : {prof.get('nickname','N/A')}\n"
        f" User ID  : {data.get('uid','N/A')}\n"
        f" Region   : {prof.get('region','N/A')}\n"
        f" Influencer : {prof.get('influencer','No')}\n"
        "└───────────────────────┘\n\n"
        "┌─ 🎖️ ACCOUNT STATS ─┐\n"
        f" Level          : {stats.get('level','N/A')}\n"
        f" Experience XP  : {stats.get('exp','N/A')}\n"
        f" Ranked Points  : {stats.get('ranked_points','N/A')}\n"
        f" Likes          : {stats.get('likes','N/A')}\n"
        "└───────────────────────┘\n\n"
    )

    return out + footer()


# =========================================================
# 7️⃣ IFSC INFORMATION
# =========================================================

def fmt_ifsc_info(d):
    data = d.get("data", d)

    out = (
        "══════════════  B A N K   I F S C   C O D E   I N F O R M A T I O N  ══════════════\n\n"
        "┃ 🔹 BANK DETAILS\n"
        f"┃ 🏦 Bank Name   : {data.get('BANK','N/A')}\n"
        f"┃ 🆔 Bank Code   : {data.get('BANKCODE','N/A')}\n"
        f"┃ 🌿 Branch      : {data.get('BRANCH','N/A')}\n"
    )
    out += wrap_addr("┃ 🏢 Address     :", data.get("ADDRESS"))
    out += (
        f"┃ 🌆 City        : {data.get('CITY','N/A')}\n"
        f"┃ 🏛 State       : {data.get('STATE','N/A')}\n"
        "┃\n"
        f"┃ 🔐 IFSC Code   : {data.get('IFSC','N/A')}\n"
        f"┃ 🧾 MICR Code   : {data.get('MICR','N/A')}\n"
    )

    return out + footer()


# =========================================================
# 8️⃣ INDIAN CALL TRACE INFORMATION
# =========================================================

def fmt_call_trace_info(d):
    data = d.get("data", d)
    loc = data.get("location", {})

    out = (
        "╔══════════════════════════════════╗\n"
        "║   📞 INDIAN CALL TRACE INFORMATION   ║\n"
        "╚══════════════════════════════════╝\n\n"
        "┌─ 📱 BASIC DETAILS ─┐\n"
        f" Mobile Number : {data.get('number','N/A')}\n"
        f" Connection    : {data.get('connection','N/A')}\n"
        f" SIM Operator  : {data.get('operator','N/A')}\n"
        f" Country       : India\n"
        "└───────────────────────┘\n\n"
        "┌─ 📍 LOCATION DETAILS ─┐\n"
        f" Mobile State   : {loc.get('state','N/A')}\n"
        f" Reference City : {loc.get('city','N/A')}\n"
        "└───────────────────────┘\n\n"
    )

    return out + footer()


# =========================================================
# 9️⃣ FAMPAY INFORMATION
# =========================================================

def fmt_fampay_info(d):
    data = d.get("data", d)

    out = (
        "══════════════  F A M P A Y   I N F O R M A T I O N  ══════════════\n\n"
        "┃ 🔹 CONTACT DETAILS\n"
        f"┃ 🆔 Fam ID      : {data.get('id','N/A')}\n"
        f"┃ 👤 Name        : {data.get('name','N/A')}\n"
        f"┃ 📞 Phone       : {data.get('phone','N/A')}\n"
        f"┃ 📡 Source      : {data.get('source','N/A')}\n"
        f"┃ ✅ Status      : {data.get('status','N/A')}\n"
        f"┃ 🗂 Type        : {data.get('type','N/A')}\n\n"
    )

    return out + footer()
