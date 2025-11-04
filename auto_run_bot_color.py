import sys, os
import subprocess
from watchgod import watch, Change
from colorama import Fore, Style, init

# Инициализация colorama
init(autoreset=True)

BOT_FILE = "oracle_bot.py"  # путь к твоему боту
WATCH_FILES = (".py", "predictions.txt")  # следим за Python файлами и предсказаниями

print(f"{Fore.GREEN}[✨] Автоперезапуск OracleBot включён. Любые изменения перезапустят бота.{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}[👀] Наблюдаем за изменениями в папке: .{Style.RESET_ALL}")

process = None

def restart_bot():
    global process
    if process:
        process.terminate()
        print(f"{Fore.YELLOW}[⚡] Бот остановлен для перезапуска.{Style.RESET_ALL}")
    process = subprocess.Popen([sys.executable, BOT_FILE])
    print(f"{Fore.GREEN}[🚀] Бот запущен.{Style.RESET_ALL}")

# Первый запуск бота
restart_bot()

# Следим за изменениями
for changes in watch("."):
    relevant = [f for change_type, f in changes if f.endswith(WATCH_FILES)]
    if relevant:
        print(f"{Fore.CYAN}[🔄] Изменения обнаружены в файлах: {relevant}{Style.RESET_ALL}")
        restart_bot()

