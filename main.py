import sys
import random
from engine import GameEngine
from data import LEVELS
from utils import print_header, print_info, print_color, Colors, clear_screen, print_error, print_success
from data import ACHIEVEMENTS

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

    print_header("🏆 成就勋章墙 🏆")
    for ach in ACHIEVEMENTS:
        unlocked = ach.id in engine.unlocked_achievements
        status = "⭐" if unlocked else "�"
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

def main():
    try:
        welcome()
        engine = GameEngine()

        while True:
            print_menu()
            choice = input().strip()

            if choice == '1':
                engine.is_running = True
                while engine.is_running:
                    engine.start_level(mode='story')

            elif choice == '2':
                try:
                    lvl_input = input("请输入关卡 ID (1-60): ").strip()
                    if not lvl_input: continue
                    lvl = int(lvl_input)
                    if lvl in LEVELS:
                        engine.current_level = lvl
                        engine.is_running = True
                        while engine.is_running:
                            engine.start_level(mode='story')
                    else:
                        print_error("无效的关卡 ID！")
                        input("按回车键继续...")
                except ValueError:
                    print_error("请输入数字！")
                    input("按回车键继续...")

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
