import time
import os

def write_operator_reply(filename, reply):
    with open(filename, "a", encoding="utf-8") as f:
        f.write("OPERATOR:" + reply + "\n")

def read_last_non_empty_line(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    while lines and not lines[-1]:
        lines.pop()
    if not lines:
        return ""
    return lines[-1]

def main():
    filename = "kuyruk.txt"
    if not os.path.exists(filename):
        open(filename, "w").close()
    last_seen_bot_line = ""
    print("Operator is running. Waiting for messages...")
    while True:
        last_line = read_last_non_empty_line(filename)
        if last_line.startswith("BOT:") and last_line != last_seen_bot_line:
            last_seen_bot_line = last_line
            message = last_line[len("BOT:"):].strip()
            print(f"New BOT message: {message}")
            reply = input("Operator reply: ")
            if reply.strip():
                write_operator_reply(filename, reply.strip())
        time.sleep(1)

if __name__ == "__main__":
    main()
