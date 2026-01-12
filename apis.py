import requests

TIMEOUT = 40

def get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_india_number(n):
    return get(
        "https://subhxcosmo-osint-api.onrender.com/api",
        {"key": "VNIOX", "type": "mobile", "term": n}
    )

def api_vehicle_num(v):
    return get(
        "https://subhxcosmo-osint-api.onrender.com/api",
        {"key": "VNIOX", "type": "vehicle_num", "term": v}
    )

def api_vehicle_info(rc):
    return get("https://vnioxcyber.vercel.app/api/vehicle", {"rc": rc})

def api_id_family(fid):
    return get(
        "https://subhxcosmo-osint-api.onrender.com/api",
        {"key": "VNIOX", "type": "id_family", "term": fid}
    )

def api_pak_number(n):
    return get("https://paknum.amorinthz.workers.dev/", {"key": "AMORINTH", "number": n})

def api_ff(uid):
    return get("https://api-cr-ffinfo.kesug.com/ff.php", {"uid": uid})

def api_ifsc(code):
    return get("https://ab-ifscinfoapi.vercel.app/info", {"ifsc": code})

def api_calltrace(n):
    return get("https://ab-calltraceapi.vercel.app/info", {"number": n})

def api_fampay(fid):
    return get("https://fampay-2-number.vercel.app/get-number", {"id": fid})
