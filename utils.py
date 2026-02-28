import sys

# ANSI 颜色转义码
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    """清除屏幕（跨平台模拟）"""
    print("\033[H\033[J", end="")
