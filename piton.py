from kanren.facts import Relation, facts
from kanren.core import var, run, conde, lall

# Definisikan relasi dasar
orang_tua = Relation()

# Fakta-fakta orang tua-anak
facts(orang_tua,
      ("Slamet", "Amin"),
      ("Slamet", "Anang"),
      ("Amin", "Badu"),
      ("Amin", "Budi"),
      ("Anang", "Didi"),
      ("Anang", "Dadi"))

# Variabel untuk query
var_query = var()

# Query Ayah dari Badu
hasil_ayah = run(1, var_query, orang_tua(var_query, "Badu"))
print("Ayah dari Badu :", hasil_ayah[0])

# --- TAMBAHKAN RELASI BARU ---

# 1. Relasi Paman
def paman(relasi_orang_tua, anak, calon_paman):
    """
    calon_paman adalah paman dari anak jika:
    - ada seorang kakek/nenek yang merupakan ayah dari ayah(anak) dan juga ayah dari calon_paman
    """
    ayah = var()
    kakek = var()
    return lall(relasi_orang_tua(kakek, ayah),   # kakek adalah ayah dari ayah
                relasi_orang_tua(ayah, anak),          # ayah adalah ayah dari anak
                relasi_orang_tua(kakek, calon_paman))  # kakek juga ayah dari calon_paman

# Query Paman dari Badu
hasil_paman_semua = run(None, var_query, paman(orang_tua, "Badu", var_query))
ayah_baddu = run(1, var_query, orang_tua(var_query, "Badu"))[0]
hasil_paman = [p for p in hasil_paman_semua if p != ayah_baddu]
if hasil_paman:
    print("Paman dari Badu :", hasil_paman[0])
else:
    print("Paman dari Badu : Tidak ditemukan")

# 2. Relasi Kakek
def kakek(relasi_orang_tua, anak, calon_kakek):
    """
    calon_kakek adalah kakek dari anak jika:
    - ada seorang ayah yang merupakan ayah dari anak
    - dan calon_kakek adalah ayah dari ayah tersebut
    """
    ayah = var()
    return lall(relasi_orang_tua(calon_kakek, ayah), relasi_orang_tua(ayah, anak))

# Query Kakek dari Badu
hasil_kakek = run(1, var_query, kakek(orang_tua, "Badu", var_query))
if hasil_kakek:
    print("Kakek dari Badu :", hasil_kakek[0])
else:
    print("Kakek dari Badu : Tidak ditemukan")

# 3. Relasi Saudara
def saudara(relasi_orang_tua, orang1, orang2):
    """
    orang2 adalah saudara dari orang1 jika:
    - ada orang tua yang sama untuk keduanya
    """
    orang_tua_common = var()
    return lall(relasi_orang_tua(orang_tua_common, orang1), relasi_orang_tua(orang_tua_common, orang2))

# Query Saudara dari Badu
hasil_saudara_semua = run(None, var_query, saudara(orang_tua, "Badu", var_query))
hasil_saudara = [s for s in hasil_saudara_semua if s != "Badu"]
if hasil_saudara:
    print("Saudara dari Badu :", ", ".join(hasil_saudara))
else:
    print("Saudara dari Badu : Tidak ditemukan")
