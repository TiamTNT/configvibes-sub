import os
import requests
import base64
import re
from urllib.parse import unquote, quote

SOURCE_URL = os.environ.get("SOURCE_URL")
OUTPUT_FILE = "sub.txt"

NAME_PREFIX = "🇮🇷 MySub | "

def is_base64(s: str) -> bool:
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s.strip()
    except Exception:
        return False

def modify_name(link: str) -> str:
    """اسم (remark) لینک‌های vless/vmess/trojan رو تغییر می‌ده"""
    if link.startswith(("vless://", "trojan://")):
        if "#" in link:
            base, name = link.split("#", 1)
            new_name = NAME_PREFIX + unquote(name)
            return f"{base}#{quote(new_name)}"
        else:
            return f"{link}#{quote(NAME_PREFIX + 'Config')}"

    if link.startswith("vmess://"):
        try:
            encoded = link[8:]
            encoded += "=" * (-len(encoded) % 4)
            data = base64.b64decode(encoded).decode("utf-8")
            import json
            conf = json.loads(data)
            old_name = conf.get("ps", "Config")
            conf["ps"] = NAME_PREFIX + old_name
            new_encoded = base64.b64encode(json.dumps(conf, ensure_ascii=False).encode()).decode().rstrip("=")
            return "vmess://" + new_encoded
        except Exception:
            return link

    return link

def main():
    if not SOURCE_URL:
        print("SOURCE_URL تنظیم نشده!")
        return

    print(f"در حال دریافت از: {SOURCE_URL}")
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.raise_for_status()
    content = resp.text.strip()

    if is_base64(content):
        try:
            content = base64.b64decode(content).decode("utf-8")
        except Exception:
            pass

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    
    modified = []
    for line in lines:
        if line.startswith(("vless://", "vmess://", "trojan://", "ss://")):
            modified.append(modify_name(line))
        else:
            modified.append(line)

    final_content = "\n".join(modified)


    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"تعداد کانفیگ: {len(modified)}")
    print("فایل با موفقیت آپدیت شد.")

if __name__ == "__main__":
    main()
