import requests
import base64
import re
import json
import socket

# Список источников
sources = [
    "https://raw.githubusercontent.com/w1770946466/Auto_Proxy/main/Long_term_subscription_num",
    "https://raw.githubusercontent.com/stayallive/v2ray-proxy-group/main/v2ray-proxy-group.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-checker-backend/main/checked/RU_Best/ru_white_all_part2.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/26.txt"
]

FLAGS = {'US': '🇺🇸', 'DE': '🇩🇪', 'RU': '🇷🇺', 'TR': '🇹🇷', 'NL': '🇳🇱', 'SG': '🇸🇬', 'FR': '🇫🇷', 'GB': '🇬🇧', 'HK': '🇭🇰', 'KZ': '🇰🇿'}

def is_alive(addr, port):
    try:
        with socket.create_connection((addr, int(port)), timeout=1.5):
            return True
    except:
        return False

def get_addr(cfg):
    try:
        if "vmess://" in cfg:
            data = json.loads(base64.b64decode(cfg[8:]).decode())
            return data.get('add'), data.get('port')
        match = re.search(r'@([^:]+):(\num+)', cfg)
        if match: return match.group(1), match.group(2)
    except: pass
    return None, None

def rename(cfg, i):
    country = "🌐"
    for code, flag in FLAGS.items():
        if code in cfg.upper(): country = flag; break
    
    if cfg.startswith("vmess://"):
        try:
            data = json.loads(base64.b64decode(cfg[8:]).decode())
            data['ps'] = f"{country} Freedom | #{i}"
            return "vmess://" + base64.b64encode(json.dumps(data).encode()).decode()
        except: return cfg
    
    parts = cfg.split('#')
    return f"{parts[0]}#{country} Freedom | #{i}"

def collect():
    raw_configs = []
    for url in sources:
        try:
            res = requests.get(url, timeout=10).text
            if "://" not in res: res = base64.b64decode(res).decode('utf-8', 'ignore')
            raw_configs.extend(re.findall(r'(vless|vmess|ss|trojan)://[^\s|]+', res))
        except: continue

    unique = list(dict.fromkeys(raw_configs))
    final = []
    count = 1
    for c in unique[:150]:
        addr, port = get_addr(c)
        if addr and is_alive(addr, port):
            final.append(rename(c, count))
            count += 1
        if count > 50: break

    with open("sub_auto.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final))

if __name__ == "__main__":
    collect()
