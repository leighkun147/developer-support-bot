# Isletim sistemi islemleri icin os modulunu ice aktarir.
import os
# Komut satiri argumanlari icin sys modulunu ice aktarir.
import sys
# Zaman gecikmeleri icin time modulunu ice aktarir.
import time

# Levenshtein mesafesi hesaplayan fonksiyon baslangici.
def levenshtein_distance(a, b):
    # Turkce yorum: Iki metin arasindaki Levenshtein mesafesini elle hesaplar.
    # Iki metin ayniysa mesafe sifirdir.
    if a == b:
        # Esitse 0 dondurur.
        return 0
    # a bos ise b uzunlugu kadar mesafe vardir.
    if len(a) == 0:
        # b uzunlugunu dondurur.
        return len(b)
    # b bos ise a uzunlugu kadar mesafe vardir.
    if len(b) == 0:
        # a uzunlugunu dondurur.
        return len(a)

    # Onceki satir icin baslangic maliyet dizisini olusturur.
    prev_row = list(range(len(b) + 1))
    # a karakterleri uzerinde dolasir.
    for i in range(1, len(a) + 1):
        # Guncel satir maliyetlerini baslatir.
        curr_row = [i] + [0] * len(b)
        # b karakterleri uzerinde dolasir.
        for j in range(1, len(b) + 1):
            # Karakterler ayniysa maliyeti 0, degilse 1 yapar.
            cost = 0 if a[i - 1] == b[j - 1] else 1
            # Ekleme, silme ve degistirme maliyetlerinden minimumunu secer.
            curr_row[j] = min(
                # Silme maliyeti.
                prev_row[j] + 1,
                # Ekleme maliyeti.
                curr_row[j - 1] + 1,
                # Degistirme maliyeti.
                prev_row[j - 1] + cost,
            )
        # Guncel satiri onceki satir olarak ayarlar.
        prev_row = curr_row
    # Son hucredeki mesafeyi dondurur.
    return prev_row[-1]

# bilgi.txt icerigini okuyup listelere ayiran fonksiyon baslangici.
def load_bilgi(filename):
    # Turkce yorum: bilgi.txt icinden hata adlari ve cozumleri listelere ayirir.
    # Hata isimlerini tutacak listeyi baslatir.
    errors = []
    # Cozumleri tutacak listeyi baslatir.
    solutions = []
    # Dosya yoksa bos listelerle doner.
    if not os.path.exists(filename):
        # Bos listeleri dondurur.
        return errors, solutions

    # Dosyayi okuma modunda acar.
    with open(filename, "r", encoding="utf-8") as f:
        # Dosyadaki her satiri isler.
        for line in f:
            # Satir sonu bosluklarini temizler.
            line = line.strip()
            # Satir bos ise atlar.
            if not line:
                # Sonraki satira gecer.
                continue
            # Ayirac yoksa satiri atlar.
            if ":" not in line:
                # Sonraki satira gecer.
                continue
            # Ilk iki parcaya boler.
            parts = line.split(":", 1)
            # Hata adini alir.
            error_name = parts[0].strip()
            # Cozum metnini alir.
            solution = parts[1].strip()
            # Hata adi bossa eklemez.
            if error_name:
                # Hata adini listeye ekler.
                errors.append(error_name)
                # Cozumu listeye ekler.
                solutions.append(solution)
    # Listeleri dondurur.
    return errors, solutions

# En iyi eslesmeyi bulan fonksiyon baslangici.
def best_match(user_text, errors):
    # Turkce yorum: En kucuk Levenshtein mesafesine sahip hatayi bulur.
    # En iyi eslesme indeksini baslatir.
    best_index = -1
    # En iyi mesafe degerini baslatir.
    best_distance = None
    # Tum hata adlarini gezer.
    for i in range(len(errors)):
        # Kullanici girdisi ile hata adi arasindaki mesafeyi hesaplar.
        dist = levenshtein_distance(user_text, errors[i])
        # Daha kucuk bir mesafe bulunduysa gunceller.
        if best_distance is None or dist < best_distance:
            # En iyi mesafeyi gunceller.
            best_distance = dist
            # En iyi indeksi gunceller.
            best_index = i
    # Sonucu dondurur.
    return best_index, best_distance

# Mesaji kuyruk dosyasina yazan fonksiyon baslangici.
def write_to_queue(message, filename):
    # Turkce yorum: Mesaji kuyruk dosyasina ekler ve yeni konumu dondurur.
    # Dosyayi ekleme modunda acar.
    with open(filename, "a", encoding="utf-8") as f:
        # Mesaji BOT etiketiyle yazar.
        f.write("BOT:" + message + "\n")
        # Yazma sonrasi dosya konumunu dondurur.
        return f.tell()

# Operator cevabini bekleyen fonksiyon baslangici.
def wait_for_operator(filename, last_pos):
    # Turkce yorum: Operator cevabini bekler.
    # Cevap geldi mi bilgisini tutar.
    responded = False
    # Cevap metnini saklar.
    response_text = ""
    # Cevap gelene kadar doner.
    while not responded:
        # Dosyayi okuma modunda acar.
        with open(filename, "r", encoding="utf-8") as f:
            # Son okuma konumuna gider.
            f.seek(last_pos)
            # Kalan satirlari okur.
            lines = f.readlines()
            # Guncel konumu kaydeder.
            last_pos = f.tell()
        # Yeni okunan satirlari kontrol eder.
        for line in lines:
            # Operator etiketi varsa cevap bulunur.
            if line.startswith("OPERATOR:"):
                # Etiketi temizleyip cevabi alir.
                response_text = line[len("OPERATOR:"):].strip()
                # Cevap geldi durumunu isaretler.
                responded = True
                # Donguden cikar.
                break
        # Biraz bekleyerek tekrar dener.
        time.sleep(1)
    # Cevap ve yeni konumu dondurur.
    return response_text, last_pos

# Tehlikeli anahtar kelimeleri kontrol eden fonksiyon baslangici.
def contains_danger(text):
    # Turkce yorum: Tehlikeli anahtar kelimeleri kontrol eder.
    # Tehlikeli kelimeleri liste olarak tanimlar.
    danger_words = [
        # Veritabani ile ilgili kelime.
        "database",
        # Kisa veritabani ifadesi.
        "db",
        # Uretim ortami ifadesi.
        "production",
        # Uretim ortami kisaltmasi.
        "prod",
        # Silme eylemi ifadesi.
        "deleted",
        # Silme komutu ifadesi.
        "drop",
        # Cokme ifadesi.
        "crash",
        # Guvenlik ifadesi.
        "security",
        # Kimlik dogrulama ifadesi.
        "auth",
        # Odeme ifadesi.
        "payment",
        # Para ifadesi.
        "money",
        # Dagitim ifadesi.
        "deployment",
        # Dagitma fiili.
        "deploy",
    ]
    # Metni kucuk harfe cevirir.
    text_lower = text.lower()
    # Tehlikeli kelimeleri tek tek kontrol eder.
    for word in danger_words:
        # Metin icinde kelime geciyorsa tehlikeli sayar.
        if word in text_lower:
            # Tehlike var sonucu dondurur.
            return True
    # Hic tehlike yoksa False dondurur.
    return False

# HOTL yonlendirme gerekcesini olusturan fonksiyon baslangici.
def build_hotl_escalation_reason(user_input, idx, dist):
    # Turkce yorum: HOTL modunda neden operator'a yonlendirme yapildigini aciklar.
    # Gerekce listesini baslatir.
    reasons = []
    # Tehlikeli kelime varsa gerekce ekler.
    if contains_danger(user_input):
        # Tehlikeli kelime gerekcesini ekler.
        reasons.append("tehlikeli anahtar kelime")
    # Eslesme yoksa gerekce ekler.
    if dist is None or idx == -1:
        # Bilgi tabaninda eslesme olmadigini ekler.
        reasons.append("bilgi tabaninda benzer eslesme bulunamadi")
    # Mesafe yuksekse belirsizlik gerekcesi ekler.
    elif dist > 4:
        # Yüksek belirsizlik gerekcesini ekler.
        reasons.append("yuksek belirsizlik (Levenshtein mesafesi > 4)")
    # Hic gerekce yoksa varsayilan metin dondurur.
    if not reasons:
        # Varsayilan gerekceyi dondurur.
        return "operator'a yonlendirme karari verildi"
    # Gerekceleri virgulle birlestirip dondurur.
    return ", ".join(reasons)

# Programin ana fonksiyonu baslangici.
def main():
    # Arguman sayisini kontrol eder.
    if len(sys.argv) < 2:
        # Kullanim bilgisini yazdirir.
        print("Kullanim: python3 bot.py hootl|hitl|hotl")
        # Erken cikis yapar.
        return

    # Mod bilgisini kucuk harfe cevirip alir.
    mode = sys.argv[1].lower()
    # Mod gecerli degilse uyarir.
    if mode not in ["hootl", "hitl", "hotl"]:
        # Gecersiz mod mesajini yazdirir.
        print("Gecersiz mod. hootl, hitl veya hotl kullanin.")
        # Erken cikis yapar.
        return

    # Bilgi dosyasi adini belirler.
    bilgi_file = "bilgi.txt"
    # Kuyruk dosyasi adini belirler.
    kuyruk_file = "kuyruk.txt"

    # Kuyruk dosyasi yoksa olusturur.
    if not os.path.exists(kuyruk_file):
        # Bos dosya olusturup kapatir.
        open(kuyruk_file, "w").close()

    # Bilgi dosyasindan hata ve cozumleri okur.
    errors, solutions = load_bilgi(bilgi_file)

    # HOOTL ve HOTL icin en az 12 satir kontrolu yapar.
    if mode in ["hootl", "hotl"] and len(errors) < 12:
        # Bilgi dosyasinin yetersiz oldugunu bildirir.
        print("bilgi.txt en az 12 satir icermelidir.")
        # Erken cikis yapar.
        return

    # Son okuma konumunu sifirlar.
    last_pos = 0

    # Surekli kullanici girdisi almak icin dongu baslatir.
    while True:
        # Kullanici girdisini almayi dener.
        try:
            # Kullaniciya mesaj sorar.
            user_input = input("Hata kodu veya mesaj girin (cikmak icin 'exit'): ")
        # STDIN kapanirsa donguden cikar.
        except EOFError:
            # Turkce yorum: STDIN kapaninca donguden cik.
            # Donguyu sonlandirir.
            break
        # Kullanici exit yazarsa cikis yapar.
        if user_input.lower() == "exit":
            # Donguyu sonlandirir.
            break

        # HOOTL modunu isler.
        if mode == "hootl":
            # En iyi eslesmeyi bulur.
            idx, dist = best_match(user_input, errors)
            # Mesafe uygunsa cevabi yazdirir.
            if dist is not None and dist <= 3 and idx != -1:
                # Cozum metnini yazdirir.
                print(solutions[idx])
            # Eslesme yoksa bilgi verir.
            else:
                # Hata bulunamadi mesajini yazdirir.
                print("Hata bulunamadi.")
            # Bir sonraki tura gecer.
            continue

        # HITL modunu isler.
        if mode == "hitl":
            # Mesaji kuyruga yazar ve konumu alir.
            last_pos = write_to_queue(user_input, kuyruk_file)
            # Operator cevabini bekler.
            response, last_pos = wait_for_operator(kuyruk_file, last_pos)
            # Operator cevabini yazdirir.
            print("Senior Engineer: " + response)
            # Bir sonraki tura gecer.
            continue

        # HOTL icin eslesmeyi hesaplar.
        idx, dist = best_match(user_input, errors)
        # Tehlikeli kelime kontrolu yapar.
        danger = contains_danger(user_input)

        # Tehlike veya belirsizlik durumunu kontrol eder.
        if danger or dist is None or idx == -1 or dist > 4:
            # Yönlendirme gerekcesini olusturur.
            reason = build_hotl_escalation_reason(user_input, idx, dist)
            # HOTL yonlendirme mesajini yazdirir.
            print("HOTL: " + reason + " -> operator'a yonlendiriliyor.")
            # Mesaji kuyruga yazar ve konumu alir.
            last_pos = write_to_queue(user_input, kuyruk_file)
            # Operator cevabini bekler.
            response, last_pos = wait_for_operator(kuyruk_file, last_pos)
            # Operator cevabini yazdirir.
            print("Senior Engineer: " + response)
        # Tehlike yoksa dogrudan cozum verir.
        else:
            # Eslesme varsa cozum yazdirir.
            if idx != -1:
                # Cozumu yazdirir.
                print(solutions[idx])
            # Eslesme yoksa yardim mesajini verir.
            else:
                # Yardim bulunamadi mesajini yazdirir.
                print("Yardim bulunamadi.")

# Dosya dogrudan calistirildiginda ana fonksiyon cagrisi.
if __name__ == "__main__":
    # Ana fonksiyonu baslatir.
    main()
