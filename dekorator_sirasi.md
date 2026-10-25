# İleri Python Programlama — Hafta 5: Dekoratör Sırası ve Çağrı Sayacı Analizi

**Öğrenci:** Emir Talha Karaman  
**Öğrenci No:** 20253006003  
**Ders:** İleri Python Programlama  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
**Dönem:** 2026–2027 Güz  

---

## 1. Giriş ve Dekoratörlerin Uygulanma Mekanizması

Python'da birden fazla dekoratör alt alta yazıldığında, fonksiyon tanımı **aşağıdan yukarıya (içten dışa)** doğru sarmalanır:

```python
@dekorator1
@dekorator2
def f():
    pass
```

Bu sözdizimi Python çalışma zamanında tam olarak şu anlama gelir:
$$\text{f} = \text{dekorator1}(\text{dekorator2}(\text{f}))$$

Dolayısıyla fonksiyon çağrıldığında, yürütme sırası **dıştan içe** doğru gerçekleşir:
1. İlk olarak en dıştaki `dekorator1` devreye girer.
2. `dekorator1` içindeki sarmalayıcı devam ederse bir alt katmandaki `dekorator2` çalışır.
3. Son olarak orijinal `f` fonksiyonu yürütülür.

Aşağıda, özyinelemeli (recursive) Fibonacci fonksiyonu üzerinde `@say` ve `@lru_cache` dekoratörlerinin üç farklı diziliminin `fib(20)` için ürettiği çağrı sayıları ve bu sayıların teknik nedenleri incelenmiştir.

---

## 2. Üç Farklı Durumun Karşılaştırmalı Sonuçları

| Durum | Dekoratör Dizilimi | Çağrı Sayacı (`fib(20)`) | Sayaca Erişim Biçimi |
|:---|:---|:---:|:---|
| **Durum 1** | Yalnızca `@say` | **21891** | `fib.cagri` |
| **Durum 2** | `@say` üstte, `@lru_cache` altta | **39** | `fib.cagri` |
| **Durum 3** | `@lru_cache` üstte, `@say` altta | **21** | `fib.__wrapped__.cagri` |

---

## 3. Durumların Detaylı Açıklamaları

### Durum 1: Yalnızca `@say` (21.891 Çağrı)

```python
@say
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

* **Neden 21891?**  
  Burada herhangi bir önbellekleme (memoization) katmanı bulunmamaktadır. Klasik özyinelemeli Fibonacci fonksiyonu ikili bir karar ağacı (binary tree) oluşturur. `n=20` için aynı alt problemler (`fib(3)`, `fib(4)` vb.) defalarca baştan hesaplanır. Matematiksel olarak $n \ge 1$ için özyinelemeli çağrı sayısı formülü:
  $$\text{Toplam Çağrı} = 2 \times F_{n+1} - 1 = 2 \times F_{21} - 1 = 2 \times 10946 - 1 = 21891$$
  Tüm bu 21.891 çağrının her biri doğrudan `@say` sarmalayıcısından geçer ve her seferinde sayaç 1 artar.

---

### Durum 2: `@say` Üstte, `@lru_cache` Altta (39 Çağrı)

```python
@say
@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

* **Sarmalama Yapısı:**  
  $$\text{fib} = \text{say}(\text{lru\_cache}(\text{fib}))$$
* **Neden 39?**  
  En dıştaki katman `say` fonksiyonudur. `fib` fonksiyonu özyinelemeli olarak kendisini her çağırdığında (örneğin `return fib(n-1) + fib(n-2)` satırında), en dıştaki `say` sarmalayıcısına gelir. Bu nedenle yapılan **her bir çağrı isteği**, önbellekte zaten mevcut olsa bile, önce `say` sarmalayıcısı tarafından karşılanır ve sayaç artırılır.  
  Ardından istek alttaki `@lru_cache` katmanına iletilir. Eğer değer önbellekte varsa `lru_cache` hemen cevabı döner, yoksa orijinal fonksiyonu çalıştırır.  
  `fib(20)` hesaplanırken:
  - 0'dan 20'ye kadar olan 21 değer ilk kez aranırken 21 çağrı,
  - Sol koldan hesaplanan değerler sağ koldaki ikincil dallanmalarda önbellekten çekilirken 18 çağrı yapılır.
  - Toplamda $21 + 18 = 39$ çağrı `say` sarmalayıcısına ulaşmış olur.

---

### Durum 3: `@lru_cache` Üstte, `@say` Altta (21 Çağrı)

```python
@functools.lru_cache(maxsize=None)
@say
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

* **Sarmalama Yapısı:**  
  $$\text{fib} = \text{lru\_cache}(\text{say}(\text{fib}))$$
* **Neden 21?**  
  Bu senaryoda en dıştaki katman `@lru_cache`'tir. Bir parametre (örneğin `n=18`) daha önce hesaplanıp önbelleğe alındıysa, `@lru_cache` isteği hemen yakalar ve altındaki `@say` katmanına **hiç iletmeden** önbellekten döner (Cache Hit).  
  Dolayısıyla `@say` sarmalayıcısına yalnızca ve yalnızca **önbellekte henüz bulunmayan (Cache Miss)** çağrılar ulaşır. $n=0, 1, 2, \dots, 20$ olmak üzere 21 farklı tamsayı değeri ilk kez hesaplanırken `@say` tam 21 kez tetiklenir.
* **`__wrapped__` Nitelik Erişimi:**  
  En dışta `@lru_cache` bulunduğu için doğrudan `fib.cagri` niteliği arandığında bulunamaz; çünkü `cagri` niteliği içteki `say` sarmalayıcısına aittir. `functools.wraps` sayesinde iç katmandaki nesneye `fib.__wrapped__` üzerinden erişilir ve sayacın güncel değeri `fib.__wrapped__.cagri` ile 21 olarak okunur.

---

## 4. Sonuç ve Mimari Çıkarım

Dekoratörlerin diziliş sırası fonksiyonun davranışını ve performans ölçümlerini doğrudan belirler:
* Bir fonksiyonun **gerçek çalışma / hesaplama maliyetini** ölçmek istiyorsak, sayaç veya süre ölçücü dekoratör `@lru_cache`'in **altında** olmalıdır (Durum 3).
* Fonksiyona gelen **toplam istek trafiğini** ölçmek istiyorsak, sayaç dekoratörü `@lru_cache`'in **üstünde** olmalıdır (Durum 2).
