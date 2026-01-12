import uuid
import json

def save_txt(data):
    path = f"/tmp/result_{uuid.uuid4().hex[:8]}.txt"

    with open(path, "w", encoding="utf-8") as f:
        if isinstance(data, (dict, list)):
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            f.write(str(data))

    return path
