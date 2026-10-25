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


# --- Görev 2: say ve Dekoratör Sırası Testleri ---

def test_say_yalnizca_say() -> None:
    """Yalnızca @say ile süslenen özyinelemeli fib(20) için 21891 çağrı yapıldığını doğrular."""
    from uzay_oyunu.dekoratorler import say

    @say
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    assert fib(20) == 6765
    assert fib.cagri == 21891


def test_say_ustte_lru_cache_altta() -> None:
    """@say üstte, @lru_cache altta iken fib(20) için 39 çağrı yapıldığını doğrular."""
    import functools
    from uzay_oyunu.dekoratorler import say

    @say
    @functools.lru_cache(maxsize=None)
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    assert fib(20) == 6765
    assert fib.cagri == 39


def test_lru_cache_ustte_say_altta() -> None:
    """@lru_cache üstte, @say altta iken fib(20) için 21 çağrı yapıldığını doğrular."""
    import functools
    from uzay_oyunu.dekoratorler import say

    @functools.lru_cache(maxsize=None)
    @say
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    assert fib(20) == 6765
    # @lru_cache en dışta olduğu için içteki sayacın niteliğine __wrapped__ ile ulaşılır
    assert fib.__wrapped__.cagri == 21


# --- Görev 3: log_cagri Testleri ---

def test_log_cagri_ciktisi(capsys: pytest.CaptureFixture[str]) -> None:
    """log_cagri dekoratörünün PDF'teki örnek gibi hem çağrıyı hem sonucu logladığını doğrular."""
    from uzay_oyunu.dekoratorler import log_cagri

    @log_cagri
    def yolculuk(hedef: str, hiz: int = 1) -> str:
        return f"{hedef} hiz={hiz}"

    sonuc = yolculuk("orion", hiz=3)
    assert sonuc == "orion hiz=3"

    cikis = capsys.readouterr().out
    assert "-> yolculuk('orion', hiz=3)" in cikis
    assert "<- yolculuk = 'orion hiz=3'" in cikis


def test_log_cagri_hedef_menusu_ve_galaksi_kur(capsys: pytest.CaptureFixture[str]) -> None:
    """hedef_menusu ve galaksi_kur fonksiyonlarının loglanarak sorunsuz çalıştığını doğrular."""
    from uzay_oyunu.oyun import hedef_menusu
    from uzay_oyunu.galaksi import galaksi_kur

    # hedef_menusu çağrısı
    menu = hedef_menusu(["centauri", "sirius"])
    assert "[1] centauri" in menu

    # galaksi_kur çağrısı
    g = galaksi_kur(["dünya", "mars"], {"dünya": ["mars"]}, "dünya", yakit=80)
    assert g["konum"] == "dünya"

    cikis = capsys.readouterr().out
    assert "-> hedef_menusu(['centauri', 'sirius'])" in cikis
    assert "<- hedef_menusu =" in cikis
    assert "-> galaksi_kur(['dünya', 'mars'], {'dünya': ['mars']}, 'dünya', yakit=80)" in cikis
    assert "<- galaksi_kur =" in cikis


# --- Görev 4: Komut Sistemi Testleri ---

def test_komut_kayit_ve_mukerrer_hata() -> None:
    """@komut dekoratörünün fonksiyonu değiştirmeden kaydettiğini ve mükerrer ada hata verdiğini doğrular."""
    from uzay_oyunu.komutlar import komut, KOMUTLAR

    @komut("test_komutu", "örnek bir test komutu")
    def ozel_islem(durum: dict) -> str:
        return "tamam"

    assert ozel_islem({"konum": "dünya"}) == "tamam"
    assert "test_komutu" in KOMUTLAR
    assert KOMUTLAR["test_komutu"][1] == "örnek bir test komutu"

    # Aynı adla tekrar kayıt denenirse ValueError fırlatmalıdır
    with pytest.raises(ValueError) as excinfo:
        @komut("test_komutu", "ikinci kayıt")
        def mukerrer(durum: dict) -> str:
            return "hata"

    assert "zaten kayıtlı" in str(excinfo.value)


def test_komut_yardim() -> None:
    """yardim komutunun kayıtlı komutları ve açıklamalarını listelediğini doğrular."""
    from uzay_oyunu.komutlar import yardim

    cikti = yardim({})
    assert "yardim" in cikti
    assert "envanter" in cikti
    assert "harita" in cikti
    assert "komutları listeler" in cikti


def test_komut_envanter() -> None:
    """envanter komutunun durum sözlüğündeki eşyaları listelediğini doğrular."""
    from uzay_oyunu.komutlar import envanter

    durum = {"credits": True, "engines": False, "copilot": True}
    cikti = envanter(durum)
    assert "bol kredi" in cikti
    assert "yetenekli bir pilot" in cikti


def test_komut_harita() -> None:
    """harita komutunun bulunulan konumdan gidilebilecek yerleri virgülle listelediğini doğrular."""
    from uzay_oyunu.komutlar import harita

    durum = {
        "konum": "dünya",
        "baglantilar": {"dünya": ["centauri", "sirius"]}
    }
    cikti = harita(durum)
    assert cikti == "centauri, sirius"


def test_travel_komut_entegrasyonu(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """travel() içinde komut girildiğinde komutun çalışıp menünün tekrar gösterildiğini doğrular."""
    from uzay_oyunu.oyun import travel

    # Önce 'harita' komutunu çalıştır, ardından 'q' ile çık
    girdiler = iter(["harita", "q"])
    monkeypatch.setattr("builtins.input", lambda _istem: next(girdiler))

    travel()

    cikis = capsys.readouterr().out
    assert "centauri, sirius" in cikis
    assert "Oyunu 0 hamlede bitirdin!" in cikis
