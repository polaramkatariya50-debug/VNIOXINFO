def auto_format(data, indent=0):
    sp = " " * indent
    out = ""
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                out += f"{sp}{k}:\n{auto_format(v, indent+4)}"
            else:
                out += f"{sp}{k}: {v}\n"
    elif isinstance(data, list):
        for i, x in enumerate(data, 1):
            out += f"{sp}[{i}]\n{auto_format(x, indent+4)}"
    else:
        out += f"{sp}{data}\n"
    return out

def fmt_all(title, data):
    body = auto_format(data)
    return (
        f"{title}\n\n"
        f"{body}\n\n"
        "BUY API - @SUBHXCOSMO\n"
        "MADE BY - @LingTech_Dev"
    )
