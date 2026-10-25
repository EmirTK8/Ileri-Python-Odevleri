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


def say(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Çağrı sayısını fonksiyonun bir niteliğinde (.cagri) sayan dekoratör.

    Her çağrıda sarmalayici.cagri değerini bir artırır ve fonksiyonu çalıştırır.
    functools.wraps ile sarmalanır.

    Args:
        fonksiyon: Çağrıları sayılacak hedef fonksiyon.

    Returns:
        Callable: cagri niteliğine sahip sarmalayıcı fonksiyon.
    """
    @functools.wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)

    sarmalayici.cagri = 0
    return sarmalayici


def log_cagri(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Her çağrıdan önce fonksiyon adını ve argümanlarını, sonra da dönüş değerini yazdıran dekoratör.

    Çağrı formatı:
    -> fonksiyon_adi(arg1, arg2, kw1=deger1)
    <- fonksiyon_adi = donus_degeri

    Args:
        fonksiyon: Loglanacak hedef fonksiyon.

    Returns:
        Callable: Loglama yapan sarmalayıcı fonksiyon.
    """
    @functools.wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        arg_parcalari = [repr(arg) for arg in args]
        arg_parcalari.extend(f"{anahtar}={deger!r}" for anahtar, deger in kwargs.items())
        print(f"-> {fonksiyon.__name__}({', '.join(arg_parcalari)})")

        sonuc = fonksiyon(*args, **kwargs)

        print(f"<- {fonksiyon.__name__} = {sonuc!r}")
        return sonuc

    return sarmalayici


def sinirla(alt: int | float, ust: int | float) -> Callable[[Callable], Callable]:
    """Dekore edilen fonksiyonun ilk argümanının [alt, ust] aralığında olduğunu denetleyen dekoratör.

    İlk argüman aralık dışındaysa anlamlı bir ValueError fırlatır:
    '{fonksiyon.__name__}: {deger} değeri {alt}-{ust} aralığında değil'

    Args:
        alt: İzin verilen en küçük değer (dahil).
        ust: İzin verilen en büyük değer (dahil).

    Returns:
        Callable: Aralığı denetleyen dekoratör.
    """
    def dekorator(fonksiyon: Callable) -> Callable:
        @functools.wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            if not args:
                raise ValueError(f"{fonksiyon.__name__}: En az bir konumsal argüman bekleniyor.")
            ilk_arg = args[0]
            if not (alt <= ilk_arg <= ust):
                raise ValueError(
                    f"{fonksiyon.__name__}: {ilk_arg} değeri {alt}-{ust} aralığında değil"
                )
            return fonksiyon(*args, **kwargs)

        return sarmalayici

    return dekorator


@sinirla(0, 100)
def yakit_harca(miktar: int) -> int:
    """Belirtilen miktar kadar yakıt harcar ve kalan yakıtı döndürür."""
    return 100 - miktar


def hafiza(maxsize: int | None = None) -> Callable[[Callable], Callable]:
    """Bonus (+10): functools.lru_cache kullanmadan çalışan closure tabanlı önbellek dekoratörü.

    Closure içindeki bir sözlükle çalışır. maxsize verildiğinde önbellek dolunca
    en eski girdiyi silerek LRU/FIFO mantığını uygular.

    Args:
        maxsize: Önbellekte tutulacak en fazla eleman sayısı (None ise sınırsız).

    Returns:
        Callable: Önbellekleme yapan dekoratör.
    """
    def dekorator(fonksiyon: Callable) -> Callable:
        onbellek: dict[Any, Any] = {}

        @functools.wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            anahtar = (args, tuple(sorted(kwargs.items())))
            if anahtar in onbellek:
                deger = onbellek.pop(anahtar)
                onbellek[anahtar] = deger
                return deger

            sonuc = fonksiyon(*args, **kwargs)

            if maxsize is not None and maxsize > 0:
                while len(onbellek) >= maxsize:
                    en_eski = next(iter(onbellek))
                    del onbellek[en_eski]

            onbellek[anahtar] = sonuc
            return sonuc

        sarmalayici.onbellek = onbellek
        return sarmalayici

    return dekorator
