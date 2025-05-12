import requests
import random
import time
import socket
from datetime import datetime

# Telegram konfigurasiýasy
BOT_TOKEN = "7853273196:AAGdXBhl2x4FS3QQOKU5cabM13L1q_VAoM0"
CHAT_ID = "1753028724"

# CF IP Rangelar (IPv4)
CF_IP_RANGES = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
]

# Öňden ulanylan IP sanawy
USED_IP_FILE = "/mnt/data/used_ips.txt"

# Ulanylan IP-leri oka
def load_used_ips():
    try:
        with open(USED_IP_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

# Täze IP-ni loga ýaz
def save_used_ip(ip):
    with open(USED_IP_FILE, "a") as f:
        f.write(ip + "\n")

# IP adresleri döret (CIDR-den)
def cidr_to_ips(cidr):
    ip, cidr = cidr.split("/")
    host_bits = 32 - int(cidr)
    ip_num = sum(int(x) << (8 * (3 - i)) for i, x in enumerate(ip.split(".")))
    return [(ip_num + i) for i in range(2**host_bits)]

# IP-ni okalýan formata getir
def ip_num_to_str(ip_num):
    return ".".join(str((ip_num >> (8 * i)) & 0xFF) for i in reversed(range(4)))

# Port açykmy?
def is_port_open(ip, port, timeout=1.5):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

# Telegram habary ugrat
def send_telegram_message(ip, port):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"""
🟢 Täze Cloudflare IP tapyldy!

📡 IP: {ip}
🌐 Port: {port} açyk
🕓 Wagt: {timestamp}
📊 Status: Işleýär (%75 mümkinçilik)

#CF #Proxy #Türkmenistan
"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

# Esasy skript
def main():
    used_ips = load_used_ips()
    found = 0
    max_to_find = 50

    while found < max_to_find:
        cidr = random.choice(CF_IP_RANGES)
        ip_list = cidr_to_ips(cidr)
        random.shuffle(ip_list)

        for ip_num in ip_list:
            ip = ip_num_to_str(ip_num)
            if ip in used_ips:
                continue
            if is_port_open(ip, 443) or is_port_open(ip, 80):
                send_telegram_message(ip, 443 if is_port_open(ip, 443) else 80)
                save_used_ip(ip)
                used_ips.add(ip)
                found += 1
                if found >= max_to_find:
                    break

# Döwrebap işleýän mod
if __name__ == "__main__":
    while True:
        main()
        time.sleep(1800)  # 30 minut dynç alyş

