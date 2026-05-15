
# Senaryo Adı: Yazılım Geliştirici Destek Botu (S28)

## Kullanım Hikayesi
Junior bir yazılımcı, kod yazarken aldığı hata mesajını veya sorununu `bot.py`'a yazar. Bot, bildiği hatalarda otomatik çözüm sunar; riskli veya belirsiz durumlarda ise mesajı kıdemli yazılımcıya (`operator.py`) iletir.

## Hedef Kullanıcı
- Yazılım öğrenmeye yeni başlamış öğrenciler veya junior geliştiriciler.
- Kıdemli yazılımcı/operatör, kritik veya belirsiz durumlarda destek verir.

## Mod Mantığı (En Önemli Kısım)
### HOOTL (İnsansız Mod)
- `bilgi.txt` dosyasındaki hata-çözüm çiftlerini okur.
- Kullanıcı girdisi ile her hata anahtarı arasındaki Levenshtein mesafesini hesaplar.
- En iyi eşleşme mesafesi **<= 3** ise, çözümü ekrana yazar.
- En iyi eşleşme **> 3** ise: `Hata bulunamadi.` yazar.

### HITL (Tamamen İnsanlı Mod)
- `bilgi.txt`'yi hiç kullanmaz.
- Kullanıcı mesajını `kuyruk.txt`'ye `BOT:<mesaj>` olarak yazar.
- Operatör, `OPERATOR:<cevap>` satırı ekleyene kadar bekler.
- Sadece operatörün cevabını ekrana yazar.

### HOTL (Yarı İnsanlı Mod) — Yönlendirme Sebepleri
HOTL, sadece güvenli ve emin olduğu durumlarda otomatik cevap verir. Aksi halde operatöre yönlendirir.

**Tehlikeli Anahtar Kelimeler (Anında Yönlendirme)**
| Anahtar Kelime | Neden "Tehlikeli"? |
|---|---|
| database / db | Veritabanı üzerinde işlem yapmak yüksek risklidir; bot hatası veri kaybına yol açabilir. |
| production / prod | Canlı ortamda hata, insan gözüyle kontrol edilmelidir. |
| deleted / drop | Veri kaybı anlamına gelir, acil uzman müdahalesi gerekir. |
| crash | Sistem tamamen çökmüşse, basit bir bot çözümü yeterli olmayabilir. |
| security / auth | Güvenlik ihlali veya giriş sorunları çok hassastır, bot çözmemelidir. |
| payment / money | Finansal işlemler yüksek sorumluluk gerektirir, insan kontrolü şarttır. |
| deployment | Dağıtım hattı bozuksa, kod canlıya çıkmadan insan onayı gerekir. |

**Yüksek Belirsizlik Yönlendirmesi**
- En iyi Levenshtein mesafesi **> 4** ise, bot emin olmadığını belirtir ve operatöre yönlendirir.

**Eşleşme Bulunamazsa Yönlendirme**
- Bot, hiç benzer hata bulamazsa (anahtar kelime yoksa/geçersizse), "bulunamadi" demek yerine operatöre iletir.

## Test Örnekleri (5 Girdi)
Bu örnekler, davranışı gösterir (`operator.py` ikinci terminalde çalışmalı):

1) Girdi: `SyntaxError` (HOTL)
- Beklenen: `bilgi.txt`'den otomatik cevap (yakın eşleşme).

2) Girdi: `SyntaXEror` (HOOTL)
- Beklenen: Mesafe <= 3 ise otomatik cevap (tipoya toleranslı).

3) Girdi: `there is a problem with the dataset` (HOTL)
- Beklenen: Mesafe > 4 / eşleşme yoksa operatöre yönlendirme.

4) Girdi: `database migration failed` (HOTL)
- Beklenen: "database" tehlikeli kelime olduğu için anında operatöre yönlendirme.

5) Girdi: `payment refunded twice` (HOTL)
- Beklenen: "payment" tehlikeli kelime olduğu için anında operatöre yönlendirme.

## Gerekli Dosyalar
- `SPEC.md` — Bu belge.
- `bilgi.txt` — Yazılım hataları için en az 12 satırlık "anahtar: çözüm".
- `bot.py` — Tüm modları (`hootl`, `hitl`, `hotl`) terminal argümanıyla çalıştıran tek dosya.
- `operator.py` — `kuyruk.txt`'yi izleyen ve `OPERATOR:` yanıtı yazan ayrı script.
