import os
import json
import random
import time

from data import LEVELS, Challenge, ACHIEVEMENTS
from utils import print_color, print_success, print_error, print_info, print_warning, print_hint, Colors, clear_screen, print_header

class GameEngine:
    def __init__(self):
        self.current_level = 1
        self.current_challenge_index = 0
        self.score = 0
        self.is_running = True
        self.consecutive_failures = 0
        self.unlocked_achievements = set()
        self.hints_used = 0
        self.challenges_completed = 0
        self.errors_in_current_level = 0
        self.perfect_levels_count = 0
        self.load_progress()


    def load_progress(self):
        try:
            if os.path.exists("progress.json"):
                with open("progress.json", "r") as f:
                    data = json.load(f)
                    self.current_level = data.get("level", 1)
                    self.score = data.get("score", 0)
                    self.unlocked_achievements = set(data.get("achievements", []))
                    self.challenges_completed = data.get("challenges_completed", 0)
                    self.hints_used = data.get("hints_used", 0)
                    self.perfect_levels_count = data.get("perfect_levels_count", 0)
        except Exception as e:
            print_error(f"加载进度失败: {e}")

    def save_progress(self):
        try:
            with open("progress.json", "w") as f:
                json.dump({
                    "level": self.current_level,
                    "score": self.score,
                    "achievements": list(self.unlocked_achievements),
                    "challenges_completed": self.challenges_completed,
                    "hints_used": self.hints_used,
                    "perfect_levels_count": self.perfect_levels_count
                }, f)
        except Exception as e:
            print_error(f"保存进度失败: {e}")

    def check_achievement(self, condition_type, value=None):
        for achievement in ACHIEVEMENTS:
            if achievement.id in self.unlocked_achievements:
                continue

            unlocked = False
            if achievement.condition == "complete_first_challenge" and condition_type == "complete_challenge" and self.challenges_completed >= 1:
                unlocked = True
            elif achievement.condition == "fail_5_times" and condition_type == "fail" and self.consecutive_failures >= 5:
                unlocked = True
            elif achievement.condition == "use_5_hints" and condition_type == "hint" and self.hints_used >= 5:
                unlocked = True
            elif achievement.condition == "use_20_hints" and condition_type == "hint" and self.hints_used >= 20:
                unlocked = True
            elif achievement.condition == "score_50_time_attack" and condition_type == "time_attack_score" and value >= 50:
                unlocked = True
            elif achievement.condition == "score_100_time_attack" and condition_type == "time_attack_score" and value >= 100:
                unlocked = True
            elif achievement.condition == "complete_10_in_time_attack" and condition_type == "time_attack_completed" and value >= 10:
                unlocked = True
            elif achievement.condition == "total_score_100" and condition_type == "score" and self.score >= 100:
                unlocked = True
            elif achievement.condition == "total_score_500" and condition_type == "score" and self.score >= 500:
                unlocked = True
            elif achievement.condition == "total_score_1000" and condition_type == "score" and self.score >= 1000:
                unlocked = True
            elif achievement.condition == "reach_level_10" and condition_type == "level" and self.current_level >= 10:
                unlocked = True
            elif achievement.condition == "reach_level_20" and condition_type == "level" and self.current_level >= 20:
                unlocked = True
            elif achievement.condition == "reach_level_30" and condition_type == "level" and self.current_level >= 30:
                unlocked = True
            elif achievement.condition == "reach_level_50" and condition_type == "level" and self.current_level >= 50:
                unlocked = True
            elif achievement.condition == "perfect_level_completion" and condition_type == "perfect_level":
                unlocked = True
            elif achievement.condition == "cumulative_5_perfect_levels" and condition_type == "perfect_level" and self.perfect_levels_count >= 5:
                unlocked = True
            elif achievement.condition == "complete_50_challenges" and condition_type == "complete_challenge" and self.challenges_completed >= 50:
                unlocked = True
            elif achievement.condition == "complete_100_challenges" and condition_type == "complete_challenge" and self.challenges_completed >= 100:
                unlocked = True
            elif achievement.condition == "unlock_10_achievements" and condition_type == "unlock_achievement" and len(self.unlocked_achievements) >= 10:
                unlocked = True
            elif achievement.condition == "complete_all_levels" and condition_type == "all_levels":
                unlocked = True

            if unlocked:
                self.unlocked_achievements.add(achievement.id)
                print_color(f"\n🏆 解锁成就: {achievement.name} - {achievement.description} 🏆", Colors.BOLD + Colors.OKGREEN)
                self.save_progress()
                # Check for collector achievement after unlocking one
                if achievement.id != "collector":
                    self.check_achievement("unlock_achievement")

    def clear_progress(self):
        self.current_level = 1
        self.score = 0
        self.unlocked_achievements = set()
        self.challenges_completed = 0
        self.hints_used = 0
        self.perfect_levels_count = 0
        self.save_progress()
        print_success("进度已清除！")

    def get_current_challenge(self) -> Challenge:

        level_data = LEVELS.get(self.current_level)
        if level_data:
            challenges = level_data.get("challenges")
            if self.current_challenge_index < len(challenges):
                return challenges[self.current_challenge_index]
        return None

    def start_level(self, level_id=None, mode='story'):
        self.mode = mode
        if level_id:
            self.current_level = level_id

        level_data = LEVELS.get(self.current_level)
        if not level_data:
            if self.mode == 'story':
                self.game_over()
            else:
                print_error("关卡不存在！")
                self.is_running = False
            return

        clear_screen()
        print_color(f"--- 关卡 {self.current_level}: {level_data['name']} ---", Colors.HEADER + Colors.BOLD)
        self.current_challenge_index = 0
        self.errors_in_current_level = 0 # Reset error count for the new level
        self.play_challenge()

    def play_challenge(self):
        challenge = self.get_current_challenge()
        if not challenge:
            self.finish_level()
            return

        print_info(f"\n挑战 {challenge.id}: {challenge.title}")
        print_color(challenge.description, Colors.OKBLUE)
        print_color(f"当前路径: {challenge.initial_path}", Colors.UNDERLINE)

        attempts = 0
        self.consecutive_failures = 0 # Reset for new challenge

        while True:
            # Check for failure threshold
            if self.consecutive_failures >= 5:
                self.check_achievement("fail") # Check achievement
                print_color("\n你已经连续错误 5 次了。", Colors.WARNING)
                choice = input(f"{Colors.WARNING}是否直接显示答案？(y/n): {Colors.ENDC}").strip().lower()
                if choice == 'y':
                    print_info(f"参考答案: {challenge.expected_command[0]}")
                    # Reset failure count so we don't ask again immediately if they type wrong again
                    self.consecutive_failures = 0
                    continue

            user_input = input(f"{Colors.OKGREEN}user@linux-game:{challenge.initial_path}$ {Colors.ENDC}").strip()

            if user_input.lower() in ['exit', 'quit']:
                self.is_running = False
                return

            if user_input.lower() == 'hint':
                self.hints_used += 1
                self.check_achievement("hint")
                print_hint(challenge.hint)
                continue

            if user_input.lower() == 'help':
                print_info("可用命令: [你的 Linux 命令], hint (提示), help (帮助), exit (退出)")
                continue

            if user_input in challenge.expected_command:
                self.consecutive_failures = 0
                self.success(challenge)
                break
            else:
                attempts += 1
                self.consecutive_failures += 1
                self.handle_failure(user_input, attempts)

    def start_time_attack(self, duration=60):
        clear_screen()
        print_header("⏱️ 限时挑战模式 ⏱️")
        print_info(f"你有 {duration} 秒的时间尽可能多地完成挑战！")
        input("按回车键开始...")

        start_time = time.time()
        score = 0
        completed_count = 0

        # Flatten all challenges
        all_challenges = []
        for lvl in LEVELS.values():
            all_challenges.extend(lvl['challenges'])

        while True:
            elapsed = time.time() - start_time
            remaining = duration - elapsed

            if remaining <= 0:
                break

            challenge = random.choice(all_challenges)
            print_color(f"\n[剩余时间: {int(remaining)}s] 挑战: {challenge.title}", Colors.BOLD)
            print_color(challenge.description, Colors.OKBLUE)

            # Simple input loop for time attack
            user_input = input(f"{Colors.OKGREEN}user@linux-game:{challenge.initial_path}$ {Colors.ENDC}").strip()

            # Re-check time after input (since input is blocking)
            if time.time() - start_time > duration:
                break

            if user_input in challenge.expected_command:
                print_success("正确！+10分")
                score += 10
                completed_count += 1
            elif user_input.lower() in ['exit', 'quit']:
                break
            else:
                print_error("错误！跳过此题...")

        print_header("⏰ 时间到！ ⏰")
        print_color(f"✨ 最终得分: {score} ✨", Colors.WARNING + Colors.BOLD)
        print_color(f"🎯 完成挑战数: {completed_count}", Colors.OKCYAN)

        self.check_achievement("time_attack_score", score)
        self.check_achievement("time_attack_completed", completed_count)

        input("\n按回车键返回主菜单...")

    def success(self, challenge: Challenge):
        print_success(challenge.success_msg)
        print_info(f"【知识点】{challenge.knowledge_point}")
        self.score += 10
        self.current_challenge_index += 1
        self.challenges_completed += 1
        self.check_achievement("complete_challenge")
        self.check_achievement("score")

        input("\n按回车键继续...")
        self.play_challenge()

    def handle_failure(self, user_input: str, attempts: int):
        self.errors_in_current_level += 1
        # 简单的命令模拟反馈
        if not user_input:
            return

        cmd_parts = user_input.split()
        cmd = cmd_parts[0]

        # 支持的命令列表
        supported_cmds = [
            'ls', 'cd', 'pwd', 'mkdir', 'touch', 'rm', 'cat', 'grep', 'cp', 'mv', 'chmod', 'whoami', 'ps', 'df', 'free',
            'cksum', 'diff', 'file', 'find', 'locate', 'ln', 'shred', 'tr', 'uniq', 'wc', 'cut', 'jq', 'stat', 'tree', 'dd',
            'ping', 'nc', 'wget', 'curl', 'traceroute', 'tar', 'uname', 'crontab',
            'gzip', 'zip', 'useradd', 'chown', 'sed', 'awk', 'which', 'alias', 'export', 'dmesg', 'lsmod', 'reboot', 'shutdown',
            'head', 'tail', 'sort', 'du', 'top', 'htop', 'ifconfig', 'ip', 'clear', 'history',
            'echo', 'printf', 'env', 'printenv', 'unset', 'readonly', 'declare',
            'bash', 'sh', 'source', '.',
            'expr', 'let', 'test', '[', '[[', '((',
            'if', 'else', 'elif', 'fi', 'case', 'esac',
            'for', 'while', 'until', 'do', 'done', 'break', 'continue',
            'function', 'return',
            'true', 'false',
            'iconv', 'fmt', 'split', 'dos2unix', 'unix2dos', 'uudecode', 'uuencode', 'spell', 'ispell', 'look', 'fold', 'paste', 'join', 'col', 'colrm',
            'ssh', 'scp', 'ftp', 'sftp', 'rsync', 'telnet', 'rlogin',
            'nslookup', 'dig', 'host', 'traceroute', 'mtr', 'whois',
            'netstat', 'ss', 'lsof', 'nmap',
            'route', 'nmcli', 'hostname', 'arp',
            'tcpdump',
            'wall', 'mail', 'mutt', 'write', 'mesg', 'talk',
            'useradd', 'userdel', 'usermod', 'groupadd', 'groupdel', 'passwd', 'id', 'who', 'w', 'last',
            'kill', 'killall', 'pkill', 'nice', 'renice', 'nohup', 'jobs', 'bg', 'fg',
            'fdisk', 'parted', 'mkfs', 'mkswap', 'swapon', 'swapoff', 'lsblk', 'blkid',
            'mount', 'umount', 'eject',
            'fsck', 'badblocks', 'tune2fs', 'dumpe2fs', 'sync',
            'crontab', 'at', 'batch',
            'vmstat', 'iostat', 'sar', 'dstat', 'glances', 'watch',
            'journalctl', 'logger', 'logrotate',
            'systemctl', 'service', 'chkconfig', 'init',
            'rpm', 'yum', 'dnf', 'apt', 'apt-get', 'dpkg',
            'modprobe', 'insmod', 'rmmod', 'depmod',
            'lscpu', 'lsusb', 'lspci', 'dmidecode',
            'sudo', 'visudo', 'su', 'lastb', 'auditd',
            'lp', 'lpr', 'lpq', 'lprm'
        ]

        # 模拟 Linux 常见错误
        if '=' in cmd and cmd not in supported_cmds:
            # 变量赋值，不报错
            pass
        elif cmd.startswith('./'):
            # 脚本执行，不报错
            pass
        elif cmd.startswith('(('):
            # 算术运算，不报错
            pass
        elif cmd not in supported_cmds:
            print_error(f"bash: {cmd}: 未找到命令")
            return # Don't simulate output if command not found

        # 即使不是正确答案，也显示一些模拟输出
        self.simulate_command_output(cmd, cmd_parts[1:] if len(cmd_parts) > 1 else [])
        print_warning(f"命令执行了，但似乎没有达到任务的目标。")

        if attempts >= 2:
            print_hint("输入 'hint' 获取提示。")

    def simulate_command_output(self, cmd: str, args: list):
        """为常用命令提供简单的模拟输出"""
        if cmd == 'pwd':
            print("/home/user")
        elif cmd == 'ls':
            print("documents  notes.txt  projects  README.md")
        elif cmd == 'whoami':
            print("linux-learner")
        elif cmd == 'df':
            print("Filesystem      Size  Used Avail Use% Mounted on")
            print("/dev/sda1        50G   20G   30G  40% /")
        elif cmd == 'ps':
            print("  PID TTY          TIME CMD")
            print("    1 pts/0    00:00:00 bash")
            print("   15 pts/0    00:00:00 ps")
        elif cmd == 'free':
            print("              total        used        free      shared  buff/cache   available")
            print("Mem:        8192000     2048000     4096000      102400     2048000     6144000")
        elif cmd == 'ping':
            print("PING google.com (142.250.190.46) 56(84) bytes of data.")
            print("64 bytes from hkg12s28-in-f14.1e100.net (142.250.190.46): icmp_seq=1 ttl=117 time=12.5 ms")
            print("64 bytes from hkg12s28-in-f14.1e100.net (142.250.190.46): icmp_seq=2 ttl=117 time=13.1 ms")
        elif cmd == 'wc':
            print("  2  5 36 article.txt")
        elif cmd == 'uname':
            print("Linux linux-game 5.15.0-generic #100-Ubuntu SMP Wed Jan 26 10:00:00 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux")
        elif cmd == 'tree':
            print(".")
            print("├── src")
            print("│   ├── main.py")
            print("│   └── utils.py")
            print("└── tests")
            print("    └── test_main.py")
        elif cmd == 'lsmod':
            print("Module                  Size  Used by")
            print("nls_utf8               16384  1")
            print("isofs                  49152  1")
        elif cmd == 'dmesg':
            print("[    0.000000] Linux version 5.15.0-generic ...")
            print("[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.15.0-generic ...")
        elif cmd == 'which':
            print(f"/usr/bin/{args[0] if args else 'cmd'}")
        elif cmd == 'reboot':
            print("System is going down for reboot NOW!")
        elif cmd == 'shutdown':
            print("Shutdown scheduled for ...")
        elif cmd == 'head':
            print("Line 1: This is the beginning of the file...")
            print("Line 2: ...")
            print("Line 3: ...")
        elif cmd == 'tail':
            print("Line 98: ...")
            print("Line 99: This is the end of the file.")
            print("Line 100: Footer info.")
        elif cmd == 'sort':
            print("Alice")
            print("Bob")
            print("Charlie")
            print("David")
        elif cmd == 'du':
            print("4.0K    ./config")
            print("12M     ./data")
            print("12M     .")
        elif cmd == 'top' or cmd == 'htop':
            print("top - 10:00:01 up 1 day,  1:00,  1 user,  load average: 0.00, 0.01, 0.05")
            print("Tasks: 100 total,   1 running,  99 sleeping,   0 stopped,   0 zombie")
            print("%Cpu(s):  0.5 us,  0.2 sy,  0.0 ni, 99.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st")
        elif cmd == 'ifconfig' or cmd == 'ip':
            print("eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500")
            print("        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255")
            print("        ether 00:11:22:33:44:55  txqueuelen 1000  (Ethernet)")
        elif cmd == 'clear':
            # 简单的模拟清屏
            print("\n" * 50)
        elif cmd == 'history':
            print("    1  ls")
            print("    2  cd Documents")
            print("    3  pwd")
            print("    4  history")
        elif cmd == 'cat':
             print("This is the content of the file.")
        elif cmd == 'grep':
             print("Found matches for pattern.")
        elif cmd == 'find':
             print("./found/file.txt")
        elif cmd == 'sed':
             print("This is the output after sed replacement.")
        elif cmd == 'awk':
             print("col1 col3")
             print("val1 val3")
        elif cmd == 'diff':
             print("1c1")
             print("< Hello")
             print("---")
             print("> Hello World")
        elif cmd == 'iconv':
             print("Converted content...")
        elif cmd == 'jq':
             print('"Trae"')
        elif cmd == 'fmt':
             print("This is a\nformatted\ntext.")
        elif cmd == 'split':
             print("Creating files: xaa, xab, xac...")
        elif cmd in ['wget', 'curl']:
             print("Downloading file...")
             print("100% [================================>] 10.5M  2.1MB/s    in 5s")
        elif cmd == 'ssh':
             print("admin@server1's password: ")
             print("Welcome to server1!")
        elif cmd in ['scp', 'rsync']:
             print("local.txt                               100%   12KB  12.0KB/s   00:00")
        elif cmd in ['nslookup', 'dig', 'host']:
             print("Server:     8.8.8.8")
             print("Address:    8.8.8.8#53")
             print("Non-authoritative answer:")
             print("Name:   google.com")
             print("Address: 142.250.190.46")
        elif cmd in ['traceroute', 'mtr']:
             print("traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets")
             print(" 1  gateway (192.168.1.1)  1.123 ms  1.098 ms  1.087 ms")
             print(" 2  10.10.10.1 (10.10.10.1)  2.345 ms  2.234 ms  2.123 ms")
             print(" 3  * * *")
        elif cmd in ['netstat', 'ss']:
             print("Active Internet connections (only servers)")
             print("Proto Recv-Q Send-Q Local Address           Foreign Address         State")
             print("tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN")
             print("tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN")
             print("tcp6       0      0 :::80                   :::*                    LISTEN")
        elif cmd in ['nc', 'nmap']:
             print("Connection to localhost 80 port [tcp/http] succeeded!")
        elif cmd in ['route', 'ip']:
             print("Kernel IP routing table")
             print("Destination     Gateway         Genmask         Flags Metric Ref    Use Iface")
             print("0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0")
             print("192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eth0")
        elif cmd == 'hostname':
             print("linux-learner")
        elif cmd == 'tcpdump':
             print("tcpdump: verbose output suppressed, use -v or -vv for full protocol decode")
             print("listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes")
             print("10:00:00.123456 IP 192.168.1.100.22 > 192.168.1.2.54321: Flags [P.], seq 1:50, ack 1, win 501, length 49")
             print("10:00:00.123567 IP 192.168.1.2.54321 > 192.168.1.100.22: Flags [.], ack 50, win 200, length 0")
        elif cmd in ['wall', 'write', 'mail']:
             print("Broadcast message from user@linux-learner (pts/0) (Sat Feb 26 10:00:00 2022):")
             print(f"{' '.join(args) if args else 'Message'}")
        elif cmd in ['useradd', 'adduser', 'groupadd']:
             pass # No output on success
        elif cmd == 'id':
             print("uid=1000(linux-learner) gid=1000(linux-learner) groups=1000(linux-learner),27(sudo)")
        elif cmd in ['who', 'w']:
             print("linux-learner pts/0        2022-02-26 10:00 (192.168.1.1)")
        elif cmd == 'last':
             print("linux-learner pts/0        192.168.1.1     Sat Feb 26 10:00   still logged in")
        elif cmd == 'jobs':
             print("[1]+  Running                 ./script.sh &")
        elif cmd in ['kill', 'killall', 'pkill']:
             pass # No output on success usually
        elif cmd == 'lsblk':
             print("NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT")
             print("sda      8:0    0   50G  0 disk")
             print("└─sda1   8:1    0   50G  0 part /")
             print("sdb      8:16   0   10G  0 disk")
             print("└─sdb1   8:17   0   10G  0 part")
        elif cmd in ['mount', 'umount']:
             pass
        elif cmd == 'fsck':
             print("fsck from util-linux 2.37.2")
             print("/dev/sdb1: clean, 11/655360 files, 26172/2621440 blocks")
        elif cmd == 'crontab':
             if '-e' in args:
                 print("crontab: installing new crontab")
        elif cmd == 'vmstat':
             print("procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----")
             print("r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st")
             print("1  0      0 354320  43210 987654    0    0     5    10   20   30  5  2 93  0  0")
        elif cmd == 'uptime':
             print(" 10:30:00 up 12 days,  2:30,  1 user,  load average: 0.05, 0.03, 0.01")
        elif cmd == 'journalctl':
             print("-- Logs begin at Sat 2022-02-26 10:00:00 UTC, end at Sat 2022-02-26 10:30:00 UTC. --")
             print("Feb 26 10:30:01 linux-learner systemd[1]: Started Session 1 of user linux-learner.")
        elif cmd in ['systemctl', 'service']:
             if 'status' in args:
                 print("● nginx.service - A high performance web server and a reverse proxy server")
                 print("     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)")
                 print("     Active: active (running) since Sat 2022-02-26 10:00:00 UTC; 30min ago")
             else:
                 pass
        elif cmd in ['apt', 'apt-get', 'yum', 'dnf']:
             print(f"Installing {args[-1] if args else 'package'}...")
             print("Setting up package (1.0-1) ...")
             print("Processing triggers for man-db (2.10.2-1) ...")
        elif cmd == 'lscpu':
             print("Architecture:            x86_64")
             print("  CPU op-mode(s):        32-bit, 64-bit")
             print("  Byte Order:            Little Endian")
             print("CPU(s):                  4")
             print("  On-line CPU(s) list:   0-3")
        elif cmd in ['su', 'sudo']:
             pass
        elif cmd == 'lastb':
             print("admin    ssh:notty    192.168.1.100    Sat Feb 26 10:05 - 10:05  (00:00)")
        elif cmd in ['lpq', 'lpstat']:
             print("no entries")
        elif cmd == 'echo':
            print(" ".join(args).replace('"', '').replace("'", ""))
        elif cmd == 'printf':
            if args:
                fmt = " ".join(args)
                print(fmt.replace('\\n', '\n').replace('\\t', '\t').replace('"', '').replace("'", ""))
        elif cmd in ['env', 'printenv']:
            print("USER=linux-learner")
            print("SHELL=/bin/bash")
            print("PATH=/usr/local/bin:/usr/bin:/bin")
            print("PWD=/home/user")
            print("TERM=xterm-256color")
        elif cmd == 'expr':
             try:
                 expr_str = " ".join(args)
                 allowed = set("0123456789+-*/%() ")
                 if set(expr_str).issubset(allowed):
                      print(eval(expr_str))
                 else:
                      print("expr: syntax error")
             except:
                 print("expr: syntax error")
        elif cmd in ['bash', 'sh'] and args:
             print(f"Executing script {args[0]}...")
        elif cmd in ['source', '.'] and args:
             print(f"Sourced {args[0]}")
        elif cmd.startswith('./'):
             print(f"Executing {cmd}...")
             if 'deploy.sh' in cmd:
                 print("Deploying application...")
                 print("Done.")

    def finish_level(self):
        print_success(f"恭喜！你完成了关卡 {self.current_level}！")

        # Check for perfect level completion
        if self.errors_in_current_level == 0:
            self.perfect_levels_count += 1
            self.check_achievement("perfect_level")

        # Check for level reach achievements
        self.check_achievement("level")

        if self.mode == 'story':
            self.current_level += 1
            self.save_progress()
            if self.current_level in LEVELS:
                input("\n按回车键进入下一关...")
                # self.start_level()  <-- Recursion removed
            else:
                self.game_over()
        else:
            input("\n按回车键返回菜单...")
            self.is_running = False

    def game_over(self):
        clear_screen()
        print_color("🎉 恭喜你通关了所有关卡！ 🎉", Colors.HEADER + Colors.BOLD)
        print_info(f"最终得分: {self.score}")
        print_color("你已经掌握了 Linux 的基础操作，继续在真实环境中探索吧！", Colors.OKGREEN)

        # Unlock Master Achievement
        self.check_achievement("all_levels")

        self.is_running = False
