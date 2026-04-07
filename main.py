import requests
import base64
import re

# Список источников (ссылки на другие подписки)
sources = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/splited/all.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt"
]

def collect():
    all_configs = []
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Разбиваем текст на строки и ищем конфиги
                configs = response.text.splitlines()
                for cfg in configs:
                    if cfg.startswith(('vless://', 'vmess://', 'ss://', 'trojan://')):
                        all_configs.append(cfg)
        except:
            continue
    
    # Убираем дубликаты и берем первые 50 для теста
    unique_configs = list(set(all_configs))[:50]
    
    # Сохраняем в файл
    with open("sub_auto.txt", "w") as f:
        f.write("\n".join(unique_configs))
    print(f"Собрано {len(unique_configs)} конфигов.")

if __name__ == "__main__":
    collect()
