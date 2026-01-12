def header(title):
    return f"══════════════  {title}  ══════════════\n\n"

def footer():
    return (
        "\n══════════════════════════════════\n"
        "          BUY API - @SUBHXCOSMO\n"
        "══════════════════════════════════\n"
        "══════════════════════════════════\n"
        "          MADE BY - @LingTech_Dev\n"
        "══════════════════════════════════"
    )

def fmt_raw(title, data):
    def walk(d, pad=""):
        out = ""
        if isinstance(d, dict):
            for k, v in d.items():
                out += f"{pad}{k}:\n"
                out += walk(v, pad + "  ")
        elif isinstance(d, list):
            for i, x in enumerate(d, 1):
                out += f"{pad}[{i}]\n"
                out += walk(x, pad + "  ")
        else:
            out += f"{pad}{d}\n"
        return out

    return header(title) + walk(data) + footer()

def fmt_india_number(d):
    res = d.get("result", {}).get("result", [])
    out = header("I N D I A N   N U M B E R   I N F O R M A T I O N")
    for i, r in enumerate(res, 1):
        out += (
            f"┃ 🔹 RESULT {i}\n"
            f"┃ 👤 Name        : {r.get('name','Not Available')}\n"
            f"┃ 📞 Mobile      : {r.get('mobile','Not Available')}\n"
            f"┃ 👨‍👦 Father     : {r.get('father_name','Not Available')}\n"
            f"┃ 📍 Address     : {r.get('address','Not Available')}\n"
            f"┃ 📱 Alt Mobile  : {r.get('alt_mobile','Not Available')}\n"
            f"┃ 📡 Circle      : {r.get('circle','Not Available')}\n"
            f"┃ 🆔 ID Number   : {r.get('id_number','Not Available')}\n"
            f"┃ 📧 Email       : {r.get('email','Not Available')}\n"
            f"┃ 🆔 Record ID   : {r.get('id','Not Available')}\n"
        )
        if i != len(res):
            out += "┃\n┃────────────────────────────────\n"
    return out + footer()
