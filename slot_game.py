#!/usr/bin/env python3
"""
🎰 カジノ スロットマシン 🎰
楽しいスロットゲームへようこそ！
"""

import random
import time
import os
import sys


# ===== 定数 =====
SYMBOLS = {
    "🍒": {"name": "チェリー",   "weight": 30, "value": 2},
    "🍋": {"name": "レモン",     "weight": 25, "value": 3},
    "🍊": {"name": "オレンジ",   "weight": 20, "value": 4},
    "🍇": {"name": "ブドウ",     "weight": 15, "value": 5},
    "🔔": {"name": "ベル",       "weight": 8,  "value": 10},
    "⭐": {"name": "スター",     "weight": 5,  "value": 20},
    "💎": {"name": "ダイヤ",     "weight": 3,  "value": 50},
    "7️⃣": {"name": "セブン",     "weight": 2,  "value": 100},
}

SYMBOL_LIST = list(SYMBOLS.keys())
WEIGHTS = [SYMBOLS[s]["weight"] for s in SYMBOL_LIST]

REELS = 3
STARTING_COINS = 100
BET_OPTIONS = [5, 10, 25, 50]

# ANSI カラー
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
BLINK   = "\033[5m"


# ===== ユーティリティ =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")


def slow_print(text: str, delay: float = 0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def spin_animation(duration: float = 1.2):
    """スロットが回るアニメーション"""
    frames = 12
    interval = duration / frames
    for _ in range(frames):
        reels = [random.choice(SYMBOL_LIST) for _ in range(REELS)]
        line = "  ".join(reels)
        print(f"\r  ┃ {line} ┃  ", end="", flush=True)
        time.sleep(interval)
    print()


def weighted_choice() -> str:
    return random.choices(SYMBOL_LIST, weights=WEIGHTS, k=1)[0]


# ===== 勝利判定 =====
def check_win(result: list[str], bet: int) -> tuple[int, str]:
    """(獲得コイン, メッセージ) を返す"""
    a, b, c = result

    if a == b == c:
        symbol = a
        multiplier = SYMBOLS[symbol]["value"]
        prize = bet * multiplier
        if symbol == "7️⃣":
            msg = f"{BOLD}{RED}{BLINK}🎊 ジャックポット！！ 7-7-7 !! × {multiplier}{RESET}"
        elif symbol == "💎":
            msg = f"{BOLD}{CYAN}💎 ダイヤ ３つ揃い！ × {multiplier}{RESET}"
        elif symbol == "⭐":
            msg = f"{BOLD}{YELLOW}⭐ スター ３つ揃い！ × {multiplier}{RESET}"
        else:
            msg = f"{GREEN}✨ ３つ揃い！ {SYMBOLS[symbol]['name']} × {multiplier}{RESET}"
        return prize, msg

    if a == b or b == c or a == c:
        # 2つ揃い
        if a == b:
            sym = a
        elif b == c:
            sym = b
        else:
            sym = a
        multiplier = max(1, SYMBOLS[sym]["value"] // 4)
        prize = bet * multiplier
        msg = f"{YELLOW}🎯 ２つ揃い！ {SYMBOLS[sym]['name']} × {multiplier}{RESET}"
        return prize, msg

    return 0, f"{RED}ハズレ... もう一度！{RESET}"


# ===== 表示 =====
def print_header():
    print(f"{BOLD}{YELLOW}")
    print("  ╔══════════════════════════════╗")
    print("  ║   🎰  カジノ スロット  🎰    ║")
    print("  ╚══════════════════════════════╝")
    print(f"{RESET}")


def print_paytable():
    print(f"{BOLD}{CYAN}  ╔═══════ 配当表 ═══════╗{RESET}")
    print(f"{CYAN}  ║  シンボル   ３揃い倍率 ║{RESET}")
    print(f"{CYAN}  ╠═════════════════════════╣{RESET}")
    for sym, info in SYMBOLS.items():
        name  = info["name"]
        val   = info["value"]
        bar   = "★" * min(val // 10 + 1, 8)
        print(f"{CYAN}  ║  {sym}  {name:<6} ×{val:<4}  {bar:<8}║{RESET}")
    print(f"{CYAN}  ╚═════════════════════════╝{RESET}")
    print(f"  {WHITE}２つ揃い: ３揃い倍率の 1/4{RESET}\n")


def print_status(coins: int, total_bet: int, total_won: int, spins: int):
    net = total_won - total_bet
    color = GREEN if net >= 0 else RED
    print(f"\n  {BOLD}💰 コイン: {YELLOW}{coins}{RESET}  "
          f"{WHITE}| 回転数: {spins}  "
          f"| 収支: {color}{net:+d}{RESET}")


def print_result_box(result: list[str]):
    line = "   ".join(result)
    print(f"\n  {BOLD}┏━━━━━━━━━━━━━━━━━━━━━━━┓{RESET}")
    print(f"  {BOLD}┃   {line}   ┃{RESET}")
    print(f"  {BOLD}┗━━━━━━━━━━━━━━━━━━━━━━━┛{RESET}")


def choose_bet(coins: int) -> int:
    valid = [b for b in BET_OPTIONS if b <= coins]
    if not valid:
        return coins  # 全額ベット

    print(f"\n  {BOLD}ベット額を選んでください:{RESET}")
    for i, b in enumerate(valid, 1):
        print(f"    {CYAN}{i}{RESET}. {b} コイン")
    print(f"    {CYAN}0{RESET}. カスタム金額")

    while True:
        try:
            choice = input(f"\n  {BOLD}>{RESET} ").strip()
            if choice == "0":
                custom = int(input(f"  ベット額を入力 (1-{coins}): "))
                if 1 <= custom <= coins:
                    return custom
                print(f"  {RED}1〜{coins} の範囲で入力してください{RESET}")
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(valid):
                    return valid[idx]
                print(f"  {RED}有効な番号を入力してください{RESET}")
        except (ValueError, KeyboardInterrupt):
            print(f"  {RED}有効な入力をしてください{RESET}")


# ===== メインゲームループ =====
def main():
    clear()
    print_header()
    slow_print(f"  {WHITE}スロットマシンへようこそ！{RESET}")
    print(f"  スタートコイン: {YELLOW}{BOLD}{STARTING_COINS}{RESET}\n")
    time.sleep(0.5)

    print_paytable()
    input(f"  {CYAN}[Enter] でゲーム開始！{RESET}")

    coins = STARTING_COINS
    spins = 0
    total_bet = 0
    total_won = 0
    best_win = 0

    while True:
        clear()
        print_header()
        print_status(coins, total_bet, total_won, spins)

        if coins <= 0:
            print(f"\n  {RED}{BOLD}💸 コインが尽きました！ゲームオーバー{RESET}")
            break

        print(f"\n  {BOLD}[s]{RESET} スピン  {BOLD}[p]{RESET} 配当表  {BOLD}[q]{RESET} 終了")
        action = input(f"  {BOLD}>{RESET} ").strip().lower()

        if action == "q":
            break
        elif action == "p":
            clear()
            print_paytable()
            input(f"  {CYAN}[Enter] で戻る{RESET}")
            continue
        elif action != "s":
            continue

        # ベット選択
        bet = choose_bet(coins)
        coins -= bet
        total_bet += bet
        spins += 1

        # スピン
        clear()
        print_header()
        print(f"\n  {BOLD}🎰 スピン中...{RESET}")
        spin_animation(1.5)

        # 結果
        result = [weighted_choice() for _ in range(REELS)]
        prize, msg = check_win(result, bet)

        print_result_box(result)
        print(f"\n  {msg}")

        if prize > 0:
            coins += prize
            total_won += prize
            if prize > best_win:
                best_win = prize
            print(f"  {GREEN}{BOLD}+{prize} コイン獲得！{RESET}")
            if prize >= bet * 10:
                # 大当たり演出
                for _ in range(3):
                    print(f"  {YELLOW}{BOLD}🎊🎊🎊  大当たり！！  🎊🎊🎊{RESET}")
                    time.sleep(0.3)
        else:
            print(f"  {RED}-{bet} コイン{RESET}")

        print_status(coins, total_bet, total_won, spins)
        input(f"\n  {CYAN}[Enter] で続ける{RESET}")

    # ゲーム終了サマリー
    clear()
    print_header()
    print(f"\n  {BOLD}{CYAN}━━━━━ ゲーム終了 ━━━━━{RESET}")
    print(f"  総スピン数 : {WHITE}{spins}{RESET}")
    print(f"  最終コイン : {YELLOW}{coins}{RESET}")
    net = total_won - total_bet
    color = GREEN if net >= 0 else RED
    print(f"  収   支   : {color}{BOLD}{net:+d}{RESET}")
    print(f"  最高獲得  : {YELLOW}{best_win}{RESET} コイン")
    print(f"\n  {BOLD}またのご来店をお待ちしております！{RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}ゲームを終了しました。またね！{RESET}\n")
        sys.exit(0)
