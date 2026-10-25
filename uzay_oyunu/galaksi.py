# Ad Soyad: Emir Talha Karaman
# Öğrenci Numarası: 20253006003
# Tarih: 11.10.2026
#
# Görev 3 – Galaksiyi veri dosyasından kur

import json
import os
from typing import Any
from uzay_oyunu.dekoratorler import log_cagri


@log_cagri
def galaksi_kur(
    gezegenler: list,
    baglantilar: dict,
    baslangic: str,
    **kwargs: Any
) -> dict:
    """Galaksi haritasını ve başlangıç durumunu kurar.

    Başlangıç gezegeni listede yoksa ValueError fırlatır.
    Yakıt verilmediyse varsayılan olarak 50 alır.
    """
    if baslangic not in gezegenler:
        raise ValueError(
            f"Başlangıç gezegeni '{baslangic}' gezegenler listesinde bulunamadı!"
        )

    # Yakıt verilmediyse varsayılan 50 olsun (kwargs.get)
    yakit = kwargs.get("yakit", 50)

    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "konum": baslangic,
        "yakit": yakit,
    }


def veri_yukle(dosya_adi: str = "galaksi.json") -> dict:
    """JSON veri dosyasını okuyup galaksi_kur(**veri) ile galaksiyi kurar."""
    klasor = os.path.dirname(os.path.abspath(__file__))
    tam_yol = os.path.join(klasor, dosya_adi)

    with open(tam_yol, "r", encoding="utf-8") as dosya:
        veri = json.load(dosya)

    return galaksi_kur(**veri)


# Geriye dönük uyumluluk için takma ad (alias)
galaksi_yukle = veri_yukle
