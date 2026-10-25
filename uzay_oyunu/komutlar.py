# Ad Soyad: Emir Talha Karaman
# Öğrenci Numarası: 20253006003
# Tarih: 25.10.2026
#
# Hafta 5 Lab Ödevi — Komut Sistemi (Kayıt Deseni)
# Bu modül komut dekoratörünü ve oyun içi komut fonksiyonlarını içerir.

from typing import Any, Callable

# Kayıtlı komutları (fonksiyon, aciklama) biçiminde tutan sözlük
KOMUTLAR: dict[str, tuple[Callable[[dict[str, Any]], str], str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[Callable], Callable]:
    """Komutları KOMUTLAR sözlüğüne kaydeden dekoratör.

    Dekore edilen fonksiyonu değiştirmeden (fonksiyon, aciklama) olarak sözlüğe
    ekler. Aynı ad iki kez kaydedilmeye çalışılırsa ValueError fırlatır.

    Args:
        ad: Komut adı (çağrı anahtarı).
        aciklama: Komutun işlevini belirten açıklama metni.

    Returns:
        Callable: Orijinal fonksiyonu aynen döndüren dekoratör.

    Raises:
        ValueError: Komut adı zaten kayıtlıysa.
    """
    def kayit_dekoratoru(fonksiyon: Callable) -> Callable:
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' adlı komut zaten kayıtlı!")
        KOMUTLAR[ad] = (fonksiyon, aciklama)
        return fonksiyon

    return kayit_dekoratoru


@komut("yardim", "komutları listeler")
def yardim(durum: dict[str, Any]) -> str:
    """Kayıtlı komutları ve açıklamalarını alfabetik sırayla listeler."""
    satirlar: list[str] = []
    for komut_adi, (_, aciklama) in sorted(KOMUTLAR.items()):
        satirlar.append(f"{komut_adi:<10} {aciklama}".rstrip())
    return "\n".join(satirlar)


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: dict[str, Any]) -> str:
    """Oyuncunun sahip olduğu eşyaları envanter_metni ile listeler."""
    from uzay_oyunu.oyun import envanter_metni

    credits = durum.get("credits", False)
    engines = durum.get("engines", False)
    copilot = durum.get("copilot", False)
    metin = envanter_metni(credits, engines, copilot)
    return metin if metin else "Envanterinde hiç eşya yok."


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: dict[str, Any]) -> str:
    """Mevcut gezegenden doğrudan gidilebilecek bağlantılı gezegenleri listeler."""
    konum = durum.get("konum", "")
    baglantilar = durum.get("baglantilar", {})
    hedefler = baglantilar.get(konum, [])
    return ", ".join(hedefler)
