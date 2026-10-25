# Ad Soyad: Emir Talha Karaman
# Öğrenci Numarası: 20253006003
# Tarih: 25.10.2026
#
# Hafta 5 Lab Ödevi — Dekoratörler Modülü
# Bu modül uzay oyunu ve fonksiyonel işlemler için genel amaçlı dekoratörleri içerir.

import functools
import time
from typing import Any, Callable


def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun çalışma süresini time.perf_counter() ile ölçen dekoratör.

    Çalışma süresini 'ad: 0.0123 sn' biçiminde ekrana yazdırır ve fonksiyonun
    orijinal sonucunu aynen döndürür. functools.wraps ile metaverileri korur.

    Args:
        fonksiyon: Süresi ölçülecek hedef fonksiyon.

    Returns:
        Callable: Süre ölçümü yapan sarmalayıcı fonksiyon.
    """
    @functools.wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        bitis = time.perf_counter()
        gecen_sure = bitis - baslangic
        print(f"{fonksiyon.__name__}: {gecen_sure:.4f} sn")
        return sonuc

    return sarmalayici
