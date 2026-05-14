import os
import sys
import time

def levenshtein_distance(a, b):
    # Turkce yorum: Iki metin arasindaki Levenshtein mesafesini elle hesaplar.
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)

    prev_row = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        curr_row = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr_row[j] = min(
                prev_row[j] + 1,
                curr_row[j - 1] + 1,
                prev_row[j - 1] + cost,
            )
        prev_row = curr_row
    return prev_row[-1]

def load_bilgi(filename):
    # Turkce yorum: bilgi.txt icinden hata adlari ve cozumleri listelere ayirir.
    errors = []
    solutions = []
    if not os.path.exists(filename):
        return errors, solutions

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                continue
            parts = line.split(":", 1)
            error_name = parts[0].strip()
            solution = parts[1].strip()
            if error_name:
                errors.append(error_name)
                solutions.append(solution)
    return errors, solutions

def best_match(user_text, errors):
    # Turkce yorum: En kucuk Levenshtein mesafesine sahip hatayi bulur.
    best_index = -1
    best_distance = None
    for i in range(len(errors)):
        dist = levenshtein_distance(user_text, errors[i])
        if best_distance is None or dist < best_distance:
            best_distance = dist
            best_index = i
    return best_index, best_distance

def write_to_queue(message, filename):
    # Turkce yorum: Mesaji kuyruk dosyasina ekler ve yeni konumu dondurur.
    with open(filename, "a", encoding="utf-8") as f:
        f.write("BOT:" + message + "\n")
        return f.tell()

def wait_for_operator(filename, last_pos):
    # Turkce yorum: Operator cevabini bekler.
    responded = False
    response_text = ""
    while not responded:
        with open(filename, "r", encoding="utf-8") as f:
            f.seek(last_pos)
            lines = f.readlines()
            last_pos = f.tell()
        for line in lines:
            if line.startswith("OPERATOR:"):
                response_text = line[len("OPERATOR:"):].strip()
                responded = True
                break
        time.sleep(1)
    return response_text, last_pos

def contains_danger(text):
    # Turkce yorum: Tehlikeli anahtar kelimeleri kontrol eder.
    danger_words = ["database", "production", "crash", "fire", "deleted"]
    text_lower = text.lower()
    for word in danger_words:
        if word in text_lower:
            return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Kullanim: python3 bot.py hootl|hitl|hotl")
        return

    mode = sys.argv[1].lower()
    if mode not in ["hootl", "hitl", "hotl"]:
        print("Gecersiz mod. hootl, hitl veya hotl kullanin.")
        return

    bilgi_file = "bilgi.txt"
    kuyruk_file = "kuyruk.txt"

    if not os.path.exists(kuyruk_file):
        open(kuyruk_file, "w").close()

    errors, solutions = load_bilgi(bilgi_file)

    if mode in ["hootl", "hotl"] and len(errors) < 12:
        print("bilgi.txt en az 12 satir icermelidir.")
        return

    last_pos = 0

    while True:
        try:
            user_input = input("Hata kodu veya mesaj girin (cikmak icin 'exit'): ")
        except EOFError:
            # Turkce yorum: STDIN kapaninca donguden cik.
            break
        if user_input.lower() == "exit":
            break

        if mode == "hootl":
            idx, dist = best_match(user_input, errors)
            if dist is not None and dist <= 3 and idx != -1:
                print(solutions[idx])
            else:
                print("Hata bulunamadi.")
            continue

        if mode == "hitl":
            last_pos = write_to_queue(user_input, kuyruk_file)
            response, last_pos = wait_for_operator(kuyruk_file, last_pos)
            print("Senior Engineer: " + response)
            continue

        idx, dist = best_match(user_input, errors)
        danger = contains_danger(user_input)

        if danger or dist is None or idx == -1 or dist > 4:
            last_pos = write_to_queue(user_input, kuyruk_file)
            response, last_pos = wait_for_operator(kuyruk_file, last_pos)
            print("Senior Engineer: " + response)
        else:
            if idx != -1:
                print(solutions[idx])
            else:
                print("Yardim bulunamadi.")

if __name__ == "__main__":
    main()
