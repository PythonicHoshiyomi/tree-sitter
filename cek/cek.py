import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNC = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        err = cari_error(child)
        if err:
            return err
    return None

def cek_file(path):
    try:
        konten = path.read_bytes()
    except Exception as e:
        print(f"Gagal membaca {path}: {e}")
        return

    tree = parser.parse(konten)

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO/FIXME] {path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNC).matches(tree.root_node):
        node_fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        baris_awal = node_fungsi.start_point[0] + 1
        baris_akhir = node_fungsi.end_point[0] + 1
        jumlah_baris = baris_akhir - baris_awal + 1
        if jumlah_baris > 30:
            print(f"[FUNGSI PANJANG] {path}:{baris_awal}: fungsi '{nama}' ({jumlah_baris} baris)")

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        err_node = cari_error(tree.root_node)
        baris_err = err_node.start_point[0] + 1 if err_node else 1
        print(f"[ERROR SINTAKS] {path}:{baris_err}: file mengandung kesalahan sintaks")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Penggunaan: python {sys.argv[0]} <folder>")
        sys.exit(1)

    target_dir = Path(sys.argv[1])
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__"}

    for path in target_dir.rglob("*.py"):
        if any(part in ignored for part in path.parts):
            continue
        cek_file(path)
