#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import requests
import time
import random
from datetime import datetime
import os

# === Telegram sazlamalar ===
TELEGRAM_TOKEN = "7853273196:AAGdXBhl2x4FS3QQOKU5cabM13L1q_VAoM0"
CHAT_ID = "1753028724"

# === CF ulanýan saýtlaryň sanawy ===
saytlar = [
    "https://animepahe.ru",
    "https://cryptobrowser.site",
    "https://filmix.ac",
    "https://protonvpn.com",
    "https://www.udemy.com",
    "https://sflix.to",
    "https://kissasian.lu",
    "https://www.cloudflare.com",
    "https://www.fembed.com",
    "https://www.gogoanime.dk",
    "https://gogoanime.wiki"
]

# === Netije faýly ===
netije_faýl = "cf_ips_turkmenistan.txt"

# === IP-leri okap gaýtalanmaz ýaly sakla ===
def oku_bar_ipler():
    if os.path.exists(netije_faýl):
        with open(netije_faýl, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

# === URL-den IP almak ===
def url_ip_al(url):
    try:
        domen = url.split("//")[-1].split("/")[0]
        return socket.gethostbyname(domen)
    except Exception:
        return None

# === Telegram habary ugratmak ===
def telegram_ugrat(habar):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": habar
        })
    except Exception as e:
        print(f"Telegram ýalňyşlygy: {e}")

# === Baş iş prosesi ===
def bashla():
    bar_ipler = oku_bar_ipler()
    täze_ipler = set()
    habarnama = ""

    for sayt in saytlar:
        ip = url_ip_al(sayt)
        if ip and ip not in bar_ipler:
            if random.random() <= 0.75:
                täze_ipler.add(ip)
                bar_ipler.add(ip)
                habarnama += f"✅ {sayt} ➜ {ip}\n"
                print(f"[+] Täze IP: {ip} ({sayt})")
            else:
                print(f"[×]  çykaryldy (blok bolmagy ähtimal): {ip}")
        time.sleep(1)

    if täze_ipler:
        with open(netije_faýl, "a") as f:
            for ip in täze_ipler:
                f.write(ip + "\n")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        telegram_ugrat(f"🕒 {timestamp}\nTäze Cloudflare IP-ler:\n{habarnama}")
    else:
        telegram_ugrat("⚠️ Täze IP tapylmady.")

# === Hemişelik işleýän sikl ===
if __name__ == "__main__":
    while True:
        print("🔁 CF IP gözleg başlaýar...")
        bashla()
        print("⏳ Indiki gözleg üçin 1 sagat garaşylýar...")
        time.sleep(3600)
