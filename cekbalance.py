from web3 import Web3

# Konfigurasi RPC
rpc_url = "https://rpc.coinzax.com"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Cek koneksi ke RPC
if web3.is_connected():
    print("Connected to COINZAX RPC")
else:
    print("Failed to connect to COINZAX RPC")
    exit()

# Fungsi untuk mengecek saldo
def check_balance(address):
    balance = web3.eth.get_balance(address)
    balance_in_zax = web3.from_wei(balance, 'ether')  # Menggunakan web3.from_wei
    return balance_in_zax

# Baca file wallets.txt
with open("wallets.txt", "r") as file:
    wallets = file.read().splitlines()  # Membaca semua baris dan menghapus karakter newline

# Mengecek saldo untuk setiap wallet
for wallet in wallets:
    try:
        # Konversi alamat ke checksum address
        checksum_address = web3.to_checksum_address(wallet)
        balance = check_balance(checksum_address)
        print(f"Saldo ZAX di wallet {checksum_address}: {balance} ZAX")
    except Exception as e:
        print(f"Gagal mengecek saldo untuk wallet {wallet}: {str(e)}")