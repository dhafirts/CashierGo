
# =====================================================
# CASHIERGO
# Sistem Pemesanan Makanan dan Pengelolaan Kasir
# Mata Kuliah: Algoritma dan Pemrograman
# Penyimpanan: menu.csv, transaksi.csv, diskon.csv
# =====================================================

import pandas as pd
import os


# =====================================================
# BAGIAN 1: PERSIAPAN FILE
# =====================================================

FOLDER = os.path.dirname(os.path.abspath(__file__))

FILE_MENU = os.path.join(FOLDER, "menu.csv")
FILE_TRANSAKSI = os.path.join(FOLDER, "transaksi.csv")
FILE_DISKON = os.path.join(FOLDER, "diskon.csv")

KOLOM_MENU = ["id_menu", "nama_menu", "kategori", "harga", "stok"]

KOLOM_TRANSAKSI = [
    "id_transaksi", "nama_menu", "jumlah", "harga_satuan",
    "subtotal", "metode_pembayaran", "total_pembelian",
    "diskon", "total_bayar"
]

KOLOM_DISKON = ["minimal_pembelian", "persentase_diskon"]


def siapkan_file():
    # Membuat file menu jika belum tersedia
    try:
        pd.read_csv(FILE_MENU)
    except FileNotFoundError:
        data = pd.DataFrame(columns=KOLOM_MENU)
        data.to_csv(FILE_MENU, index=False)

    # Membuat file transaksi jika belum tersedia
    try:
        pd.read_csv(FILE_TRANSAKSI)
    except FileNotFoundError:
        data = pd.DataFrame(columns=KOLOM_TRANSAKSI)
        data.to_csv(FILE_TRANSAKSI, index=False)

    # Membuat file diskon jika belum tersedia
    try:
        pd.read_csv(FILE_DISKON)
    except FileNotFoundError:
        data = pd.DataFrame({
            "minimal_pembelian": [0],
            "persentase_diskon": [0]
        })
        data.to_csv(FILE_DISKON, index=False)


# =====================================================
# BAGIAN 2: FUNGSI BANTU
# =====================================================

def baca_menu():
    data = pd.read_csv(FILE_MENU)

    if not data.empty:
        data = data.astype({
            "id_menu": int,
            "nama_menu": str,
            "kategori": str,
            "harga": int,
            "stok": int
        })

    return data


def simpan_menu(data):
    data.to_csv(FILE_MENU, index=False)


def baca_transaksi():
    return pd.read_csv(FILE_TRANSAKSI)


def simpan_transaksi(data):
    data.to_csv(FILE_TRANSAKSI, index=False)


def baca_diskon():
    data = pd.read_csv(FILE_DISKON)

    minimal = int(data.at[0, "minimal_pembelian"])
    persen = float(data.at[0, "persentase_diskon"])

    return minimal, persen


def simpan_diskon(minimal, persen):
    data = pd.DataFrame({
        "minimal_pembelian": [minimal],
        "persentase_diskon": [persen]
    })

    data.to_csv(FILE_DISKON, index=False)


def format_rupiah(angka):
    return "Rp" + f"{angka:,.0f}".replace(",", ".")


def minta_angka(pesan, minimal=0):
    while True:
        teks = input(pesan).strip()

        if teks.isdigit() and int(teks) >= minimal:
            return int(teks)

        print("Input tidak valid. Masukkan angka minimal", minimal)


def minta_ya_tidak(pesan):
    while True:
        jawab = input(pesan).strip().lower()

        if jawab == "y" or jawab == "ya":
            return True
        elif jawab == "n" or jawab == "tidak":
            return False

        print("Jawab dengan y atau n.")


def pilih_kategori():
    while True:
        print("1. Makanan")
        print("2. Minuman")

        pilihan = input("Pilih kategori: ").strip()

        if pilihan == "1":
            return "Makanan"
        elif pilihan == "2":
            return "Minuman"

        print("Pilihan tidak valid.")



def tampilkan_menu(data):
    if data.empty:
        print("Belum ada data menu.")
    else:
        tabel = data.copy()

        # Mengubah kolom harga menjadi teks terlebih dahulu
        tabel["harga"] = tabel["harga"].apply(format_rupiah)

        print(tabel.to_string(index=False))

    


def tekan_enter():
    input("\nTekan Enter untuk kembali...")


# =====================================================
# BAGIAN 3: KELOLA MENU (CRUD)
# =====================================================

def tambah_menu():
    print("\n--- TAMBAH MENU ---")

    data = baca_menu()

    nama = input("Nama menu: ").strip()

    if nama == "":
        print("Nama menu tidak boleh kosong.")
        return

    # Memeriksa apakah nama menu sudah tersedia
    for i in range(len(data)):
        nama_lama = str(data.iloc[i]["nama_menu"])

        if nama_lama.lower() == nama.lower():
            print("Menu tersebut sudah tersedia.")
            return

    # Menentukan ID baru
    id_baru = 1

    for i in range(len(data)):
        if int(data.iloc[i]["id_menu"]) >= id_baru:
            id_baru = int(data.iloc[i]["id_menu"]) + 1

    kategori = pilih_kategori()
    harga = minta_angka("Harga: Rp", 1)
    stok = minta_angka("Stok: ", 0)

    menu_baru = pd.DataFrame([{
        "id_menu": id_baru,
        "nama_menu": nama,
        "kategori": kategori,
        "harga": harga,
        "stok": stok
    }])

    data = pd.concat([data, menu_baru], ignore_index=True)

    simpan_menu(data)

    print("Menu berhasil ditambahkan.")


def tampilkan_semua_menu():
    print("\n--- DAFTAR MENU ---")

    data = baca_menu()
    tampilkan_menu(data)


def cari_menu():
    print("\n--- CARI MENU ---")

    data = baca_menu()

    kata = input("Masukkan ID atau nama menu: ").strip()

    if kata == "":
        print("Kata pencarian tidak boleh kosong.")
        return

    hasil = data[
        (data["id_menu"].astype(str) == kata) |
        (data["nama_menu"].str.contains(kata, case=False, na=False))
    ]

    if not hasil.empty:
        print("Menu ditemukan:")
        tampilkan_menu(hasil)
    else:
        print("Menu tidak ditemukan.")


def edit_menu():
    print("\n--- EDIT MENU ---")

    data = baca_menu()

    if data.empty:
        print("Belum ada data menu.")
        return

    tampilkan_menu(data)

    id_edit = minta_angka(
        "Masukkan ID menu yang diedit (0 = kembali): ", 0
    )

    if id_edit == 0:
        return

    hasil = data[data["id_menu"] == id_edit]

    if hasil.empty:
        print("ID menu tidak ditemukan.")
        return

    indeks = hasil.index[0]

    print("\nKosongkan input jika tidak ingin mengubah data.")

    # Mengubah nama menu
    nama_lama = str(data.at[indeks, "nama_menu"])

    nama_baru = input(
        f"Nama baru [{nama_lama}]: "
    ).strip()

    if nama_baru != "":
        nama_kembar = data[
            (data["nama_menu"].str.lower() == nama_baru.lower()) &
            (data["id_menu"] != id_edit)
        ]

        if not nama_kembar.empty:
            print("Nama menu sudah digunakan.")
            return

        data.at[indeks, "nama_menu"] = nama_baru

    # Mengubah kategori
    kategori_lama = str(data.at[indeks, "kategori"])

    while True:
        print("\n1. Makanan")
        print("2. Minuman")

        kategori = input(
            f"Kategori baru [{kategori_lama}]: "
        ).strip()

        if kategori == "":
            break
        elif kategori == "1":
            data.at[indeks, "kategori"] = "Makanan"
            break
        elif kategori == "2":
            data.at[indeks, "kategori"] = "Minuman"
            break
        else:
            print("Pilihan kategori tidak valid.")

    # Mengubah harga
    harga_lama = int(data.at[indeks, "harga"])

    while True:
        harga = input(
            f"Harga baru [{harga_lama}]: "
        ).strip()

        if harga == "":
            break
        elif harga.isdigit() and int(harga) > 0:
            data.at[indeks, "harga"] = int(harga)
            break
        else:
            print("Harga harus berupa angka lebih dari 0.")

    # Mengubah stok
    stok_lama = int(data.at[indeks, "stok"])

    while True:
        stok = input(
            f"Stok baru [{stok_lama}]: "
        ).strip()

        if stok == "":
            break
        elif stok.isdigit():
            data.at[indeks, "stok"] = int(stok)
            break
        else:
            print("Stok harus berupa angka 0 atau lebih.")

    # Menyimpan perubahan
    simpan_menu(data)

    print("\nMenu berhasil diubah!")

    tampilkan_menu(
        data[data["id_menu"] == id_edit]
    )


def hapus_menu():
    print("\n--- HAPUS MENU ---")

    data = baca_menu()

    if data.empty:
        print("Belum ada data menu.")
        return

    tampilkan_menu(data)

    id_hapus = minta_angka(
        "Masukkan ID menu yang dihapus (0 = kembali): ", 0
    )

    if id_hapus == 0:
        return

    hasil = data[data["id_menu"] == id_hapus]

    if hasil.empty:
        print("ID menu tidak ditemukan.")
        return

    nama = hasil.iloc[0]["nama_menu"]

    if minta_ya_tidak(f"Yakin menghapus {nama}? (y/n): "):
        data = data[data["id_menu"] != id_hapus]

        data = data.reset_index(drop=True)

        simpan_menu(data)

        print("Menu berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")


def kelola_menu():
    while True:
        print("\n========== KELOLA MENU ==========")
        print("1. Tambah Menu")
        print("2. Tampilkan Semua Menu")
        print("3. Cari Menu")
        print("4. Edit Menu")
        print("5. Hapus Menu")
        print("0. Kembali")

        pilihan = input("Pilih: ").strip()

        if pilihan == "1":
            tambah_menu()
        elif pilihan == "2":
            tampilkan_semua_menu()
        elif pilihan == "3":
            cari_menu()
        elif pilihan == "4":
            edit_menu()
        elif pilihan == "5":
            hapus_menu()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")


# =====================================================
# BAGIAN 4: ATUR DISKON
# =====================================================

def atur_diskon():
    while True:
        minimal, persen = baca_diskon()

        print("\n========== ATUR DISKON ==========")
        print("Minimal pembelian :", format_rupiah(minimal))
        print("Persentase diskon :", persen, "%")
        print("---------------------------------")
        print("1. Ubah Pengaturan Diskon")
        print("0. Kembali ke Menu Utama")
        print("=================================")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            minimal_baru = minta_angka(
                "Minimal pembelian baru: Rp", 0
            )

            while True:
                teks = input(
                    "Persentase diskon baru (0-100): "
                ).strip()

                try:
                    persen_baru = float(teks)

                    if 0 <= persen_baru <= 100:
                        break
                    else:
                        print("Diskon harus antara 0 sampai 100.")

                except ValueError:
                    print("Masukkan angka yang benar.")

            if minta_ya_tidak("Simpan pengaturan diskon? (y/n): "):
                simpan_diskon(minimal_baru, persen_baru)
                print("Pengaturan diskon berhasil disimpan.")
            else:
                print("Perubahan diskon dibatalkan.")

        elif pilihan == "0":
            print("Kembali ke menu utama.")
            break

        else:
            print("Pilihan tidak valid.")


# =====================================================
# BAGIAN 5: FITUR KASIR
# =====================================================

def buat_id_transaksi():
    data = baca_transaksi()

    if data.empty:
        nomor = 1
    else:
        transaksi_unik = data["id_transaksi"].nunique()
        nomor = transaksi_unik + 1

    return "T" + str(nomor).zfill(3)


def fitur_kasir():
    print("\n--- FITUR KASIR ---")

    data_menu = baca_menu()

    if data_menu.empty:
        print("Belum ada menu. Tambahkan menu terlebih dahulu.")
        tekan_enter()
        return

    minimal, persen = baca_diskon()

    keranjang = []

    # Tahap 1: Memilih menu
    while True:
        tampilkan_menu(data_menu)

        id_pilih = minta_angka(
            "Pilih ID menu (0 = batal): ", 0
        )

        if id_pilih == 0:
            print("Transaksi dibatalkan.")
            tekan_enter()
            return

        hasil = data_menu[data_menu["id_menu"] == id_pilih]

        if hasil.empty:
            print("Menu tidak ditemukan.")
            continue

        menu = hasil.iloc[0]

        # Menghitung jumlah menu yang sudah dipesan
        sudah_dipesan = 0

        for item in keranjang:
            if item["id"] == id_pilih:
                sudah_dipesan = item["jumlah"]

        sisa_stok = int(menu["stok"]) - sudah_dipesan

        if sisa_stok <= 0:
            print("Stok menu habis.")
            continue

        jumlah = minta_angka("Jumlah pesanan: ", 1)

        if jumlah > sisa_stok:
            print("Stok tidak cukup. Sisa stok:", sisa_stok)
            continue

        sudah_ada = False

        for item in keranjang:
            if item["id"] == id_pilih:
                item["jumlah"] += jumlah
                sudah_ada = True

        if not sudah_ada:
            keranjang.append({
                "id": id_pilih,
                "nama": menu["nama_menu"],
                "jumlah": jumlah,
                "harga": int(menu["harga"])
            })

        print("Menu berhasil ditambahkan.")

        if not minta_ya_tidak("Tambah menu lagi? (y/n): "):
            break

    # Tahap 2: Menampilkan keranjang
    if len(keranjang) == 0:
        print("Keranjang kosong.")
        tekan_enter()
        return

    print("\n--- KERANJANG PESANAN ---")

    for item in keranjang:
        subtotal = item["jumlah"] * item["harga"]

        print(
            item["nama"],
            "|", item["jumlah"], "x",
            format_rupiah(item["harga"]),
            "=", format_rupiah(subtotal)
        )

    # Tahap 3: Menghitung pembayaran
    total_pembelian = 0

    for item in keranjang:
        total_pembelian += item["jumlah"] * item["harga"]

    diskon = 0

    if total_pembelian >= minimal and persen > 0:
        diskon = int(round(total_pembelian * persen / 100))

    total_bayar = total_pembelian - diskon

    print("\n--- RINCIAN PEMBAYARAN ---")
    print("Total pembelian :", format_rupiah(total_pembelian))
    print("Diskon          :", format_rupiah(diskon))
    print("Total bayar     :", format_rupiah(total_bayar))

    # Tahap 4: Memilih metode pembayaran
    while True:
        print("\n1. Cash")
        print("2. QRIS")

        pilihan = input("Metode pembayaran: ").strip()

        if pilihan == "1":
            metode = "Cash"
            break
        elif pilihan == "2":
            metode = "QRIS"
            break
        else:
            print("Pilihan tidak valid.")

    # Tahap 5: Konfirmasi transaksi
    if not minta_ya_tidak("Konfirmasi transaksi? (y/n): "):
        print("Transaksi dibatalkan. Stok tidak berubah.")
        tekan_enter()
        return

    # Membuat data transaksi
    id_transaksi = buat_id_transaksi()

    baris_transaksi = []

    for i in range(len(keranjang)):
        item = keranjang[i]

        subtotal = item["jumlah"] * item["harga"]

        if i == 0:
            total = total_pembelian
            potongan = diskon
            bayar = total_bayar
        else:
            total = ""
            potongan = ""
            bayar = ""

        baris_transaksi.append({
            "id_transaksi": id_transaksi,
            "nama_menu": item["nama"],
            "jumlah": item["jumlah"],
            "harga_satuan": item["harga"],
            "subtotal": subtotal,
            "metode_pembayaran": metode,
            "total_pembelian": total,
            "diskon": potongan,
            "total_bayar": bayar
        })

    transaksi_baru = pd.DataFrame(baris_transaksi)

    data_transaksi = baca_transaksi()

    data_transaksi = pd.concat(
        [data_transaksi, transaksi_baru],
        ignore_index=True
    )

    simpan_transaksi(data_transaksi)

    # Tahap 6: Mengurangi stok menu
    for item in keranjang:
        hasil = data_menu[data_menu["id_menu"] == item["id"]]

        if not hasil.empty:
            indeks = hasil.index[0]

            stok_baru = (
                int(data_menu.at[indeks, "stok"]) - item["jumlah"]
            )

            data_menu.at[indeks, "stok"] = stok_baru

    simpan_menu(data_menu)

    print("\nTransaksi", id_transaksi, "berhasil disimpan.")

    tekan_enter()


# =====================================================
# BAGIAN 6: REKAP PENGHASILAN
# =====================================================

def rekap_penghasilan():
    print("\n========== REKAP PENGHASILAN ==========")

    transaksi = baca_transaksi()
    menu = baca_menu()

    if transaksi.empty:
        print("Belum ada transaksi.")
        tekan_enter()
        return

    # Mengambil baris pertama setiap transaksi
    data_total = transaksi[transaksi["total_bayar"].notna()]

    jumlah_transaksi = len(data_total)

    total_pendapatan = data_total["total_bayar"].sum()

    cash = data_total[
        data_total["metode_pembayaran"] == "Cash"
    ]["total_bayar"].sum()

    qris = data_total[
        data_total["metode_pembayaran"] == "QRIS"
    ]["total_bayar"].sum()

    print("Jumlah transaksi :", jumlah_transaksi)
    print("Total pendapatan :", format_rupiah(total_pendapatan))
    print("Pendapatan Cash  :", format_rupiah(cash))
    print("Pendapatan QRIS  :", format_rupiah(qris))

    # Menghitung jumlah menu yang terjual
    if not menu.empty:
        data_terjual = transaksi.groupby("nama_menu")["jumlah"].sum()

        menu["terjual"] = menu["nama_menu"].map(data_terjual)
        menu["terjual"] = menu["terjual"].fillna(0).astype(int)

        terbanyak = menu["terjual"].max()

        if terbanyak == 0:
            print("Menu terlaris: Belum ada penjualan.")
        else:
            menu_terlaris = menu[
                menu["terjual"] == terbanyak
            ]["nama_menu"].tolist()

            print(
                "Menu terlaris :",
                ", ".join(menu_terlaris),
                "(", terbanyak, "terjual)"
            )

        print("\n--- RINCIAN PER MENU ---")

        tabel = menu[["nama_menu", "terjual", "stok"]]

        tabel = tabel.rename(columns={
            "nama_menu": "Nama Menu",
            "terjual": "Terjual",
            "stok": "Sisa Stok"
        })

        print(tabel.to_string(index=False))

    tekan_enter()


# =====================================================
# BAGIAN 7: MENU UTAMA
# =====================================================

def tampilkan_menu_utama():
    print("\n=================================")
    print("            CASHIERGO")
    print("     SISTEM PEMESANAN MAKANAN")
    print("=================================")
    print("1. Kelola Menu")
    print("2. Atur Diskon")
    print("3. Fitur Kasir")
    print("4. Rekap Penghasilan")
    print("0. Keluar")
    print("=================================")


def menu_utama():
    berjalan = True

    while berjalan:
        tampilkan_menu_utama()

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            kelola_menu()
        elif pilihan == "2":
            atur_diskon()
        elif pilihan == "3":
            fitur_kasir()
        elif pilihan == "4":
            rekap_penghasilan()
        elif pilihan == "0":
            print("Terima kasih telah menggunakan CashierGo.")
            berjalan = False
        else:
            print("Pilihan tidak valid.")


# =====================================================
# PROGRAM UTAMA
# =====================================================

siapkan_file()
menu_utama()
