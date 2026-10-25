# Ad Soyad: Emir Talha Karaman
# Öğrenci Numarası: 20253006003
# Tarih: 18.10.2026
#
# Hafta 4 Lab Ödevi




from functools import lru_cache
from collections.abc import Callable, Mapping


def rota_sayaci(
    baglantilar: Mapping[str, list[str]],
) -> Callable[[str, int], int]:
    """Verilen galaksi için önbellekli rota sayacı oluşturur."""

    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Belirli bir gezegenden tam adım sayısında yapılabilecek rotaları sayar."""
        if adim < 0:
            raise ValueError("Adım sayısı negatif olamaz.")
        if adim == 0:
            return 1

        hedefler = baglantilar.get(gezegen, [])

        return sum(
            rota_sayisi(hedef, adim - 1)
            for hedef in hedefler
        )

    return rota_sayisi

def rota_sayisi_onbelleksiz(
    baglantilar: Mapping[str, list[str]],
    gezegen: str,
    adim: int,
) -> int:
    """Verilen gezegenden tam adım uzunluğundaki rotaları önbelleksiz sayar."""
    if adim < 0:
        raise ValueError("Adım sayısı negatif olamaz.")
    if adim == 0:
        return 1

    hedefler = baglantilar.get(gezegen, [])

    return sum(
        rota_sayisi_onbelleksiz(baglantilar, hedef, adim - 1)
        for hedef in hedefler
    )

if __name__ == "__main__":
    import time
    from uzay_oyunu.galaksi import veri_yukle

    galaksi = veri_yukle()
    baglantilar = galaksi["baglantilar"]

    baslangic = time.perf_counter()
    sonuc1 = rota_sayisi_onbelleksiz(baglantilar, "dünya", 20)
    sure1 = time.perf_counter() - baslangic

    say = rota_sayaci(baglantilar)

    baslangic = time.perf_counter()
    sonuc2 = say("dünya", 20)
    sure2 = time.perf_counter() - baslangic

    print("Önbelleksiz sonuç:", sonuc1)
    print(f"Önbelleksiz süre: {sure1:.6f} saniye")
    print("Önbellekli sonuç:", sonuc2)
    print(f"Önbellekli süre: {sure2:.6f} saniye")
    print("Önbellek bilgisi:", say.cache_info())