import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

# 1. Tiga potongan kode: fungsi, if/else, kelas dengan satu method
kode_fungsi = b"""def sapa(nama):
    return "halo " + nama
"""

kode_ifelse = b"""if x > 0:
    print("positif")
else:
    print("negatif")
"""

kode_kelas = b"""class Kucing:
    def suara(self):
        return "meong"
"""

print("--- 1. Fungsi ---")
tree = parser.parse(kode_fungsi)
print(tree.root_node)

print("\n--- 2. If/Else ---")
tree = parser.parse(kode_ifelse)
print(tree.root_node)

print("\n--- 3. Kelas ---")
tree = parser.parse(kode_kelas)
print(tree.root_node)

# 2. Periksa node anonim & bernama pada fungsi
print("\n--- Node Anonim vs Bernama (Fungsi) ---")
tree = parser.parse(kode_fungsi)
for c in tree.root_node.children[0].children:
    print(c.type, "bernama" if c.is_named else "anonim")

params = tree.root_node.children[0].child_by_field_name("parameters")
print("\nDi dalam parameters:")
for c in params.children:
    print(c.type, "bernama" if c.is_named else "anonim")

# 3. Rusak kode dengan sengaja (hapus ':')
print("\n--- Kode Rusak (tanpa ':') ---")
kode_rusak = b"""def sapa(nama)
    return "halo " + nama
"""
tree_rusak = parser.parse(kode_rusak)
print(tree_rusak.root_node)
