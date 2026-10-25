# İleri Python Programlama — Hafta 4 Lab Ödevi

**Ad Soyad:** Emir Talha Karaman
**Öğrenci No:** 20253006003
**Ders:** İleri Python Programlama
**Kurum:** İstanbul Nişantaşı Üniversitesi
**Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç
**Dönem:** 2026–2027 Güz
**GitHub deposu:** https://github.com/EmirTK8/20253006003_hafta3

## Proje

Hafta 3'te geliştirilen uzay oyunu bu hafta üreteçler, tembel veri işleme,
önbellekli rota hesabı ve `functools` kullanımıyla genişletildi. Önceki haftanın
saf fonksiyonları, galaksi JSON verisi, `*args`/`**kwargs`, closure, lambda ve
kapsam çalışmaları korunmuştur.

## Hafta 4 görevleri

1. `uzay_oyunu/akis.py` içinde Fibonacci ve yakıt üreteçleri.
2. Oyunda her yolculukta yakıt tüketimi ve yakıt bittiğinde kayıp mesajı.
3. `veri/seyir.txt` dosyası ve dosyayı listeye almadan işleyen üç aşamalı
   seyir defteri üreteç boru hattı.
4. `uzay_oyunu/rotalar.py` içinde önbellekli/önbelleksiz rota sayacı.
5. `istatistik.py` içinde galaksi istatistiklerinin iki yazımı ve `partial`
   ile `hizli_yolculuk`.

İstatistik çıktıları mevcut galaksi verisine göre:

```text
['DÜNYA', 'CENTAURI', 'SIRIUS', 'ORION', 'KARA_DELIK']
['dünya', 'centauri', 'sirius', 'orion']
12
```

Bağlantı toplamı, bu depodaki beş gezegenli galaksideki tüm yönlü bağlantı
listelerinin uzunlukları toplamıdır. Bu nedenle örnek metindeki 10 değeri yerine
mevcut veri için 12 elde edilir.

## Rota sayacı ölçümü

Ölçüm, `uzay_oyunu/galaksi.json` içindeki galaksi ve `dünya` başlangıç gezegeni
kullanılarak, `adim=20` için `time.perf_counter()` ile yapıldı. Önce
önbelleksiz fonksiyon, sonra yeni ve boş bir LRU önbelleği kullanan fonksiyon
çalıştırıldı. Çalışma ortamı: macOS, Python 3.14.2.

| Yöntem | Sonuç | Süre |
|---|---:|---:|
| Önbelleksiz | 147261692 | 65.082095 saniye |
| Önbellekli | 147261692 | 0.000122 saniye |

`cache_info()` çıktısı: `CacheInfo(hits=128, misses=98, maxsize=None, currsize=98)`.

Önbelleksiz hesap aynı alt rotaları defalarca yeniden hesaplarken, önbellekli
sürüm her gezegen/adım çifti için sonucu saklayıp tekrar kullanır. Süreler
çalıştırma ortamına göre değişebilir.

## Testler

Tüm eski ve yeni testleri çalıştırmak için:

```bash
uv run pytest
```

Son doğrulama: **31 test geçti**.
