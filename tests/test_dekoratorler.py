# Ad Soyad: Emir Talha Karaman
# Öğrenci Numarası: 20253006003
# Tarih: 25.10.2026
#
# Hafta 5 Lab Ödevi — Dekoratör Birim Testleri

import pytest
from uzay_oyunu.dekoratorler import sure_olc


# --- Görev 1: sure_olc Testleri ---

def test_sure_olc_sonuc_degismeden_donuyor(capsys: pytest.CaptureFixture[str]) -> None:
    """Dekore edilen fonksiyonun sonucunun değişmeden döndüğünü ve süreyi yazdırdığını doğrular."""
    @sure_olc
    def topla(a: int, b: int) -> int:
        """İki sayıyı toplar."""
        return a + b

    sonuc = topla(15, 25)
    assert sonuc == 40

    cikis = capsys.readouterr().out
    assert "topla:" in cikis
    assert "sn" in cikis


def test_sure_olc_adli_argumanlarla_calisiyor(capsys: pytest.CaptureFixture[str]) -> None:
    """Adlı (keyword) argümanlarla yapılan çağrıların başarıyla çalıştığını doğrular."""
    @sure_olc
    def kullanici_selamla(isim: str, unvan: str = "Gezgin") -> str:
        """Kullanıcıya unvanıyla selam verir."""
        return f"Selam {unvan} {isim}!"

    sonuc = kullanici_selamla(isim="Emir", unvan="Kaptan")
    assert sonuc == "Selam Kaptan Emir!"

    cikis = capsys.readouterr().out
    assert "kullanici_selamla:" in cikis
    assert "sn" in cikis


def test_sure_olc_name_ve_doc_korunuyor() -> None:
    """functools.wraps sayesinde __name__ ve __doc__ niteliklerinin korunduğunu doğrular."""
    @sure_olc
    def rota_hesaplayici(x: int) -> int:
        """Önemli bir rota hesabı docstring metni."""
        return x * 2

    assert rota_hesaplayici.__name__ == "rota_hesaplayici"
    assert rota_hesaplayici.__doc__ == "Önemli bir rota hesabı docstring metni."


def test_sure_olc_rota_sayacina_uygulama(capsys: pytest.CaptureFixture[str]) -> None:
    """sure_olc dekoratörünün Hafta 4'teki önbelleksiz rota sayacına uygulanabildiğini doğrular."""
    from uzay_oyunu.rotalar import rota_sayisi_onbelleksiz
    from uzay_oyunu.galaksi import veri_yukle

    galaksi = veri_yukle()
    baglantilar = galaksi["baglantilar"]

    olculen_rota_sayisi = sure_olc(rota_sayisi_onbelleksiz)
    # Hızlı ve güvenli test için adim=5 kullanıyoruz
    sonuc = olculen_rota_sayisi(baglantilar, "dünya", 5)

    assert sonuc > 0
    cikis = capsys.readouterr().out
    assert "rota_sayisi_onbelleksiz:" in cikis
    assert "sn" in cikis
