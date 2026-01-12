import uuid

def save_txt(text, name="result"):
    path = f"/tmp/{name}_{uuid.uuid4().hex[:6]}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
