import requests
import base64
import json
from urllib.parse import unquote, quote

SOURCE_URL = "https://raw.githubusercontent.com/0xRadikal/Free-v2ray-Configs/main/top100.txt"
OUTPUT_FILE = "sub.txt"

def modify_name(link: str) -> str:
    if "#" in link:
        base, name = link.split("#", 1)
        name = unquote(name)

        new_name = name.replace("@Raydikalx", "@Configvibes")
        
        return f"{base}#{quote(new_name)}"

    if link.startswith("vmess://"):
        try:
            encoded = link[8:]
            encoded += "=" * (-len(encoded) % 4)
            data = base64.b64decode(encoded).decode("utf-8")
            conf = json.loads(data)
            
            old_ps = conf.get("ps", "")
            conf["ps"] = old_ps.replace("@Raydikalx", "@Configvibes")
            
            new_encoded = base64.b64encode(
                json.dumps(conf, ensure_ascii=False).encode()
            ).decode().rstrip("=")
            return "vmess://" + new_encoded
        except Exception:
            return link

    return link

def main():
    print(f"در حال دریافت از: {SOURCE_URL}")
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.raise_for_status()
    content = resp.text

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    
    modified = []
    count = 0

    for line in lines:
        if line.startswith("#"):
            continue

        if any(line.startswith(p) for p in ("vless://", "vmess://", "trojan://", "hy2://", "hysteria2://", "ss://", "ssr://", "tuic://")):
            modified.append(modify_name(line))
            count += 1

    final_content = "\n".join(modified)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"تعداد کانفیگ تغییر یافته: {count}")
    print("فایل با موفقیت ساخته شد.")

if __name__ == "__main__":
    main()
