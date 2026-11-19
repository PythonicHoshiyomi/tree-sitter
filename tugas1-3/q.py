import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

if len(sys.argv) < 3:
    print(f"Penggunaan: python {sys.argv[0]} <file.py> <query.scm>")
    sys.exit(1)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)
query = Query(PY, pola)

capture_names = [query.capture_name(i) for i in range(query.capture_count)]

if "nama" in capture_names and "params" in capture_names:
    for _, cap in QueryCursor(query).matches(tree.root_node):
        nama = cap["nama"][0].text.decode()
        jumlah = cap["params"][0].named_child_count
        print(f"Fungsi: {nama:<25} Jumlah parameter: {jumlah}")
elif "docstring" in capture_names:
    for _, cap in QueryCursor(query).matches(tree.root_node):
        nama = cap["nama"][0].text.decode() if "nama" in cap else "-"
        doc = cap["docstring"][0].text.decode().strip()
        print(f"Fungsi: {nama}\nDocstring: {doc}\n")
else:
    hasil = QueryCursor(query).captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in nodes:
            teks = n.text.decode().strip().replace("\n", " ")
            print(f"@{nama}  baris {n.start_point[0] + 1}: {teks}")
