# İleri Python Programlama — Laboratuvar Ödevleri

**Öğrenci:** Emir Talha Karaman  
**Öğrenci No:** 20253006003  
**Ders:** İleri Python Programlama  
**Kurum:** İstanbul Nişantaşı Üniversitesi  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
**Dönem:** 2026–2027 Güz  
**GitHub Deposu:** https://github.com/EmirTK8/Ileri-Python-Odevleri  

---

## 🌿 Proje ve Branch (Dal) Yapısı

Bu depo, dönem boyunca geliştirilen **Uzay Oyunu** projesini ve haftalık laboratuvar çalışmalarını içermektedir. Proje, her haftanın bir önceki haftanın son commit'inden devam ettiği zincirleme bir branch mimarisine sahiptir:

* **`main`**: En güncel durum ve tüm haftaların birleştirilmiş ana çalışma alanı.
* **`hafta3`**: 3. Hafta Lab Ödevi (Saf fonksiyonlar, galaksi JSON verisi, esnek parametreler, kapsam ve closure).
* **`hafta4`**: 4. Hafta Lab Ödevi (Üreteçler, seyir boru hattı, rota önbelleği ve functools).
* *(Sonraki haftalar da önceki haftanın dalından türetilerek bu yapıyla devam edecektir.)*

---

## 🚀 Hafta 3 — Fonksiyonlar Derinlemesine

Uzay oyununun monolitik `travel()` fonksiyonu küçük, test edilebilir saf fonksiyonlara bölünmüş ve harita harici bir JSON dosyasına taşınmıştır:

1. **Saf Fonksiyonlar:** `envanter_metni` ve `hedef_menusu` fonksiyonları ekrana baskı yapmadan formatlanmış metin döndürecek şekilde yazıldı.
2. **Esnek Parametreler:** `gorev_kaydi` fonksiyonu ile `*args`, `**kwargs` açma mekanizması ve keyword-only `oncelik` parametresi uygulandı.
3. **Veri Odaklı Harita:** `uzay_oyunu/galaksi.json` oluşturuldu; `galaksi_kur` fonksiyonu ile başlangıç gezegeni ve varsayılan yakıt ayarları yönetildi.
4. **Tuzaklar ve Kapsam:** Varsayılan argümanlardaki değiştirilebilir liste (`depo=[]`) tuzağı `None` kalıbıyla giderildi. LEGB kuralı ve `UnboundLocalError` mekanizması `kapsam.md` dosyasında detaylandırıldı.
5. **Closure ve Lambda:** `nonlocal` ile durum tutan `hamle_sayaci`, `lambda` ile çok kriterli `en_bagli_gezegenler` sıralaması ve çalışma süresi ölçen `@sure_olc` dekoratörü eklendi.

---

## ⚡ Hafta 4 — Üreteçler ve functools

Uzay macerasına üreteçler (generators), tembel veri işleme boru hattı ve `@lru_cache` destekli önbellekli rota hesaplama araçları entegre edildi:

1. **Fibonacci Üreteci:** `fibonacci()` sonsuz üreteci yazıldı; `next()`, `itertools.islice` ve `itertools.takewhile` ile test edildi.
2. **Yakıt Göstergesi:** `yakit_gostergesi(yakit, tuketim)` üreteci ile her seyahatte yakıt tüketimi simüle edildi ve yakıt bitince oyunun sonlanması sağlandı.
3. **Seyir Defteri Boru Hattı:** `veri/seyir.txt` dosyası belleğe liste olarak yüklenmeden; `satirlari_oku`, `ayristir` ve `uzun_yolculuklar` üreteçleri üzerinden tembelce (lazy evaluation) süzüldü.
4. **Önbellekli Rota Sayacı:** `@lru_cache` kullanılarak belirli bir adımdaki rota sayısını hesaplayan `rota_sayaci` yazıldı.
5. **Fonksiyonel İstatistikler & partial:** `istatistik.py` modülünde gezegen verileri hem `map`/`filter`/`reduce` hem de liste üreteçleriyle hesaplandı; `functools.partial` ile `hizli_yolculuk` türetildi.

### Görev 4: Rota Sayacı Performans Ölçümü (`adim=20`)

Mevcut galaksi yapısında `dünya` başlangıç gezegeni için 20 adımda tamamlanan rotalar test edilmiştir:

| Yöntem | Hesaplanan Rota | Çalışma Süresi |
|:---|---:|---:|
| **Önbelleksiz** | 147.261.692 | ~65.08 saniye |
| **Önbellekli (`@lru_cache`)** | 147.261.692 | ~0.00012 saniye |

* **`cache_info()` Çıktısı:** `CacheInfo(hits=128, misses=98, maxsize=None, currsize=98)`
* **Sonuç:** Önbellek kullanımı, tekrarlanan alt rota hesaplamalarını hafızadan getirerek ~500.000 katlık bir performans artışı sağlamıştır.

---

## 🧪 Testler

Depodaki tüm testleri çalıştırmak için:

```bash
uv run pytest
# veya
python3 -m pytest
```

* Tüm haftaların toplam **31 testi** (`tests/test_fonksiyonlar.py`, `tests/test_tuzaklar.py`, `tests/test_akis.py`) başarıyla geçmektedir.
