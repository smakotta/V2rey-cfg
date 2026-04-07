import requests
import base64
import re
import json

# 1. Список источников (ЗАПЯТЫЕ В КОНЦЕ СТРОК ОБЯЗАТЕЛЬНЫ)
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

# Словарь флагов
FLAGS = {
    'US': '🇺🇸', 'DE': '🇩🇪', 'RU': '🇷🇺', 'TR': '🇹🇷', 'NL': '🇳🇱', 
    'SG': '🇸🇬', 'FR': '🇫🇷', 'GB': '🇬🇧', 'JP': '🇯🇵', 'HK': '🇭🇰',
    'FI': '🇫🇮', 'PL': '🇵🇱', 'KZ': '🇰🇿', 'UA': '🇺🇦', 'CA': '🇨🇦'
}

def get_country_and_flag(config):
    config_upper = config.upper()
    for code, flag in FLAGS.items():
        if code in config_upper:
            return f"{flag} {code}"
    return "🌐 UNK"

def rename_config(config, index):
    try:
        # VMess обрабатывается отдельно, так как это Base64 JSON
        if config.startswith("vmess://"):
            try:
                v2_bin = base64.b64decode(config[8:]).decode('utf-8')
                v2_json = json.loads(v2_bin)
                country_info = get_country_and_flag(v2_json.get('ps', ''))
                v2_json['ps'] = f"{country_info} | Freedom-{index}"
                new_v2 = base64.b64encode(json.dumps(v2_json).encode('utf-8')).decode('utf-8')
                return f"vmess://{new_v2}"
            except:
                return config

        # Остальные (VLESS, SS, Trojan) переименовываются через #
        base_part = config.split('#')[0]
        country_info = get_country_and_flag(config)
        return f"{base_part}#{country_info} | Freedom-{index}"
    except:
        return config

def collect():
    all_configs = []
    print("Начинаю сбор...")
    
    for url in sources:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                content = res.text
                # Если это зашифрованная подписка (Base64)
                if not any(proto in content for proto in ['vless://', 'vmess://', 'ss://']):
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        pass
                
                found = re.findall(r'(vless|vmess|ss|trojan)://[^\s|]+', content)
                all_configs.extend(found)
                print(f"Из {url} получено {len(found)} шт.")
        except Exception as e:
            print(f"Ошибка при чтении {url}: {e}")
            continue

    # Чистка дубликатов
    unique_configs = list(dict.fromkeys(all_configs))
    
    final_configs = []
    # Берем первые 200 конфигов для стабильности
    for i, cfg in enumerate(unique_configs[:200]):
        final_configs.append(rename_config(cfg, i+1))

    with open("sub_auto.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_configs))
    
    print(f"Успех! Сохранено {len(final_configs)} конфигов.")

if __name__ == "__main__":
    collect()
