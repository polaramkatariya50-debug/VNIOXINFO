import requests

def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=25)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_num(n):
    return safe_get(
        "https://subhxcosmo-osint-api.onrender.com/api",
        {"key": "VNIOX", "type": "mobile", "term": n}
    )

def api_vehicle_num(v):
    return safe_get(
        "https://subhxcosmo-osint-api.onrender.com/api",
        {"key": "VNIOX", "type": "vehicle_num", "term": v}
    )

def api_vehicle_info(rc):
    return safe_get(
        "https://vnioxcyber.vercel.app/api/vehicle",
        {"rc": rc}
    )

def api_id_family(i):
    return safe_get(
        "https://subhxcosmo-osint-api.onrender.com/api",
        {"key": "VNIOX", "type": "id_family", "term": i}
    )

def api_pk(n):
    return safe_get(
        "https://paknum.amorinthz.workers.dev/",
        {"key": "AMORINTH", "number": n}
    )

def api_rc(rc):
    return safe_get(
        "https://vnioxcyber.vercel.app/api/vehicle",
        {"rc": rc}
    )

def api_ff(uid):
    return safe_get(
        "https://api-cr-ffinfo.kesug.com/ff.php",
        {"uid": uid}
    )

def api_ifsc(code):
    return safe_get(
        "https://ab-ifscinfoapi.vercel.app/info",
        {"ifsc": code}
    )

def api_calltrace(n):
    return safe_get(
        "https://ab-calltraceapi.vercel.app/info",
        {"number": n}
    )

def api_fampay(fid):
    return safe_get(
        "https://fampay-2-number.vercel.app/get-number",
        {"id": fid}
    )
