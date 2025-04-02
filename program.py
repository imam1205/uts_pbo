import mysql.connector
from datetime import datetime

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="zakat_db"
        )
    except mysql.connector.Error as e:
        print(f"Error: Gagal koneksi ke database - {str(e)}")
        exit(1)

def create_beras_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS beras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            harga DECIMAL(10,2)
        )
    ''')
    db.commit()

def create_payment_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(100),
            jumlah_jiwa INT,
            total_beras DECIMAL(10,2),
            total_uang DECIMAL(10,2),
            tanggal DATETIME
        )
    ''')
    db.commit()

def tambah_data_beras():
    db = connect_db()
    cursor = db.cursor()
    try:
        print("\n=== Tambah Data Beras ===")
        harga = float(input("Masukkan harga beras per Liter: Rp "))
        
        cursor.execute('''
            INSERT INTO beras (harga)
            VALUES (%s)
        ''', (harga,))
        db.commit()
        print("\nHarga beras berhasil ditambahkan!")
        
    except ValueError:
        print("Error: Harga harus berupa angka!")
    except Exception as e:
        print(f"Error: {str(e)}")

def tampilkan_data_beras():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM beras')
        hasil = cursor.fetchall()
        
        if not hasil:
            print("\nBelum ada data harga beras")
            return None
            
        print("\n=== Daftar Harga Beras ===")
        print("-" * 35)
        print(f"{'ID':^4} | {'Harga/Liter':^28}")
        print("-" * 35)
        
        for row in hasil:
            print(f"{row[0]:^4} | Rp {float(row[1]):>24,.2f}")
        print("-" * 35)
        return hasil
    except mysql.connector.Error as e:
        print(f"Error: Gagal mengambil data beras - {str(e)}")
        return None

def tampilkan_data_pembayaran():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM payment')
        hasil = cursor.fetchall()
        
        if not hasil:
            print("\nBelum ada data pembayaran")
            return None
            
        print("\n=== Data Pembayaran Zakat ===")
        print("-" * 80)
        print(f"{'ID':^4} | {'Nama':^20} | {'Jumlah Jiwa':^12} | {'Total Beras':^12} | {'Total Uang':^15}")
        print("-" * 80)
        
        for row in hasil:
            print(f"{row[0]:^4} | {row[1]:^20} | {row[2]:^12} | {float(row[3]):^12.2f} | Rp {float(row[4]):>11,.2f}")
        print("-" * 80)
        return hasil
    except mysql.connector.Error as e:
        print(f"Error: Gagal mengambil data pembayaran - {str(e)}")
        return None

def tambah_pembayaran():
    try:
        db = connect_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT harga FROM beras ORDER BY id DESC LIMIT 1')
        hasil = cursor.fetchone()
        
        if not hasil:
            print("\nError: Belum ada data harga beras!")
            return
            
        harga_beras = float(hasil[0])
        print("\n=== Pembayaran Zakat ===")
        nama = input("Masukkan nama: ")
        jumlah_jiwa = int(input("Masukkan jumlah jiwa: "))
        
        total_beras = jumlah_jiwa * 2.5  # 2.5 liter per jiwa
        total_uang = total_beras * harga_beras
        
        cursor.execute('''
            INSERT INTO payment (nama, jumlah_jiwa, total_beras, total_uang, tanggal)
            VALUES (%s, %s, %s, %s, %s)
        ''', (nama, jumlah_jiwa, total_beras, total_uang, datetime.now()))
        
        db.commit()
        print("\nPembayaran zakat berhasil dicatat!")
        print(f"Total yang harus dibayar: Rp {total_uang:,.2f}")
        
    except ValueError:
        print("Error: Input tidak valid!")
    except Exception as e:
        print(f"Error: {str(e)}")

try:
    db = connect_db()
    cursor = db.cursor()
    create_beras_table()
    create_payment_table(db)
except mysql.connector.Error as e:
    print(f"Database connection failed: {e}")
    exit(1)

try:
    while True:
        print("\n=== Menu ===")
        print("1. Tambah Data Beras")
        print("2. Tampilkan Data Beras")
        print("3. Tampilkan Data Pembayaran")
        print("4. Pembayaran Zakat")
        print("5. Keluar")
        
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == '1':
            tambah_data_beras()
        elif pilihan == '2':
            tampilkan_data_beras()
        elif pilihan == '3':
            tampilkan_data_pembayaran()
        elif pilihan == '4':
            tambah_pembayaran()
        elif pilihan == '5':
            print("Program selesai")
            break
        else:
            print("Pilihan tidak valid!")

finally:
    cursor.close()
    db.close()