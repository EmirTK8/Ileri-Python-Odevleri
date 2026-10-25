# Ad Soyad: Emir Talha Karaman
# Öğrenci Numarası: 20253006003
# Tarih: 18.10.2026
#
# Hafta 4 Lab Ödevi




from itertools import islice, takewhile

import pytest

from istatistik import (
    hizli_yolculuk,
    istatistikler,
    istatistikler_map_filter_reduce,
    yolculuk,
)
from uzay_oyunu.galaksi import veri_yukle
from uzay_oyunu.akis import (
    fibonacci,
    yakit_gostergesi,
    satirlari_oku,
    ayristir,
    uzun_yolculuklar,
)
from uzay_oyunu.oyun import travel
from uzay_oyunu.rotalar import rota_sayaci, rota_sayisi_onbelleksiz

def test_fibonacci_next() -> None:
    """Fibonacci üretecinin ilk üç değerini kontrol eder."""
    g = fibonacci()

    assert next(g) == 0
    assert next(g) == 1
    assert next(g) == 1


def test_fibonacci_islice() -> None:
    """İlk 12 Fibonacci sayısını kontrol eder."""
    sonuc = list(islice(fibonacci(), 12))

    assert sonuc == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def test_fibonacci_takewhile() -> None:
    """100'den küçük Fibonacci sayılarını kontrol eder."""
    sonuc = list(takewhile(lambda x: x < 100, fibonacci()))

    assert sonuc == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def test_fibonacci_generator_is_consumed() -> None:
    """Aynı üretecin ikinci kullanımda kaldığı yerden devam ettiğini kontrol eder."""
    g = fibonacci()

    ilk = list(islice(g, 3))
    ikinci = list(islice(g, 3))

    assert ilk == [0, 1, 1]
    assert ikinci == [2, 3, 5]


def test_yakit_gostergesi() -> None:
    """Yakıtın her adımda doğru miktarda azaldığını kontrol eder."""
    sonuc = list(yakit_gostergesi(100, 30))

    assert sonuc == [70, 40, 10, 0]


def test_yakit_gostergesi_biter() -> None:
    """Yakıt bitince üretecin durduğunu kontrol eder."""
    g = yakit_gostergesi(30, 10)

    assert list(g) == [20, 10, 0]

    with pytest.raises(StopIteration):
        next(g)


def test_yakit_gostergesi_gecersiz_tuketim() -> None:
    """Sıfır veya negatif tüketimin sonsuz üreteç oluşturmasını engeller."""
    with pytest.raises(ValueError):
        list(yakit_gostergesi(100, 0))


def test_travel_yakit_bitince_mesaj_verir(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Yakıt bittiğinde oyunun kayıp mesajıyla durduğunu kontrol eder."""
    secimler = iter(["1"] * 21)
    monkeypatch.setattr("builtins.input", lambda _istem: next(secimler))

    travel()

    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in capsys.readouterr().out

def test_satirlari_oku() -> None:
    """Dosyadaki boş ve yorum satırlarının atlandığını kontrol eder."""
    satirlar = list(satirlari_oku("veri/seyir.txt"))

    assert len(satirlar) == 6
    assert all(not satir.startswith("#") for satir in satirlar)


def test_ayristir() -> None:
    """Seyir kayıtlarının doğru ayrıştırıldığını kontrol eder."""
    kayitlar = list(ayristir(satirlari_oku("veri/seyir.txt")))

    assert kayitlar[0] == ("dünya", "sirius", 12)
    assert kayitlar[-1] == ("sirius", "kara_delik", 30)
    assert sum(yakit for _, _, yakit in kayitlar) == 88


def test_uzun_yolculuklar() -> None:
    """Eşikten büyük yakıt tüketimli yolculukların hedeflerini kontrol eder."""
    hedefler = list(
        uzun_yolculuklar(
            ayristir(satirlari_oku("veri/seyir.txt")),
            10,
        )
    )

    assert hedefler == ["sirius", "centauri", "orion", "kara_delik"]


def test_rota_sayaci_onbellekli_ve_onbelleksiz() -> None:
    """Önbellekli ve önbelleksiz sayaçların aynı rotaları bulduğunu doğrular."""
    baglantilar = veri_yukle()["baglantilar"]
    say = rota_sayaci(baglantilar)

    assert say("dünya", 3) == 16
    assert say("dünya", 10) == rota_sayisi_onbelleksiz(baglantilar, "dünya", 10)
    assert say.cache_info().hits > 0


def test_rota_sayaci_gecersiz_adim() -> None:
    """Negatif adım sayısının açıkça reddedildiğini doğrular."""
    say = rota_sayaci({"dünya": ["sirius"]})

    with pytest.raises(ValueError):
        say("dünya", -1)


def test_istatistikler_iki_yontemle_aynidir() -> None:
    """Map/filter/reduce ve liste üreticisi/sum sonuçlarını karşılaştırır."""
    galaksi = veri_yukle()
    beklenen = (
        ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"],
        ["dünya", "centauri", "sirius", "orion"],
        12,
    )

    assert istatistikler_map_filter_reduce(galaksi) == beklenen
    assert istatistikler(galaksi) == beklenen


def test_hizli_yolculuk_partial() -> None:
    """Kısmi fonksiyonun hızı üçe sabitlediğini kontrol eder."""
    assert hizli_yolculuk(12) == 4

    with pytest.raises(ValueError):
        yolculuk(12, 0)