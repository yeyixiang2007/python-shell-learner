import sys
import random
from engine import GameEngine
from data import LEVELS
from utils import print_header, print_info, print_color, Colors, clear_screen, print_error, print_success

def welcome():
    clear_screen()
    print_header("🐧 Linux 命令学习游戏 🐧")
    print_info("欢迎来到 Linux 的世界！")
    print_color("在这个游戏中，你将通过模拟终端来学习最常用的 Linux 命令。", Colors.OKCYAN)
    print_color("规则：", Colors.WARNING)
    print_color("- 根据提示输入正确的 Linux 命令。", Colors.ENDC)
    print_color("- 如果卡住了，可以输入 'hint' 获取提示。", Colors.ENDC)
    print_color("- 输入 'exit' 或 'quit' 退出游戏。", Colors.ENDC)
    print_color("- 输入 'help' 查看帮助信息。", Colors.ENDC)
    print_color("\n准备好了吗？让我们开始吧！", Colors.BOLD + Colors.OKGREEN)
    input("\n按回车键进入主菜单...")

def print_menu():
    clear_screen()
    print_header("🐧 Linux 命令学习游戏 - 主菜单 🐧")
    print_color("1. 开始/继续游戏", Colors.OKGREEN)
    print_color("2. 选择关卡", Colors.OKCYAN)
    print_color("3. 随机挑战", Colors.OKBLUE)
    print_color("4. 查看进度", Colors.WARNING)
    print_color("5. 退出游戏", Colors.FAIL)
    print_color("\n请输入选项 (1-5): ", Colors.BOLD)

def view_progress(engine):
    clear_screen()
    print_header("📊 游戏进度 📊")
    print_info(f"当前关卡: {engine.current_level}")
    print_info(f"当前得分: {engine.score}")
    print_color("\n[C] 清除进度  [Any] 返回主菜单", Colors.WARNING)
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
                view_progress(engine)

            elif choice == '5':
                print("\n再见！")
                sys.exit()

    except KeyboardInterrupt:
        print("\n\n游戏已退出。再见！")
    except Exception as e:
        print(f"\n发生错误: {e}")

if __name__ == "__main__":
    main()
