# Zamanla ilgili islemler icin time modulunu ice aktarir.
import time
# Dosya ve dizin islemleri icin os modulunu ice aktarir.
import os

# Operator cevabini dosyaya yazan fonksiyon baslangici.
def write_operator_reply(filename, reply):
    # Dosyayi ekleme modunda acmak icin context manager baslatir.
    with open(filename, "a", encoding="utf-8") as f:
        # Cevabi "OPERATOR:" etiketi ile birlikte dosyaya yazar.
        f.write("OPERATOR:" + reply + "\n")

# Dosyadaki son bos olmayan satiri okuyan fonksiyon baslangici.
def read_last_non_empty_line(filename):
    # Dosyayi okuma modunda acar ve tum satirlari okur.
    with open(filename, "r", encoding="utf-8") as f:
        # Satirlari sondaki bosluklardan temizlenmis halde listeye alir.
        lines = [line.strip() for line in f.readlines()]
    # Sondaki bos satirlari temizler.
    while lines and not lines[-1]:
        # Son satir bossa listeden cikarir.
        lines.pop()
    # Tum satirlar bos ise bos string dondurur.
    if not lines:
        # Bos sonuc dondurur.
        return ""
    # Son bos olmayan satiri dondurur.
    return lines[-1]

# Programin ana akisini yoneten fonksiyon baslangici.
def main():
    # Kuyruk dosya adini belirler.
    filename = "kuyruk.txt"
    # Dosya yoksa olusturur.
    if not os.path.exists(filename):
        # Bos dosya olusturup kapatir.
        open(filename, "w").close()
    # Son gorulen BOT satirini saklamak icin degisken olusturur.
    last_seen_bot_line = ""
    # Operatorun calistigini bildirir.
    print("Operator is running. Waiting for messages...")
    # Surekli dinleme dongusu baslatir.
    while True:
        # Kuyruk dosyasinin son bos olmayan satirini okur.
        last_line = read_last_non_empty_line(filename)
        # Yeni bir BOT mesaji gelmisse ve daha once gorulmemisse kontrol eder.
        if last_line.startswith("BOT:") and last_line != last_seen_bot_line:
            # Bu satiri son gorulen BOT satiri olarak kaydeder.
            last_seen_bot_line = last_line
            # BOT mesajinin etiketini temizleyip mesaji alir.
            message = last_line[len("BOT:"):].strip()
            # Yeni BOT mesajini ekrana yazdirir.
            print(f"New BOT message: {message}")
            # Operator cevabini alir.
            reply = input("Operator reply: ")
            # Cevap bos degilse dosyaya yazar.
            if reply.strip():
                # Operator cevabini kuyruk dosyasina ekler.
                write_operator_reply(filename, reply.strip())
        # Her turda 1 saniye bekler.
        time.sleep(1)

# Bu dosya dogrudan calistirildiysa ana fonksiyonu cagirir.
if __name__ == "__main__":
    # Ana program akisini baslatir.
    main()
