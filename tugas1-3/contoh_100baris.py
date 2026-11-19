# Contoh kode Python nyata untuk pengujian jelajah.py (>= 100 baris)

class Mahasiswa:
    def __init__(self, nim, nama, prodi):
        self.nim = nim
        self.nama = nama
        self.prodi = prodi
        self.nilai = []

    def tambah_nilai(self, mata_kuliah, nilai):
        if 0 <= nilai <= 100:
            self.nilai.append({"matkul": mata_kuliah, "skor": nilai})
        else:
            print("Nilai tidak valid!")

    def hitung_rata_rata(self):
        if not self.nilai:
            return 0.0
        total = sum(item["skor"] for item in self.nilai)
        return total / len(self.nilai)

    def status_kelulusan(self):
        rata_rata = self.hitung_rata_rata()
        if rata_rata >= 70:
            return "Lulus"
        elif rata_rata >= 50:
            return "Remedial"
        else:
            return "Tidak Lulus"


class SistemAkademik:
    def __init__(self):
        self.daftar_mahasiswa = {}

    def daftarkan_mahasiswa(self, nim, nama, prodi):
        if nim in self.daftar_mahasiswa:
            print(f"Mahasiswa dengan NIM {nim} sudah terdaftar.")
            return False
        mhs = Mahasiswa(nim, nama, prodi)
        self.daftar_mahasiswa[nim] = mhs
        return True

    def input_nilai(self, nim, matkul, nilai):
        if nim in self.daftar_mahasiswa:
            self.daftar_mahasiswa[nim].tambah_nilai(matkul, nilai)
            return True
        print("Mahasiswa tidak ditemukan.")
        return False

    def cari_mahasiswa(self, nim):
        return self.daftar_mahasiswa.get(nim, None)

    def cetak_semua_laporan(self):
        print("=" * 40)
        print("LAPORAN AKADEMIK MAHASISWA")
        print("=" * 40)
        for nim, mhs in self.daftar_mahasiswa.items():
            print(f"NIM   : {mhs.nim}")
            print(f"Nama  : {mhs.nama}")
            print(f"Prodi : {mhs.prodi}")
            print(f"Rata-rata: {mhs.hitung_rata_rata():.2f}")
            print(f"Status: {mhs.status_kelulusan()}")
            print("-" * 40)


def saring_mahasiswa_lulus(sistem):
    lulus = []
    for mhs in sistem.daftar_mahasiswa.values():
        if mhs.status_kelulusan() == "Lulus":
            lulus.append(mhs.nama)
    return lulus


def demo_data():
    sistem = SistemAkademik()
    sistem.daftarkan_mahasiswa("202401", "Budi Santoso", "Teknik Informatika")
    sistem.daftarkan_mahasiswa("202402", "Siti Aminah", "Teknik Informatika")
    sistem.daftarkan_mahasiswa("202403", "Ahmad Fauzi", "Sistem Informasi")

    sistem.input_nilai("202401", "Pemrograman Lanjut", 85)
    sistem.input_nilai("202401", "Struktur Data", 78)
    sistem.input_nilai("202402", "Pemrograman Lanjut", 65)
    sistem.input_nilai("202402", "Struktur Data", 55)
    sistem.input_nilai("202403", "Pemrograman Lanjut", 40)
    sistem.input_nilai("202403", "Struktur Data", 45)

    return sistem


def main():
    sistem = demo_data()
    sistem.cetak_semua_laporan()
    daftar_lulus = saring_mahasiswa_lulus(sistem)
    print(f"Total mahasiswa lulus: {len(daftar_lulus)}")
    for nama in daftar_lulus:
        print(f"- {nama}")


if __name__ == "__main__":
    main()
