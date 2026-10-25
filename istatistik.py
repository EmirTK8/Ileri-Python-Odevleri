from functools import partial, reduce
from typing import Any


def istatistikler_map_filter_reduce(
    galaksi: dict[str, Any],
) -> tuple[list[str], list[str], int]:
    """Üç galaksi istatistiğini map, filter ve reduce kullanarak hesaplar."""
    gezegenler = galaksi["gezegenler"]
    baglantilar = galaksi["baglantilar"]

    buyuk_harfli = list(map(str.upper, gezegenler))
    en_az_iki_baglantili = list(
        map(
            lambda kayit: kayit[0],
            filter(lambda kayit: len(kayit[1]) >= 2, baglantilar.items()),
        )
    )
    toplam_baglanti = reduce(
        lambda toplam, hedefler: toplam + len(hedefler),
        baglantilar.values(),
        0,
    )
    return buyuk_harfli, en_az_iki_baglantili, toplam_baglanti


def istatistikler(
    galaksi: dict[str, Any],
) -> tuple[list[str], list[str], int]:
    """Üç galaksi istatistiğini liste üreticisi ve sum kullanarak hesaplar."""
    gezegenler = galaksi["gezegenler"]
    baglantilar = galaksi["baglantilar"]

    # Bu kısa dönüşümlerde liste üreticisi ve sum daha okunaklıdır.
    buyuk_harfli = [gezegen.upper() for gezegen in gezegenler]
    en_az_iki_baglantili = [
        gezegen for gezegen, hedefler in baglantilar.items()
        if len(hedefler) >= 2
    ]
    toplam_baglanti = sum(len(hedefler) for hedefler in baglantilar.values())
    return buyuk_harfli, en_az_iki_baglantili, toplam_baglanti


def yolculuk(mesafe: float, hiz: float) -> float:
    """Verilen mesafenin belirtilen hızla kaç zaman biriminde alınacağını döndürür."""
    if hiz <= 0:
        raise ValueError("Hız pozitif olmalıdır.")
    return mesafe / hiz


hizli_yolculuk = partial(yolculuk, hiz=3)
