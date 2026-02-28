import sys

# ANSI 颜色转义码
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    GRAY = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_display_width(text):
    """获取字符串在终端中的显示宽度（处理中文字符）"""
    import unicodedata
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ('F', 'W', 'A'):
            width += 2
        else:
            width += 1
    return width

def pad_text(text, target_width):
    """根据终端宽度填充字符串"""
    current_width = get_display_width(text)
    if current_width >= target_width:
        return text
    return text + ' ' * (target_width - current_width)

def print_color(text, color=Colors.OKGREEN, end='\n'):
    """打印彩色文本"""
    print(f"{color}{text}{Colors.ENDC}", end=end)

def print_header(text):
    """打印大标题"""
    print_color("\n" + "="*50, Colors.HEADER)
    print_color(text.center(50), Colors.HEADER + Colors.BOLD)
    print_color("="*50 + "\n", Colors.HEADER)

def print_success(text):
    """打印成功信息"""
    print_color(f"✔ {text}", Colors.OKGREEN)

def print_error(text):
    """打印错误信息"""
    print_color(f"✘ {text}", Colors.FAIL)

def print_info(text):
    """打印一般信息"""
    print_color(f"ℹ {text}", Colors.OKCYAN)

def print_warning(text):
    """打印警告信息"""
    print_color(f"⚠ {text}", Colors.WARNING)

def print_hint(text):
    """打印提示信息"""
    print_color(f"💡 提示: {text}", Colors.WARNING + Colors.UNDERLINE)

def clear_screen():
    """清除屏幕（无闪烁版本）"""
    # 使用ANSI转义序列将光标移到顶部，然后清除屏幕
    # 这种方法比cls命令更平滑，不会产生闪烁
    print("\033[2J\033[H", end="")  # 清除整个屏幕并移动光标到左上角

def reset_cursor():
    """将光标重置到屏幕顶部（不清除内容）"""
    print("\033[H", end="")  # 仅移动光标到左上角

def get_key():
    """获取按键（处理方向键）"""
    if sys.platform == "win32":
        import msvcrt
        ch = msvcrt.getch()
        if ch in [b'\x00', b'\xe0']: # 方向键前缀
            ch = msvcrt.getch()
            return {b'H': 'up', b'P': 'down', b'K': 'left', b'M': 'right'}.get(ch, None)
        if ch == b'\r': return 'enter'
        if ch == b'\x1b': return 'esc'
        try:
            return ch.decode('utf-8').lower()
        except:
            return None
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return {'A': 'up', 'B': 'down', 'D': 'left', 'C': 'right'}.get(ch3, None)
            if ch == '\r' or ch == '\n': return 'enter'
            if ch == '\x1b': return 'esc'
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
