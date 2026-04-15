from kanren.facts import Relation, facts
import kanren.core

# Definisikan relasi dasar
parent = Relation()

# Fakta-fakta orang tua-anak
facts(parent,
      ("Slamet", "Amin"),
      ("Slamet", "Anang"),
      ("Amin", "Badu"),
      ("Amin", "Budi"),
      ("Anang", "Didi"),
      ("Anang", "Dadi"))

# Variabel untuk query
x = kanren.core.var()

# Query Ayah dari Badu (sudah ada)
result_father = kanren.core.run(1, x, parent(x, "Badu"))
print("Ayah dari Badu :", result_father[0])

# --- TAMBAHKAN RELASI BARU ---

# 1. Relasi Paman (Uncle)
def uncle(parent_rel, child, potential_uncle):
    """
    potential_uncle adalah paman dari child jika:
    - ada seorang grandparent yang merupakan ayah dari father(child) dan juga ayah dari potential_uncle
    - dan potential_uncle != father(child)
    """
    father = kanren.core.var()
    grandparent = kanren.core.var()
    return kanren.core.lall(
        parent_rel(grandparent, father),   # grandparent adalah ayah dari father
        parent_rel(father, child),          # father adalah ayah dari child
        parent_rel(grandparent, potential_uncle),  # grandparent juga ayah dari potential_uncle
        kanren.core.ne(potential_uncle, father)   # potential_uncle bukan ayah dari child
    )

# Query Paman dari Badu
result_uncle = kanren.core.run(1, x, uncle(parent, "Badu", x))
if result_uncle:
    print("Paman dari Badu :", result_uncle[0])
else:
    print("Paman dari Badu : Tidak ditemukan")

# 2. Relasi Kakek (Grandfather)
def grandfather(parent_rel, child, grandpa):
    """
    grandpa adalah kakek dari child jika:
    - ada seorang father yang merupakan ayah dari child
    - dan grandpa adalah ayah dari father tersebut
    """
    father = kanren.core.var()
    return kanren.core.lall(parent_rel(grandpa, father), parent_rel(father, child))

# Query Kakek dari Badu
result_grandfather = kanren.core.run(1, x, grandfather(parent, "Badu", x))
if result_grandfather:
    print("Kakek dari Badu :", result_grandfather[0])
else:
    print("Kakek dari Badu : Tidak ditemukan")