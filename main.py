import sys
import random
import time
from engine import GameEngine
from data import LEVELS, ACHIEVEMENTS
from utils import print_header, print_info, print_color, Colors, clear_screen, print_error, print_success, get_key, pad_text, get_display_width

def welcome():
    clear_screen()
    print_header("🐧 Linux 命令学习游戏 🐧")
    print_info("欢迎来到 Linux 的世界！")
    print_color("在这个游戏中，你将通过模拟终端来学习最常用的 Linux 命令。", Colors.OKCYAN)

    print_color("\n[ 💡 游戏规则 ]", Colors.HEADER + Colors.BOLD)
    print_color("• 根据提示输入正确的 Linux 命令。", Colors.OKBLUE)
    print_color("• 如果卡住了，可以输入 'hint' 获取提示。", Colors.OKBLUE)
    print_color("• 连续错误 5 次可以选择直接显示答案。", Colors.OKBLUE)
    print_color("• 输入 'exit' 或 'quit' 退出游戏。", Colors.OKBLUE)
    print_color("• 输入 'help' 查看帮助信息。", Colors.OKBLUE)

    print_color("\n🚀 准备好了吗？让我们开始吧！", Colors.BOLD + Colors.OKGREEN)
    input("\n按回车键进入主菜单...")

def print_menu():
    clear_screen()
    print_header("🐧 Linux 命令学习游戏 - 主菜单 🐧")
    # 使用更有逻辑性的色彩搭配
    print_color(" 1. 🟢 开始/继续游戏", Colors.OKGREEN)
    print_color(" 2. 🔵 选择关卡", Colors.OKBLUE)
    print_color(" 3. 🔵 随机挑战", Colors.OKBLUE)
    print_color(" 4. 🟣 限时挑战", Colors.HEADER)
    print_color(" 5. 🟡 查看进度与成就", Colors.WARNING)
    print_color(" 6. 🔴 退出游戏", Colors.FAIL)
    print_color("\n请输入选项 (1-6): ", Colors.BOLD)

def view_progress(engine):
    clear_screen()
    print_header("📊 个人荣誉与进度 📊")
    print_color(f"👤 当前关卡: {engine.current_level}", Colors.OKCYAN)
    print_color(f"💰 当前总分: {engine.score}", Colors.WARNING)
    print_color(f"🔥 已完成挑战: {engine.challenges_completed}", Colors.OKGREEN)
    print_color(f"✨ 完美通关数: {engine.perfect_levels_count}", Colors.HEADER)

    print_header("🏆 成就勋章墙 🏆")
    for ach in ACHIEVEMENTS:
        unlocked = ach.id in engine.unlocked_achievements
        status = "⭐" if unlocked else "❓"
        color = Colors.OKGREEN if unlocked else Colors.FAIL
        # 对已解锁的成就加粗显示
        text_format = color + Colors.BOLD if unlocked else color
        print_color(f" {status} [{ach.name}]: {ach.description}", text_format)

    print_color("\n" + "-"*50, Colors.OKBLUE)
    print_color("[C] 清除进度 (重来)  [Any] 返回主菜单", Colors.BOLD)
    choice = input().strip().lower()
    if choice == 'c':
        engine.clear_progress()
        input("\n按回车键返回...")

def select_level_menu(engine):
    all_level_ids = sorted(list(LEVELS.keys()))
    if not all_level_ids:
        print_error("没有可用的关卡！")
        input("按回车键继续...")
        return

    # 找到当前最大解锁关卡（故事模式进度）
    max_unlocked = engine.current_level
    cursor_idx = 0
    # 将光标初始化在当前进度关卡
    if max_unlocked in all_level_ids:
        cursor_idx = all_level_ids.index(max_unlocked)

    while True:
        clear_screen()
        print_header("🎯 选择关卡 - 练习模式 🎯")
        print_color("使用 [方向键] 移动，[Enter] 开始，[Esc/Q] 返回", Colors.OKCYAN)
        print_color("说明: ⭐ 完美通关 | ✅ 已通关 | 🔒 未解锁\n", Colors.OKBLUE)

        # 三栏布局逻辑
        cols = 3
        rows = (len(all_level_ids) + cols - 1) // cols

        for r in range(rows):
            line = ""
            for c in range(cols):
                idx = r + c * rows
                if idx < len(all_level_ids):
                    lvl_id = all_level_ids[idx]

                    # 状态判定
                    status_icon = "  "
                    is_locked = lvl_id > max_unlocked
                    if is_locked:
                        status_icon = "🔒"
                        color = Colors.GRAY # 灰色
                    elif lvl_id in engine.perfect_level_ids:
                        status_icon = "⭐"
                        color = Colors.WARNING # 金色
                    elif lvl_id < max_unlocked:
                        status_icon = "✅"
                        color = Colors.OKGREEN
                    else:
                        status_icon = "▶ " # 当前进度
                        color = Colors.OKCYAN

                    # 选中效果
                    prefix = " > " if idx == cursor_idx else "   "
                    suffix = " < " if idx == cursor_idx else "   "

                    name = LEVELS[lvl_id]['name']
                    # 截断过长的名称（中英混合）
                    max_name_len = 10
                    display_name = name
                    if get_display_width(name) > max_name_len:
                        # 逐字截断以防破坏编码
                        display_name = ""
                        curr_w = 0
                        for char in name:
                            char_w = 2 if get_display_width(char) == 2 else 1
                            if curr_w + char_w > max_name_len - 2:
                                display_name += ".."
                                break
                            display_name += char
                            curr_w += char_w

                    # 构建一个固定宽度的项
                    name_padded = pad_text(display_name, max_name_len)
                    item_content = f"{status_icon} Lvl {lvl_id:2}: {name_padded}"

                    # 组合完整行项
                    full_item = f"{prefix}{item_content}{suffix}"

                    # 选中的项加粗并反色（可选）
                    if idx == cursor_idx:
                        line += f"{Colors.BOLD}{color}{full_item}{Colors.ENDC}"
                    else:
                        line += f"{color}{full_item}{Colors.ENDC}"

                    # 栏间距
                    line += "  "
                else:
                    line += " " * 32 # 占位
            print(line)

        # 处理按键
        key = get_key()
        if key == 'up':
            if cursor_idx > 0: cursor_idx -= 1
        elif key == 'down':
            if cursor_idx < len(all_level_ids) - 1: cursor_idx += 1
        elif key == 'left':
            cursor_idx = max(0, cursor_idx - rows)
        elif key == 'right':
            cursor_idx = min(len(all_level_ids) - 1, cursor_idx + rows)
        elif key == 'enter':
            selected_id = all_level_ids[cursor_idx]
            if selected_id > max_unlocked:
                print_error(f"\n关卡 {selected_id} 尚未解锁！请先完成之前的挑战。")
                time.sleep(1)
            else:
                engine.start_level(level_id=selected_id, mode='single')
                # 重新同步进度（如果单关练习导致进度改变，虽然目前逻辑不会，但这样更稳健）
                max_unlocked = engine.current_level
        elif key in ['esc', 'q']:
            break

def main():
    try:
        engine = GameEngine()
        welcome()

        while True:
            print_menu()
            choice = input().strip()

            if choice == '1':
                engine.is_running = True
                while engine.is_running:
                    engine.start_level(mode='story')

            elif choice == '2':
                select_level_menu(engine)

            elif choice == '3':
                if not LEVELS:
                    print_error("没有可用的关卡！")
                    input("按回车键继续...")
                    continue
                lvl = random.choice(list(LEVELS.keys()))
                engine.is_running = True
                engine.start_level(level_id=lvl, mode='single')

            elif choice == '4':
                engine.start_time_attack()

            elif choice == '5':
                view_progress(engine)

            elif choice == '6':
                print("\n再见！")
                sys.exit()

    except KeyboardInterrupt:
        print("\n\n游戏已退出。再见！")
    except Exception as e:
        print(f"\n发生错误: {e}")

if __name__ == "__main__":
    main()
