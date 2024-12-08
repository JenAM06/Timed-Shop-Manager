import json
import pwinput
from prettytable import PrettyTable
from datetime import datetime, timedelta

# buka file JSON
json_path = r"C:\Users\user\DDS 1\UAS_DDP\dataku.json"

# prsing data JSON
with open(json_path, "r") as jsondatabase:
    dataku = json.load(jsondatabase)

def simpan_json(dataku):
    with open(json_path, "w") as sondatabase:
        json.dump(dataku, sondatabase, indent=4)

def tentukan_waktu(dataku):
    jam = datetime.now().hour
    if 8 <= jam < 12:
        return dataku["pagi"]
    elif 12 <= jam < 18:
        return dataku["siang"]
    elif 18 <= jam < 22:
        return dataku["malam"]
    else:
        print("Toko sudah tutup.")

def tabel_produk():
    waktu = tentukan_waktu(dataku)
    tabel = PrettyTable()
    tabel.field_names = ["Nomor", "Produk", "Gems"]
    for produk in waktu:
        tabel.add_row([produk["nomor"], produk["produk"], produk["harga"]])
    print(tabel)

def toko_buka():
    buka = datetime.now().hour
    print("|==============================|")
    print("|           JEJE GLOW          |")
    print("|------------------------------|")
    if 8 <= buka < 12:
        print("|         Selamat Pagi         |")
    elif 12 <= buka < 18:
        print("|         Selamat Siang        |")
    elif 18 <= buka < 22:
        print("|         Selamat Malam        |")
    else:
        print("[#] Toko Tutup [#]")
        return
    print("|==============================|")
    login()

def login():
    ulang = 3
    while ulang > 0:
        try:
            print("\n=== Menu Login ===")
            username = input("Nama: ")
            password = pwinput.pwinput("PIN: ")
            for user in dataku["member"] + dataku["vip"]:
                if username == user["nama"]:
                    if user["blokir"] > datetime.now().timestamp():
                        buka = datetime.fromtimestamp(user["blokir"]).strftime("%H:%M:%S")
                        print(f"[!] Akun diblokir hingga {buka} WITA. Silakan coba lagi nanti.")
                        return
                    if password == user["pin"]:
                        if user in dataku["member"]:
                            menu_member(user)
                        else:
                            menu_vip(user)
                    ulang -= 1
                    print("\n[!] Login gagal [!]")
                    if ulang == 0:
                        user["blokir"] = (datetime.now() + timedelta(hours=3)).timestamp()
                        print("[!] Akun kakak diblokir selama 3 jam karena 3 kali salah login.")
                        simpan_json(dataku)
                    break
            else:
                ulang -= 1
                print("[!] username tidak ditemukan [!]")
                if ulang == 0:
                    print("[!] Kakak sudah mencoba 3 kali. Program berhenti.")
                    break
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def menu_vip(vip):
    while True:
        try:
            print("\n--✲-- Menu VIP --✲--")
            print("[1] Lihat produk")
            print("[2] Cek akun E-money")
            print("[3] Log out")
            pilihan = int(input("[✲] Pilih opsi (1/2/3): "))
            if pilihan == 1:
                beli_vip(vip)
            elif pilihan == 2:
                vip_emoney(vip)
            elif pilihan == 3:
                login()
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")

def beli_vip(vip):
    keranjang = []  
    total_gems = 0 
    while True:
        try:
            print("\n~~✧~~ Menu Beli ~~✧~~")
            print("[✧] Kategori Produk [✧]")
            print("[1] Masker ")
            print("[2] Skincare")
            print("[3] Diffuser & Lilin Aromaterapi")
            print("[✧]~~~~~~~~~~~~~~~~~~~~~~~~~~[✧]")
            kategori = int(input("[✧] Ayo Pilih (1/2/3): "))
            if kategori == 1:
                waktu = dataku["pagi"]
            elif kategori == 2:
                waktu = dataku["siang"]
            elif kategori == 3:
                waktu = dataku["malam"]
            else:
                print("[✧] Yah pilihannya tidak ada. Pilih lagi yuk!")
                continue
            print()
            tabel = PrettyTable()
            tabel.field_names = ["Nomor", "Produk", "Gems"]
            tabel.clear_rows()
            for produk in waktu:
                tabel.add_row([produk["nomor"], produk["produk"], produk["harga"]])
            print(tabel)
            while True:
                nomor = int(input("\n[✧] Masukkan nomor produk: "))
                jumlah = int(input("[✧] Masukkan jumlah produk: "))
                if 0 < nomor <= len(waktu):
                    produk = waktu[nomor - 1]
                    subtotal = produk["harga"] * jumlah
                    keranjang.append({"produk": produk["produk"], "jumlah": jumlah, "subtotal": subtotal})
                    total_gems += subtotal
                    print(f"[✧] {produk['produk']} sebanyak {jumlah} telah ditambahkan. Total sementara: {total_gems} gems.")
                else:
                    print("\n [!] Nomor produk tidak tersedia. Silakan coba lagi. [!]")
                tambah = input("[✧] Mau tambah produk dari kategori lain? (ya/ketik sembarang huruf untuk lanjutkan pembayaran): ").lower()
                break
            if tambah == "ya":
                continue
            else:
                break
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")
    print("\n[✧] Rincian belanja:")
    print("================================================================")
    for item in keranjang:
        print(f"[✧] {item['produk']} x{item['jumlah']} = {item['subtotal']} gems")
    print(f"[✧] Total belanja: {total_gems} gems.")
    print("================================================================")
    voucher = input("\n[✧] Masukkan kode voucher (tekan Enter jika tidak ada): ").strip()
    if voucher == "DES2":
        if vip["voucher"] > 0:
            vip["voucher"] -= 1
            total_gems -= int(0.1 * total_gems)
            print(f"[✧] Voucher berhasil digunakan! Total setelah diskon: {total_gems} gems.")
        else:
            print("[!] Maaf, voucher kakak sudah habis.[!]")
    elif voucher != "":
        print()
    else:
        print("[!] Voucher tidak valid.")
    transaksi = input("\n[✧] Konfirmasi pembayaran? (ya/ketik sembarang huruf untuk membatalkan): ").lower()
    if transaksi == "ya":
        if vip["gems"] >= total_gems:
            vip["gems"] -= total_gems
            simpan_json(dataku)
            print(f"\n[✧] Transaksi berhasil! Gems tersisa: {vip['gems']}.")
        else:
            print("[!] Maaf, gems kakak tidak cukup untuk melakukan transaksi.[!]")
    else:
        print("Transaksi dibatalkan.")


def vip_emoney(vip):
    while True:
        try:
            print("\n==$== Menu Akun E-Money ==$==")
            print(f"[$] Saldo kak {vip["nama"]}: Rp {vip["saldo"]}")
            print(f"[$] Gems kak {vip["nama"]}: {vip["gems"]}")
            print(f"Voucher kak {vip["nama"]}: {vip["voucher"]}  ")
            print("=============================")
            print("[1] Tukar Saldo dengan Gems")
            print("[2] Isi Saldo")
            print("[3] Kembali ke Menu VIP")
            pilihan = int(input("[$] Ayo dipilih (1/2/3): "))
            if pilihan == 1:
                tukar_vip(vip)
            elif pilihan == 2:
                isi_vip(vip)
            elif pilihan == 3:
                menu_vip(vip)
            else:
                print("[!] Pilihan tidak valid.")
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def tukar_vip(vip):
    while True:
        try:
            jumlah_gems = int(input("\n[$] Masukkan jumlah gems yang ingin diisi (1 gem = Rp. 2000): "))
            harga_gem = 2000  
            total_harga = jumlah_gems * harga_gem

            if vip["saldo"] >= total_harga:
                vip["saldo"] -= total_harga
                vip["gems"] += jumlah_gems
                if jumlah_gems == 50:
                    bonus_gems = 10
                    vip["gems"] += bonus_gems
                    print(f"[$] Selamat! kakak mendapatkan bonus {bonus_gems} gems!")
                simpan_json(dataku)
                print(f"[$] Gems berhasil diisi sebesar {jumlah_gems}. Gems kak {vip['nama']} sekarang: {vip['gems']}")
                print(f"[$] Saldo tersisa: Rp. {vip['saldo']}")
                return
            else:
                print(f"[!] yah saldo tidak cukup untuk mengisi {jumlah_gems} gems. Saldo kak {vip['nama']} saat ini: {vip['saldo']}")
                return
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def isi_vip(vip):
    while True:
        try:
            print("\n[◆] Isi saldo")
            print("[1] Rp. 50.000")
            print("[2] Rp. 100.000")
            print("[3] Rp. 150.000")
            print("[4] Rp. 250.000")
            angka = int(input("[◆] Masukkan angka (1/2/3/4):  "))
            if angka == 1:
                vip['saldo'] += 50000
            elif angka == 2:
                vip['saldo'] += 100000
            elif angka == 3:
                vip["saldo"] += 150000
            elif angka == 4:
                vip["saldo"] += 250000
            else:
                print("[!] Masukkan nomor sesuai pilihan yang disediakan ya kak")
                continue
            simpan_json(dataku)
            print(f"\n[◆] Saldo kakak berhasil diisi. Saldo sekarang: Rp {vip['saldo']}")
            return
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def menu_member(member):
    while True:
        try:
            print("\n+++++ Menu Member +++++")
            print("[1] Lihat Produk")
            print("[2] Cek Akun E-money")
            print("[3] Log out")
            pilihan = int(input("[+] Ayo dipilih (1/2/3): "))
            if pilihan == 1:
                beli_member(member)
            elif pilihan == 2:
                member_emoney(member)
            elif pilihan == 3:
                login()
            else:
                print("[!] Pilihan tidak valid.")
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def beli_member(member):
    while True:
        try:
            print("\n**** Menu Beli ****")
            tabel_produk()
            print("[1] Beli Produk")
            print("[2] Kembali")
            pilihan = int(input("[*] Ayo dipilih (1/2): "))
            if pilihan == 1:
                total_gems = 0
                waktu = tentukan_waktu(dataku)
                keranjang = []
                while True:
                    nomor = int(input("\n[*] Masukkan nomor produk: "))
                    jumlah = int(input("[*] Masukkan jumlah produk: "))
                    if 0 < nomor <= len(waktu):
                        produk = waktu[nomor - 1]
                        subtotal = produk["harga"] * jumlah
                        keranjang.append({"produk": produk["produk"], "jumlah": jumlah, "subtotal": subtotal})
                        total_gems += subtotal
                        print(f"[*] {produk['produk']} sebanyak {jumlah} telah ditambahkan. Total sementara: {total_gems} gems.")
                        tambah = input("[*] Mau tambah produk lagi? (ya/ketik sembarang huruf untuk lanjutkan pembayaran): ").lower()
                        if tambah != "ya":
                            break
                    else:
                        print("Nomor produk tidak tersedia. Silahkan coba lagi.")
                print("\n[*] Rincian belanja:")
                print("================================================================")
                for item in keranjang:
                    print(f"[*] {item['produk']} x{item['jumlah']} = {item['subtotal']} gems")
                print(f"[*] Total belanja: {total_gems} gems.")
                print("================================================================")
                voucher = input("\n[*] Masukkan kode voucher (atau tekan Enter jika tidak ada): ").strip()
                if voucher == "DES1":
                    if member["voucher"] > 0:
                        member["voucher"] -= 1
                        total_gems -= int(0.1 * total_gems)
                        print(f"[*] Voucher berhasil digunakan! Total belanja kakak: {total_gems} gems.")
                    else:
                        print("[!] Maaf, voucher kakak sudah habis.")
                        lanjut = input("[*] Apakah ingin melanjutkan transaksi tanpa voucher? (ya/ketik sembarang huruf untuk membatalkan): ").lower()
                        if lanjut != "ya":
                            print("Transaksi dibatalkan.")
                            break
                elif voucher == "":
                    print()
                else:
                    print("[!] Voucher tidak valid.")
                    break
                transaksi = input("[*] Konfirmasi pembayaran? (ya/ketik sembarang huruf untuk membatalkan pembayaran): ").lower()
                if transaksi == "ya":
                    if member["gems"] >= total_gems:
                        member["gems"] -= total_gems
                        simpan_json(dataku)
                        print(f"[*] Pembelian berhasil! Gems tersisa: {member['gems']}.")
                    else:
                        print("[!] Maaf, gems kakak tidak cukup untuk melakukan transaksi.")
                else:
                    print("Transaksi dibatalkan.")
                    break
            elif pilihan == 2:
                menu_member(member)
                break
            else:
                print("[!] Pilihan tidak valid.")
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def member_emoney(member):
    while True:
        try:
            print("\n===== Menu Akun E-Money =====")
            print(f"Saldo kak {member["nama"]}: Rp. {member["saldo"]}")
            print(f"Gems kak {member["nama"]}: {member["gems"]}")
            print(f"Voucher kak {member["nama"]}: {member["voucher"]}")
            print("=============================")
            print("[1] Tukar Saldo dengan Gems")
            print("[2] Isi Saldo")
            print("[3] Kembali ke Menu Member")
            pilihan = int(input("[=] Ayo dipillih (1/2/3): "))
            if pilihan == 1:
                tukar_member(member)
            elif pilihan == 2:
                isi_member(member)
            elif pilihan == 3:
                menu_member(member)
            else:
                print("[!] Pilihan tidak valid.")
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def tukar_member(member):
    while True:
        try:
            jumlah_gems = int(input("\n[=] Masukkan jumlah gems yang ingin diisi (1 gem = Rp. 2000): "))
            harga_gem = 2000  
            total_harga = jumlah_gems * harga_gem
            if member["saldo"] >= total_harga:
                member["saldo"] -= total_harga
                member["gems"] += jumlah_gems
                simpan_json(dataku)
                print(f"[=] Hore! gems berhasil diisi sebesar {jumlah_gems}. Gems kak {member['nama']} sekarang: {member['gems']}")
                print(f"[=] Saldo tersisa: Rp. {member['saldo']}")
                return
            else:
                print(f"[!] yah saldo tidak cukup untuk mengisi {jumlah_gems} gems. Saldo kak {member['nama']} saat ini: {member['saldo']}")
                return
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("[!] Kakak salah input, silahkan mengulang")

def isi_member(member):
    while True:
        try:
            print("\n=== Isi Saldo ===")
            print("[1] Rp. 50.000")
            print("[2] Rp. 100.000")
            print("[3] Rp. 250.000")
            angka = int(input("[=] Masukkan angka (1/2/3):  "))
            if angka == 1:
                member['saldo'] += 50000
            elif angka == 2:
                member['saldo'] += 100000
            elif angka == 3:
                member["saldo"] += 250000
            else:
                print("[!] Masukkan nomor sesuai pilihan yang disediakan ya kak")
                continue
            simpan_json(dataku)
            print(f"[=] Saldo kakak berhasil diisi. Saldo sekarang: Rp {member['saldo']}")
            return
        except ValueError:
            print("[!] Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")

toko_buka()