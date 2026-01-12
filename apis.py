import requests

def fetch(url, params):
    try:
        r = requests.get(url, params=params, timeout=40)
        return r.json()
    except:
        return {}

def api_india_number(n):
    return fetch("https://subhxcosmo-osint-api.onrender.com/api",
                 {"key":"VNIOX","type":"mobile","term":n})

def api_vehicle_info(v):
    return fetch("https://vnioxcyber.vercel.app/api/vehicle", {"rc":v})

def api_vehicle_num(v):
    return fetch("https://subhxcosmo-osint-api.onrender.com/api",
                 {"key":"VNIOX","type":"vehicle_num","term":v})

def api_pak_number(n):
    return fetch("https://paknum.amorinthz.workers.dev/",
                 {"key":"AMORINTH","number":n})

def api_ff(uid):
    return fetch("https://api-cr-ffinfo.kesug.com/ff.php", {"uid":uid})

def api_ifsc(code):
    return fetch("https://ab-ifscinfoapi.vercel.app/info", {"ifsc":code})

def api_calltrace(n):
    return fetch("https://ab-calltraceapi.vercel.app/info", {"number":n})

def api_fampay(fid):
    return fetch("https://fampay-2-number.vercel.app/get-number", {"id":fid})

def api_id_family(a):
    return fetch("https://subhxcosmo-osint-api.onrender.com/api",
                 {"key":"VNIOX","type":"id_family","term":a})
