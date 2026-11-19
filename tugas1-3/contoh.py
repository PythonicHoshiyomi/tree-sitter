import os
import sys
from pathlib import Path
from math import sqrt, pi

def halo():
    """Fungsi sapaan tanpa parameter."""
    print("Halo dunia!")

def tambah(a, b):
    """Menjumlahkan dua buah bilangan."""
    hasil = a + b
    print("Hasil penjumlahan:", hasil)
    return hasil

def hitung_luas_lingkaran(radius):
    """Menghitung luas lingkaran berdasarkan jari-jari."""
    return pi * (radius ** 2)

def info_mahasiswa(nama, nim, jurusan="Informatika"):
    """Mencetak info mahasiswa dengan tiga parameter."""
    print(f"Mahasiswa: {nama}, NIM: {nim}, Jurusan: {jurusan}")

if __name__ == "__main__":
    halo()
    tambah(10, 20)
    print("Luas r=7:", hitung_luas_lingkaran(7))
    info_mahasiswa("Budi", "12345")
