import requests
import base64
import re
import json

# 1. Огромный список источников (ты можешь добавлять свои ссылки сюда)
sources = [
    "https://raw.githubusercontent.com/w1770946466/Auto_Proxy/main/Long_term_subscription_num",
    "https://raw.githubusercontent.com/stayallive/v2ray-proxy-group/main/v2ray-proxy-group.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.txt"
    "https://raw.githubusercontent.com/kort0881/vpn-checker-backend/main/checked/RU_Best/ru_white_all_part2.txt"
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt"
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/26.txt"
]

# Словарь флагов для красоты
FLAGS = {
    'US': '🇺🇸', 'DE': '🇩🇪', 'RU': '🇷🇺', 'TR': '🇹🇷', 'NL': '🇳🇱', 
    'SG': '🇸🇬', 'FR': '🇫🇷', 'GB': '🇬🇧', 'JP': '🇯🇵', 'HK': '🇭🇰'
}

def get_country_and_flag(config):
    # Упрощенная логика: ищем упоминание страны в самом конфиге (обычно они там есть)
    for code, flag in FLAGS.items():
        if code in config.upper():
            return f"{flag} {code}"
    return "🌐 UNK"

def rename_config(config, index):
    try:
        # Ищем часть после символа # (это название в V2Ray/VLESS)
        if "#" in config:
            base_url = config.split("#")[0]
            country_info = get_country_and_flag(config)
            # Формируем новое название: Флаг + Страна + Freedom + Номер
            new_name = f"{country_info} | Freedom-{index}"
            return f"{base_url}#{new_name}"
        return config
    except:
        return config

def collect():
    all_configs = []
    print("Начинаю сбор...")
    
    for url in sources:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                # Если данные в Base64 (часто бывает в подписках), декодируем
                content = res.text
                if not content.startswith(('vless', 'vmess', 'ss')):
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        pass
                
                # Ищем все протоколы через регулярные выражения
                found = re.findall(r'(vless|vmess|ss|trojan)://[^\s|]+', content)
                all_configs.extend(found)
        except:
            continue

    # Убираем дубликаты
    unique_configs = list(set(all_configs))
    
    # Переименовываем и оставляем только рабочие на вид (длинные строки)
    final_configs = []
    for i, cfg in enumerate(unique_configs[:100]): # Ограничим до 100 лучших
        new_cfg = rename_config(cfg, i+1)
        final_configs.append(new_cfg)

    with open("sub_auto.txt", "w") as f:
        f.write("\n".join(final_configs))
    
    print(f"Готово! Сохранено {len(final_configs)} конфигов с новыми именами.")

if __name__ == "__main__":
    collect()
