import requests
import base64
import re
import json
import socket
from urllib.parse import urlparse

# 1. Список источников
sources = [
    "https://raw.githubusercontent.com/w1770946466/Auto_Proxy/main/Long_term_subscription_num",
    "https://raw.githubusercontent.com/stayallive/v2ray-proxy-group/main/v2ray-proxy-group.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-checker-backend/main/checked/RU_Best/ru_white_all_part2.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/26.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-worker-sub/main/sub/shadowsocks",
    "https://raw.githubusercontent.com/vfarid/v2ray-worker-sub/main/sub/vless"
]

FLAGS = {
    'US': '🇺🇸', 'DE': '🇩🇪', 'RU': '🇷🇺', 'TR': '🇹🇷', 'NL': '🇳🇱', 'SG': '🇸🇬', 
    'FR': '🇫🇷', 'GB': '🇬🇧', 'JP': '🇯🇵', 'HK': '🇭🇰', 'FI': '🇫🇮', 'PL': '🇵🇱', 
    'KZ': '🇰🇿', 'UA': '🇺🇦', 'CA': '🇨🇦', 'KR': '🇰🇷', 'BR': '🇧🇷'
}

def check_port(address, port):
    """Проверяет, открыт ли порт у сервера"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((address, int(port)))
        s.close()
        return True
    except:
        return False

def get_ip_from_config(config):
    """Вытаскивает IP/Домен и Порт из конфига"""
    try:
        if config.startswith("vmess://"):
            v2_bin = base64.b64decode(config[8:]).decode('utf-8')
            v2_json = json.loads(v2_bin)
            return v2_json.get('add'), v2_json.get('port')
        
        # Для vless/trojan/ss
        parts = config.split('@')
        if len(parts) > 1:
            after_at = parts[1].split('?')[0].split('#')[0]
            addr_port = after_at.split(':')
            return addr_port[0], addr_port[1]
    except:
        return None, None

def rename_and_verify(config, index):
    addr, port = get_ip_from_config(config)
    if not addr or not port: return None
    
    # ПРОВЕРКА: Если порт закрыт — удаляем
    if not check_port(addr, port): return None

    # ОПРЕДЕЛЕНИЕ СТРАНЫ (по коду в конфиге)
    country_info = "🌐"
    for code, flag in FLAGS.items():
        if code in config.upper():
            country_info = flag
            break
            
    try:
        if config.startswith("vmess://"):
            v2_bin = base64.b64decode(config[8:]).decode('utf-8')
            v2_json = json.loads(v2_bin)
            v2_json['ps'] = f"{country_info} Freedom | #{index}"
            return "vmess://" + base64.b64encode(json.dumps(v2_json).encode()).decode()
        
        base = config.split('#')[0]
        return f"{base}#{country_info} Freedom | #{index}"
    except:
        return None

def collect():
    all_configs = []
    print("🚀 Начинаю глубокий поиск и проверку...")
    
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            content = res.text
            if "://" not in content:
                content = base64.b64decode(content).decode('utf-8', errors='ignore')
            
            found = re.findall(r'(vless|vmess|ss|trojan)://[^\s|]+', content)
            all_configs.extend(found)
        except: continue

    unique_configs = list(dict.fromkeys(all_configs))
    final_configs = []
    
    count = 1
    # Проверяем первые 300 найденных, чтобы оставить только лучшие
    for cfg in unique_configs[:300]:
        verified = rename_and_verify(cfg, count)
        if verified:
            final_configs.append(verified)
            count += 1
        if count > 100: break # Нам хватит 100 реально рабочих

    with open("sub_auto.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_configs))
    
    print(f"✅ Готово! Найдено и проверено: {len(final_configs)} рабочих серверов.")

if __name__ == "__main__":
    collect()
