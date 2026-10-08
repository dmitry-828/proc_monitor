import psutil
import time

print("Монитор процессов запущен. Нажми Ctrl+C для выхода.\n")

while True:
    for proc in psutil.process_iter(['pid', 'name']):
        info = proc.info
        print(f"PID: {info['pid']:>6} | Имя: {info['name']}")
    print("-" * 40)
    time.sleep(3)