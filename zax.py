import os
import requests
import time
from colorama import Fore, Style, init

# Fungsi untuk membersihkan layar terminal
def clear_screen():
    # Untuk Windows
    if os.name == "nt":
        os.system("cls")
    # Untuk Unix/Linux/MacOS
    else:
        os.system("clear")

# Inisialisasi colorama untuk warna di terminal
init(autoreset=True)

# Banner
BANNER = f"""
{Fore.CYAN}
     █████╗ ██╗   ██╗████████╗ ██████╗
    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
    ███████║██║   ██║   ██║   ██║   ██║  
    ██╔══██║██║   ██║   ██║   ██║   ██║ 
    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝
{Style.RESET_ALL}
Auto Claim Script with Proxy
{Fore.YELLOW}Telegram : https://t.me/airdropfetchofficial{Style.RESET_ALL}
"""

# Fungsi untuk mendapatkan IP publik menggunakan proxy
def get_public_ip(proxy):
    try:
        response = requests.get(
            "https://api64.ipify.org/?format=json",
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["ip"]
        else:
            return None
    except:
        return None

# Fungsi untuk melakukan claim
def claim(wallet_address, user_ip, proxy):
    url = "https://server.coinzax.com/claim"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "connection": "keep-alive",
        "content-length": "89",
        "content-type": "application/json",
        "host": "server.coinzax.com",
        "origin": "https://claim.coinzax.com",
        "referer": "https://claim.coinzax.com/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
    }
    payload = {
        "walletAddress": wallet_address,
        "userIP": user_ip
    }
    try:
        response = requests.post(url, json=payload, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ Successfully claimed for {wallet_address} using IP {user_ip} (Proxy: {proxy}){Style.RESET_ALL}")
            return True  # Berhasil claim
        else:
            print(f"{Fore.RED}❌ Failed to claim for {wallet_address}. Status code: {response.status_code} (Proxy: {proxy}){Style.RESET_ALL}")
            return False  # Gagal claim
    except Exception as e:
        # Jika terjadi timeout atau error, asumsikan claim sudah berhasil
        print(f"{Fore.YELLOW}⚠️ Assuming claim succeeded for {wallet_address} (Proxy: {proxy}) due to server timeout or error: {e}{Style.RESET_ALL}")
        return True  # Asumsikan berhasil

# Main function
def main():
    clear_screen()
    print(BANNER)

    # Baca daftar wallet dari file
    try:
        with open("wallets.txt", "r") as file:
            wallets = file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}❌ File 'wallets.txt' not found.{Style.RESET_ALL}")
        return

    # Baca daftar proxy dari file
    try:
        with open("proxies.txt", "r") as file:
            proxies = file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}❌ File 'proxies.txt' not found.{Style.RESET_ALL}")
        return

    # Loop untuk mengclaim semua wallet
    for wallet in wallets:
        # Garis pembatas berwarna biru cerah
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

        claimed = False  # Flag untuk menandai apakah claim berhasil
        proxy_index = 0  # Indeks proxy yang sedang digunakan
        inactive_proxies = []  # Daftar proxy yang tidak aktif

        print(f"{Fore.YELLOW}🔍 Processing wallet: {wallet}{Style.RESET_ALL}")

        while not claimed and proxy_index < len(proxies):
            proxy = proxies[proxy_index]
            public_ip = get_public_ip(proxy)

            if public_ip:
                print(f"{Fore.GREEN}✅ Found active proxy: {proxy} with IP {public_ip}{Style.RESET_ALL}")
                claimed = claim(wallet, public_ip, proxy)
            else:
                inactive_proxies.append(proxy)  # Catat proxy yang tidak aktif

            # Jika claim gagal, coba proxy berikutnya
            if not claimed:
                proxy_index += 1

        # Tampilkan pesan "Skipping to next proxy" hanya sekali di akhir
        if inactive_proxies:
            print(f"{Fore.RED}⚠️ Skipped {len(inactive_proxies)} inactive proxies.{Style.RESET_ALL}")

        # Jika semua proxy sudah dicoba dan masih gagal
        if not claimed:
            print(f"{Fore.RED}❌ Failed to claim for {wallet} after trying all proxies.{Style.RESET_ALL}")

        # Jeda waktu antara setiap claim untuk menghindari rate limiting
        time.sleep(10)

    # Garis pembatas berwarna biru cerah di akhir
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🎉 All wallets processed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()