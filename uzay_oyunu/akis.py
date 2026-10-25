# Ad Soyad: Emir Talha Karaman
# Öğrenci Numarası: 20253006003
# Tarih: 18.10.2026
#
# Hafta 4 Lab Ödevi




from collections.abc import Iterator


def fibonacci() -> Iterator[int]:
    """Fibonacci dizisinin sayılarını sonsuz olarak üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki


def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her adımda yakıtı belirtilen miktarda azaltarak kalan yakıtı üretir."""
    if yakit < 0:
        raise ValueError("Yakıt negatif olamaz.")
    if tuketim <= 0:
        raise ValueError("Tüketim pozitif olmalıdır.")

    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit


def satirlari_oku(yol: str) -> Iterator[str]:
    """Dosyadaki boş ve yorum satırları dışındaki satırları üretir."""
    with open(yol, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                yield satir


def ayristir(satirlar: Iterator[str]) -> Iterator[tuple[str, str, int]]:
    """Seyir defteri satırlarını kaynak, hedef ve yakıt bilgilerine ayırır."""
    for satir in satirlar:
        kaynak_hedef, yakit_metni = satir.rsplit(maxsplit=1)
        kaynak, hedef = kaynak_hedef.split(" -> ")
        yield kaynak, hedef, int(yakit_metni)


def uzun_yolculuklar(
    kayitlar: Iterator[tuple[str, str, int]],
    esik: int,
) -> Iterator[str]:
    """Yakıt tüketimi eşikten büyük olan yolculukların hedeflerini üretir."""
    for kaynak, hedef, yakit in kayitlar:
        if yakit > esik:
            yield hedef