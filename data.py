from dataclasses import dataclass
from typing import List, Optional, Callable, Dict, Any

@dataclass
class Challenge:
    id: int
    title: str
    description: str
    expected_command: List[str]  # 可能有多种正确写法
    hint: str
    success_msg: str
    knowledge_point: str
    initial_fs: Dict[str, Any]  # 模拟文件系统初始状态 (如: {"file1.txt": "content", "dir1": {}})
    initial_path: str = "/home/user"

# 关卡数据
LEVELS = {
    1: {
        "name": "初识 Linux",
        "challenges": [
            Challenge(
                id=101,
                title="我在哪？",
                description="显示当前工作目录的路径。",
                expected_command=["pwd"],
                hint="pwd 是 'print working directory' 的缩写。",
                success_msg="干得漂亮！你现在知道你在哪里了。",
                knowledge_point="pwd: 显示当前工作目录的绝对路径。",
                initial_fs={}
            ),
            Challenge(
                id=102,
                title="有什么？",
                description="列出当前目录下的所有文件和文件夹。",
                expected_command=["ls", "ls ."],
                hint="ls 是 'list' 的缩写，是最常用的命令之一。",
                success_msg="列表已显示。你可以看到目录里有什么了。",
                knowledge_point="ls: 列出目录内容。常用参数：-l (详细信息), -a (显示隐藏文件)。",
                initial_fs={"Documents": {}, "Downloads": {}, "notes.txt": "Remember to buy milk"}
            )
        ]
    },
    2: {
        "name": "穿越目录",
        "challenges": [
            Challenge(
                id=201,
                title="进入目录",
                description="进入 'Documents' 目录。",
                expected_command=["cd Documents", "cd ./Documents"],
                hint="cd 是 'change directory' 的缩写。",
                success_msg="成功进入！注意提示符的变化。",
                knowledge_point="cd: 切换当前工作目录。",
                initial_fs={"Documents": {"work.txt": "Work stuff"}, "Downloads": {}}
            ),
            Challenge(
                id=202,
                title="返回上级",
                description="返回上一级目录。",
                expected_command=["cd ..", "cd ../"],
                hint=".. 代表上一级目录，. 代表当前目录。",
                success_msg="成功返回！",
                knowledge_point=".. (点点) 表示父目录。",
                initial_fs={"Documents": {}, "Downloads": {}},
                initial_path="/home/user/Documents"
            )
        ]
    },
    3: {
        "name": "文件创造者",
        "challenges": [
            Challenge(
                id=301,
                title="创建文件",
                description="创建一个名为 'new_file.txt' 的空文件。",
                expected_command=["touch new_file.txt"],
                hint="touch 命令可以创建空文件或更新文件的时间戳。",
                success_msg="文件已创建！",
                knowledge_point="touch: 创建空文件或修改文件时间戳。",
                initial_fs={}
            ),
            Challenge(
                id=302,
                title="创建目录",
                description="创建一个名为 'projects' 的新目录。",
                expected_command=["mkdir projects"],
                hint="mkdir 是 'make directory' 的缩写。",
                success_msg="目录创建成功！",
                knowledge_point="mkdir: 创建新目录。-p 参数可以创建多级目录。",
                initial_fs={}
            )
        ]
    },
    4: {
        "name": "清理门户",
        "challenges": [
            Challenge(
                id=401,
                title="删除文件",
                description="删除名为 'old.txt' 的文件。",
                expected_command=["rm old.txt"],
                hint="rm 是 'remove' 的缩写。小心使用！",
                success_msg="文件已删除。",
                knowledge_point="rm: 删除文件。删除目录需加 -r 参数。",
                initial_fs={"old.txt": "useless content", "keep.txt": "important"}
            ),
            Challenge(
                id=402,
                title="删除目录",
                description="删除名为 'temp_dir' 的空目录。",
                expected_command=["rmdir temp_dir", "rm -r temp_dir", "rm -rf temp_dir"],
                hint="rmdir 只能删除空目录，rm -r 可以删除非空目录。",
                success_msg="目录已清理。",
                knowledge_point="rmdir: 删除空目录。rm -r: 递归删除目录及其内容。",
                initial_fs={"temp_dir": {}}
            )
        ]
    },
    5: {
        "name": "复制粘贴",
        "challenges": [
            Challenge(
                id=501,
                title="备份文件",
                description="将 'data.txt' 复制为 'data.bak'。",
                expected_command=["cp data.txt data.bak"],
                hint="cp [源文件] [目标文件]。",
                success_msg="备份完成！",
                knowledge_point="cp: 复制文件或目录。-r 用于复制目录。",
                initial_fs={"data.txt": "important data"}
            )
        ]
    },
    6: {
        "name": "移动与重命名",
        "challenges": [
            Challenge(
                id=601,
                title="重命名",
                description="将 'wrong_name.txt' 重命名为 'right_name.txt'。",
                expected_command=["mv wrong_name.txt right_name.txt"],
                hint="mv 命令既可以移动文件，也可以重命名文件。",
                success_msg="更名成功！",
                knowledge_point="mv: 移动或重命名文件。",
                initial_fs={"wrong_name.txt": "content"}
            ),
            Challenge(
                id=602,
                title="归档",
                description="将 'file.txt' 移动到 'archive' 目录中。",
                expected_command=["mv file.txt archive/", "mv file.txt archive"],
                hint="mv [源文件] [目标目录]。",
                success_msg="文件已归档。",
                knowledge_point="mv 也可以将文件移动到指定目录。",
                initial_fs={"file.txt": "old stuff", "archive": {}}
            )
        ]
    },
    7: {
        "name": "查看内容",
        "challenges": [
            Challenge(
                id=701,
                title="猫眼看世界",
                description="显示 'readme.txt' 的全部内容。",
                expected_command=["cat readme.txt"],
                hint="cat 是 'concatenate' 的缩写，常用于查看短文件。",
                success_msg="内容已显示。",
                knowledge_point="cat: 连接文件并打印到标准输出。",
                initial_fs={"readme.txt": "Hello Linux World!\nThis is a test file."}
            ),
            Challenge(
                id=702,
                title="只看头",
                description="查看 'long_log.txt' 的前 5 行。",
                expected_command=["head -n 5 long_log.txt", "head -5 long_log.txt"],
                hint="head 默认显示前 10 行，使用 -n 指定行数。",
                success_msg="头部信息已获取。",
                knowledge_point="head: 输出文件的开头部分。",
                initial_fs={"long_log.txt": "line 1\nline 2\nline 3\nline 4\nline 5\nline 6\nline 7"}
            ),
            Challenge(
                id=703,
                title="只看尾",
                description="查看 'long_log.txt' 的最后 3 行。",
                expected_command=["tail -n 3 long_log.txt", "tail -3 long_log.txt"],
                hint="tail 常用于查看最新的日志信息。",
                success_msg="尾部信息已获取。",
                knowledge_point="tail: 输出文件的结尾部分。-f 参数可实时追踪文件更新。",
                initial_fs={"long_log.txt": "line 1\nline 2\nline 3\nline 4\nline 5\nline 6\nline 7"}
            )
        ]
    },
    8: {
        "name": "搜索内容",
        "challenges": [
            Challenge(
                id=801,
                title="关键词搜索",
                description="在 'server.log' 中搜索包含 'ERROR' 的行。",
                expected_command=["grep ERROR server.log", "grep 'ERROR' server.log", "grep \"ERROR\" server.log"],
                hint="grep 是全局正则表达式打印 (Global Regular Expression Print) 的缩写。",
                success_msg="错误日志已定位。",
                knowledge_point="grep: 强大的文本搜索工具。常用参数：-i (忽略大小写), -v (反向匹配), -r (递归搜索)。",
                initial_fs={"server.log": "INFO: server started\nERROR: connection failed\nINFO: retry..."}
            )
        ]
    },
    9: {
        "name": "查找文件",
        "challenges": [
            Challenge(
                id=901,
                title="按名查找",
                description="在当前目录及子目录中查找所有以 '.py' 结尾的文件。",
                expected_command=["find . -name *.py", "find . -name \"*.py\"", "find . -name '*.py'"],
                hint="find [路径] -name [模式]。",
                success_msg="文件已找到。",
                knowledge_point="find: 在目录层次结构中搜索文件。功能极其强大。",
                initial_fs={"script.py": "", "src": {"main.py": "", "utils.c": ""}}
            ),
            Challenge(
                id=902,
                title="命令位置",
                description="查找 'python' 命令的可执行文件路径。",
                expected_command=["which python"],
                hint="which 命令会在 PATH 环境变量中搜索。",
                success_msg="路径已显示。",
                knowledge_point="which: 显示命令的绝对路径。",
                initial_fs={}
            )
        ]
    },
    10: {
        "name": "权限管理",
        "challenges": [
            Challenge(
                id=1001,
                title="赋予执行权",
                description="给 'script.sh' 增加可执行权限。",
                expected_command=["chmod +x script.sh", "chmod 755 script.sh"],
                hint="chmod +x 是最常用的赋予执行权限的方式。",
                success_msg="权限已修改，现在可以运行脚本了。",
                knowledge_point="chmod: 改变文件模式位。u/g/o (user/group/others) +/-/= r/w/x。",
                initial_fs={"script.sh": "#!/bin/bash\necho hello"}
            ),
            Challenge(
                id=1002,
                title="更改所有者",
                description="将 'database.db' 的所有者改为 'dbadmin'。",
                expected_command=["chown dbadmin database.db", "sudo chown dbadmin database.db"],
                hint="chown [用户] [文件]。",
                success_msg="所有者已变更。",
                knowledge_point="chown: 改变文件所有者和组。",
                initial_fs={"database.db": "data"}
            )
        ]
    },
    11: {
        "name": "链接与别名",
        "challenges": [
            Challenge(
                id=1101,
                title="创建软链接",
                description="为 'target.txt' 创建一个名为 'link.txt' 的软链接。",
                expected_command=["ln -s target.txt link.txt"],
                hint="ln -s [源文件] [链接名]。不加 -s 会创建硬链接。",
                success_msg="链接已创建。软链接就像 Windows 的快捷方式。",
                knowledge_point="ln: 创建链接。-s (symbolic) 创建符号链接。",
                initial_fs={"target.txt": "content"}
            ),
            Challenge(
                id=1102,
                title="命令别名",
                description="创建一个别名 'c'，使其等同于 'clear' 命令。",
                expected_command=["alias c=clear", "alias c='clear'"],
                hint="alias 别名=命令。",
                success_msg="别名已设置。以后输入 c 就能清屏了。",
                knowledge_point="alias: 设置指令的别名。",
                initial_fs={}
            )
        ]
    },
    12: {
        "name": "文本处理基础",
        "challenges": [
            Challenge(
                id=1201,
                title="行数统计",
                description="统计 'article.txt' 有多少行。",
                expected_command=["wc -l article.txt"],
                hint="wc 是 'word count' 的缩写，-l 统计行数。",
                success_msg="统计完成。",
                knowledge_point="wc: 统计文件的字节数、字数、行数。",
                initial_fs={"article.txt": "Line 1\nLine 2\nLine 3"}
            ),
            Challenge(
                id=1202,
                title="排序",
                description="将 'names.txt' 的内容按字母顺序排序并输出。",
                expected_command=["sort names.txt"],
                hint="sort 命令默认按 ASCII 码排序。",
                success_msg="排序完成。",
                knowledge_point="sort: 对文本文件的行进行排序。-r (逆序), -n (数值排序)。",
                initial_fs={"names.txt": "Charlie\nAlice\nBob"}
            )
        ]
    },
    13: {
        "name": "文本编辑神器",
        "challenges": [
            Challenge(
                id=1301,
                title="流编辑替换",
                description="使用 sed 将 'config.ini' 中的 'debug=false' 替换为 'debug=true' 并输出。",
                expected_command=["sed 's/debug=false/debug=true/' config.ini", "sed s/debug=false/debug=true/ config.ini"],
                hint="sed 's/旧/新/' 文件名。",
                success_msg="替换成功。sed 是自动化修改配置文件的利器。",
                knowledge_point="sed: 流编辑器。s (substitute) 命令用于替换。",
                initial_fs={"config.ini": "port=80\ndebug=false\nlog=on"}
            )
        ]
    },
    14: {
        "name": "压缩与解压",
        "challenges": [
            Challenge(
                id=1401,
                title="打包压缩",
                description="将 'logs' 目录打包并压缩为 'logs.tar.gz'。",
                expected_command=["tar -czf logs.tar.gz logs/", "tar -czf logs.tar.gz logs"],
                hint="tar -czf [压缩包名] [目录]。c:创建, z:gzip, f:文件。",
                success_msg="打包完成。",
                knowledge_point="tar: Linux 下最常用的归档工具。",
                initial_fs={"logs": {"app.log": "", "error.log": ""}}
            ),
            Challenge(
                id=1402,
                title="Gzip 压缩",
                description="使用 gzip 压缩 'large_file.txt'。",
                expected_command=["gzip large_file.txt"],
                hint="gzip 会直接压缩文件并添加 .gz 后缀。",
                success_msg="文件已压缩。",
                knowledge_point="gzip: 压缩文件。gunzip 用于解压。",
                initial_fs={"large_file.txt": "very large content..."}
            )
        ]
    },
    15: {
        "name": "磁盘查看",
        "challenges": [
            Challenge(
                id=1501,
                title="磁盘空间",
                description="以人类可读的格式(GB/MB)显示磁盘空间使用情况。",
                expected_command=["df -h"],
                hint="df (disk free) 显示文件系统磁盘空间使用情况。",
                success_msg="信息已显示。",
                knowledge_point="df: 报告文件系统磁盘空间的使用情况。-h (human-readable)。",
                initial_fs={}
            ),
            Challenge(
                id=1502,
                title="目录大小",
                description="显示当前目录下 'data' 文件夹的总大小。",
                expected_command=["du -sh data", "du -sh data/"],
                hint="du (disk usage) 统计文件和目录的磁盘占用量。-s (summary) 仅显示总计。",
                success_msg="大小已统计。",
                knowledge_point="du: 估算文件空间使用量。",
                initial_fs={"data": {"file1": "...", "file2": "..."}}
            )
        ]
    },
    16: {
        "name": "进程查看",
        "challenges": [
            Challenge(
                id=1601,
                title="进程快照",
                description="显示当前所有运行的进程。",
                expected_command=["ps -ef", "ps aux", "ps"],
                hint="ps (process status) 显示当前进程的快照。",
                success_msg="进程列表已显示。",
                knowledge_point="ps: 报告当前进程的快照。aux 或 -ef 是常用参数组合。",
                initial_fs={}
            ),
            Challenge(
                id=1602,
                title="实时监控",
                description="启动实时进程监控工具。",
                expected_command=["top", "htop"],
                hint="top 命令可以动态显示进程信息，按 q 退出。",
                success_msg="监控已启动（模拟）。",
                knowledge_point="top: 实时显示系统中各个进程的资源占用状况。",
                initial_fs={}
            )
        ]
    },
    17: {
        "name": "简单网络",
        "challenges": [
            Challenge(
                id=1701,
                title="网络连通性",
                description="测试与 google.com 的网络连通性。",
                expected_command=["ping google.com", "ping -c 4 google.com"],
                hint="ping 发送 ICMP 回显请求检测主机是否可达。",
                success_msg="网络通畅。",
                knowledge_point="ping: 测试主机之间网络的连通性。",
                initial_fs={}
            ),
            Challenge(
                id=1702,
                title="网络接口",
                description="显示所有网络接口的配置信息。",
                expected_command=["ifconfig", "ip addr", "ip a"],
                hint="ifconfig 或 ip addr 可以查看 IP 地址。",
                success_msg="配置已显示。",
                knowledge_point="ifconfig: 配置网络接口。ip: 显示/操作路由、设备、策略路由和隧道。",
                initial_fs={}
            )
        ]
    },
    18: {
        "name": "Hello Shell",
        "challenges": [
            Challenge(
                id=1801,
                title="打印问候",
                description="向屏幕输出 'Hello World'。",
                expected_command=["echo Hello World", "echo 'Hello World'", "echo \"Hello World\""],
                hint="echo [字符串]",
                success_msg="成功打印！这是编程世界的第一步。",
                knowledge_point="echo: 在终端输出字符串或变量的值。",
                initial_fs={}
            ),
            Challenge(
                id=1802,
                title="格式化输出",
                description="使用 printf 输出 'Name: Linux\\n' (注意换行符)。",
                expected_command=["printf \"Name: Linux\\n\"", "printf 'Name: Linux\\n'"],
                hint="printf \"格式字符串\" [参数...]",
                success_msg="格式化输出完成。",
                knowledge_point="printf: 格式化打印数据，支持 C 语言风格的格式控制符。",
                initial_fs={}
            )
        ]
    },
    19: {
        "name": "变量的世界",
        "challenges": [
            Challenge(
                id=1901,
                title="定义变量",
                description="定义一个名为 name 的变量，值为 'Trae'，然后输出它。",
                expected_command=["name=Trae; echo $name", "name='Trae'; echo $name", "name=\"Trae\"; echo $name"],
                hint="变量名=值 (等号两边不能有空格); echo $变量名",
                success_msg="变量定义并输出成功。",
                knowledge_point="变量定义：name=value。变量引用：$name 或 ${name}。",
                initial_fs={}
            ),
            Challenge(
                id=1902,
                title="环境变量",
                description="查看当前所有的环境变量。",
                expected_command=["env", "printenv"],
                hint="env 或 printenv 命令。",
                success_msg="环境变量列表已显示。",
                knowledge_point="env: 显示当前用户的环境变量。",
                initial_fs={}
            )
        ]
    },
    20: {
        "name": "参数传递",
        "challenges": [
            Challenge(
                id=2001,
                title="脚本参数",
                description="假设有一个脚本 'test.sh'，模拟执行它并传递参数 'arg1'。",
                expected_command=["./test.sh arg1", "bash test.sh arg1", "sh test.sh arg1"],
                hint="./脚本名 参数1 参数2 ...",
                success_msg="脚本执行并接收参数成功。",
                knowledge_point="$0: 脚本名, $1: 第一个参数, $#: 参数个数。",
                initial_fs={"test.sh": "#!/bin/bash\necho $1"}
            )
        ]
    },
    21: {
        "name": "数组操作",
        "challenges": [
            Challenge(
                id=2101,
                title="定义数组",
                description="定义一个包含 1, 2, 3 的数组 arr，并输出第一个元素。",
                expected_command=["arr=(1 2 3); echo ${arr[0]}", "arr=(1 2 3); echo ${arr[0]}"],
                hint="arr=(v1 v2 v3); echo ${arr[0]}",
                success_msg="数组操作成功。",
                knowledge_point="数组定义：arr=(v1 v2)。访问：${arr[index]}。所有元素：${arr[@]}。",
                initial_fs={}
            )
        ]
    },
    22: {
        "name": "算术运算",
        "challenges": [
            Challenge(
                id=2201,
                title="简单加法",
                description="计算 10 + 20 的结果并输出。",
                expected_command=["echo $((10+20))", "expr 10 + 20", "let res=10+20; echo $res"],
                hint="echo $((a+b)) 或 expr a + b",
                success_msg="计算正确。",
                knowledge_point="$((expression)) 是推荐的算术运算方式。",
                initial_fs={}
            )
        ]
    },
    23: {
        "name": "条件测试",
        "challenges": [
            Challenge(
                id=2301,
                title="文件存在测试",
                description="测试 'config.txt' 文件是否存在。",
                expected_command=["[ -f config.txt ]", "test -f config.txt", "[[ -f config.txt ]]"],
                hint="[ -f 文件名 ]",
                success_msg="测试完成（返回状态码 0 表示存在）。",
                knowledge_point="[ ]: 测试命令。-f: 文件存在且为普通文件。-d: 目录存在。",
                initial_fs={"config.txt": "settings"}
            )
        ]
    },
    24: {
        "name": "流程控制：选择",
        "challenges": [
            Challenge(
                id=2401,
                title="If 判断",
                description="编写一个单行 if 语句：如果 'lock' 文件存在，则输出 'Locked'。",
                expected_command=["if [ -f lock ]; then echo Locked; fi", "[ -f lock ] && echo Locked"],
                hint="if [ 条件 ]; then 命令; fi",
                success_msg="逻辑判断正确。",
                knowledge_point="if 语句结构：if condition; then commands; fi。",
                initial_fs={"lock": ""}
            )
        ]
    },
    25: {
        "name": "流程控制：循环",
        "challenges": [
            Challenge(
                id=2501,
                title="For 循环",
                description="使用 for 循环输出 1 到 3。",
                expected_command=["for i in 1 2 3; do echo $i; done", "for i in {1..3}; do echo $i; done"],
                hint="for var in list; do commands; done",
                success_msg="循环执行完毕。",
                knowledge_point="for 循环用于遍历列表或范围。",
                initial_fs={}
            )
        ]
    },
    26: {
        "name": "函数封装",
        "challenges": [
            Challenge(
                id=2601,
                title="定义函数",
                description="定义一个名为 greet 的函数，输出 'Hi'，并调用它。",
                expected_command=["function greet() { echo Hi; }; greet", "greet() { echo Hi; }; greet"],
                hint="function name() { cmds; }; name",
                success_msg="函数定义及调用成功。",
                knowledge_point="函数定义：function name() { ... }。调用时直接写函数名。",
                initial_fs={}
            )
        ]
    },
    27: {
        "name": "输入输出重定向",
        "challenges": [
            Challenge(
                id=2701,
                title="输出重定向",
                description="将 'Hello' 写入到 'output.txt' 中（覆盖）。",
                expected_command=["echo Hello > output.txt", "echo 'Hello' > output.txt"],
                hint="命令 > 文件",
                success_msg="写入成功。",
                knowledge_point=">: 重定向输出（覆盖）。>>: 重定向输出（追加）。",
                initial_fs={}
            ),
            Challenge(
                id=2702,
                title="追加重定向",
                description="将 'World' 追加到 'output.txt' 末尾。",
                expected_command=["echo World >> output.txt", "echo 'World' >> output.txt"],
                hint="命令 >> 文件",
                success_msg="追加成功。",
                knowledge_point=">> 用于在文件末尾追加内容而不覆盖原有内容。",
                initial_fs={"output.txt": "Hello"}
            )
        ]
    },
    28: {
        "name": "管道与过滤器",
        "challenges": [
            Challenge(
                id=2801,
                title="管道连接",
                description="显示 'data.txt' 的内容，并将结果通过管道传递给 grep 搜索 'error'。",
                expected_command=["cat data.txt | grep error", "cat data.txt | grep 'error'"],
                hint="命令1 | 命令2",
                success_msg="管道操作成功。",
                knowledge_point="| (管道): 将前一个命令的输出作为后一个命令的输入。",
                initial_fs={"data.txt": "info line\nerror line\nwarning line"}
            )
        ]
    },
    29: {
        "name": "文件包含",
        "challenges": [
            Challenge(
                id=2901,
                title="Source 引入",
                description="在当前 Shell 中执行/引入 'env.sh' 脚本。",
                expected_command=["source env.sh", ". env.sh"],
                hint="source 脚本名 或 . 脚本名",
                success_msg="环境配置已加载。",
                knowledge_point="source (或 .): 在当前 Shell 环境中读取并执行脚本，常用于加载配置。",
                initial_fs={"env.sh": "export PATH=$PATH:/opt/bin"}
            )
        ]
    },
    30: {
        "name": "综合脚本挑战",
        "challenges": [
            Challenge(
                id=3001,
                title="执行脚本",
                description="赋予 'deploy.sh' 执行权限并运行它。",
                expected_command=["chmod +x deploy.sh; ./deploy.sh", "chmod +x deploy.sh && ./deploy.sh"],
                hint="chmod +x ...; ./...",
                success_msg="部署脚本执行成功！",
                knowledge_point="组合命令：使用 ; 或 && 连接多个命令。",
                initial_fs={"deploy.sh": "#!/bin/bash\necho Deploying..."}
            )
        ]
    },
    31: {
        "name": "流编辑器进阶",
        "challenges": [
            Challenge(
                id=3101,
                title="Sed 替换",
                description="使用 sed 将 'file.txt' 中的所有 'apple' 替换为 'orange' 并输出。",
                expected_command=["sed 's/apple/orange/g' file.txt", "sed \"s/apple/orange/g\" file.txt"],
                hint="sed 's/旧/新/g' 文件名",
                success_msg="文本替换成功。",
                knowledge_point="sed: 流编辑器，s/old/new/g 用于全局替换。",
                initial_fs={"file.txt": "apple pie\napple juice\nbanana"}
            )
        ]
    },
    32: {
        "name": "文本分析专家",
        "challenges": [
            Challenge(
                id=3201,
                title="Awk 打印列",
                description="使用 awk 打印 'data.csv' 的第 1 列和第 3 列。",
                expected_command=["awk '{print $1, $3}' data.csv", "awk '{print $1,$3}' data.csv"],
                hint="awk '{print $1, $3}' 文件名",
                success_msg="列数据提取成功。",
                knowledge_point="awk: 强大的文本分析工具。默认以空格分隔，print $N 打印第 N 列。",
                initial_fs={"data.csv": "Name Age City\nAlice 25 NY\nBob 30 LA"}
            )
        ]
    },
    33: {
        "name": "文件差异",
        "challenges": [
            Challenge(
                id=3301,
                title="比较差异",
                description="比较 'v1.txt' 和 'v2.txt' 两个文件的差异。",
                expected_command=["diff v1.txt v2.txt", "diff -u v1.txt v2.txt"],
                hint="diff 文件1 文件2",
                success_msg="差异已显示。",
                knowledge_point="diff: 比较文件内容差异。-u 输出统一格式。",
                initial_fs={"v1.txt": "Hello", "v2.txt": "Hello World"}
            )
        ]
    },
    34: {
        "name": "格式转换",
        "challenges": [
            Challenge(
                id=3401,
                title="编码转换",
                description="使用 iconv 将 'gbk.txt' 从 GBK 转换为 UTF-8。",
                expected_command=["iconv -f GBK -t UTF-8 gbk.txt", "iconv -f gbk -t utf-8 gbk.txt"],
                hint="iconv -f 源编码 -t 目标编码 文件",
                success_msg="编码转换完成。",
                knowledge_point="iconv: 字符编码转换工具。",
                initial_fs={"gbk.txt": "..."}
            )
        ]
    },
    35: {
        "name": "JSON 处理",
        "challenges": [
            Challenge(
                id=3501,
                title="解析 JSON",
                description="使用 jq 从 'data.json' 中提取 'name' 字段。",
                expected_command=["jq '.name' data.json", "jq .name data.json", "cat data.json | jq '.name'"],
                hint="jq '.字段名' 文件名",
                success_msg="JSON 数据提取成功。",
                knowledge_point="jq: 轻量级且灵活的命令行 JSON 处理器。",
                initial_fs={"data.json": "{\"name\": \"Trae\", \"role\": \"AI\"}"}
            )
        ]
    },
    36: {
        "name": "拼写与格式",
        "challenges": [
            Challenge(
                id=3601,
                title="文本折行",
                description="使用 fmt 格式化 'long.txt'，使其宽度不超过 10 个字符。",
                expected_command=["fmt -w 10 long.txt", "fmt -10 long.txt"],
                hint="fmt -w 宽度 文件名",
                success_msg="文本格式化完成。",
                knowledge_point="fmt: 简单的文本格式化工具，常用于调整段落宽度。",
                initial_fs={"long.txt": "This is a very long line that needs formatting."}
            )
        ]
    },
    37: {
        "name": "分割与合并",
        "challenges": [
            Challenge(
                id=3701,
                title="文件分割",
                description="使用 split 将 'large.log' 按每 2 行分割成小文件。",
                expected_command=["split -l 2 large.log", "split -l 2 large.log x"],
                hint="split -l 行数 文件名",
                success_msg="文件分割成功。",
                knowledge_point="split: 将文件分割成多个小文件。",
                initial_fs={"large.log": "line1\nline2\nline3\nline4\nline5"}
            )
        ]
    },
    38: {
        "name": "下载工具",
        "challenges": [
            Challenge(
                id=3801,
                title="文件下载",
                description="使用 wget 下载 'http://example.com/file.zip'。",
                expected_command=["wget http://example.com/file.zip", "curl -O http://example.com/file.zip"],
                hint="wget URL",
                success_msg="文件下载完成。",
                knowledge_point="wget: 非交互式网络下载器。curl -O: 下载文件并保存。",
                initial_fs={}
            ),
            Challenge(
                id=3802,
                title="API 测试",
                description="使用 curl 发送 GET 请求到 'http://api.example.com/status'。",
                expected_command=["curl http://api.example.com/status", "curl -X GET http://api.example.com/status"],
                hint="curl URL",
                success_msg="请求发送成功。",
                knowledge_point="curl: 强大的数据传输工具，支持多种协议。",
                initial_fs={}
            )
        ]
    },
    39: {
        "name": "远程登录",
        "challenges": [
            Challenge(
                id=3901,
                title="SSH 登录",
                description="模拟使用 ssh 登录到 'server1' (用户: admin)。",
                expected_command=["ssh admin@server1", "ssh -l admin server1"],
                hint="ssh 用户名@主机名",
                success_msg="连接已建立（模拟）。",
                knowledge_point="ssh: 安全外壳协议，用于远程登录和执行命令。",
                initial_fs={}
            )
        ]
    },
    40: {
        "name": "文件传输",
        "challenges": [
            Challenge(
                id=4001,
                title="SCP 传输",
                description="将本地文件 'local.txt' 复制到远程主机 'server1' 的 '/tmp' 目录。",
                expected_command=["scp local.txt server1:/tmp", "scp local.txt admin@server1:/tmp"],
                hint="scp 本地文件 远程主机:路径",
                success_msg="文件传输完成。",
                knowledge_point="scp: 基于 SSH 的安全文件复制。",
                initial_fs={"local.txt": "content"}
            )
        ]
    },
    41: {
        "name": "网络诊断",
        "challenges": [
            Challenge(
                id=4101,
                title="域名解析",
                description="查询 'google.com' 的 IP 地址。",
                expected_command=["nslookup google.com", "dig google.com", "host google.com"],
                hint="nslookup 域名 或 dig 域名",
                success_msg="解析结果已显示。",
                knowledge_point="nslookup/dig: 查询 DNS 记录。",
                initial_fs={}
            ),
            Challenge(
                id=4102,
                title="路由追踪",
                description="追踪到达 '8.8.8.8' 的网络路径。",
                expected_command=["traceroute 8.8.8.8", "mtr 8.8.8.8"],
                hint="traceroute IP地址",
                success_msg="路径追踪完成。",
                knowledge_point="traceroute: 显示数据包到达目标主机所经过的路由。",
                initial_fs={}
            )
        ]
    },
    42: {
        "name": "端口与连接",
        "challenges": [
            Challenge(
                id=4201,
                title="端口监听",
                description="查看当前系统监听的所有 TCP 端口。",
                expected_command=["netstat -tuln", "ss -tuln", "netstat -an | grep LISTEN"],
                hint="netstat -tuln 或 ss -tuln",
                success_msg="监听端口列表已显示。",
                knowledge_point="netstat/ss: 查看网络连接、路由表、接口统计等。-tuln: TCP, UDP, Listening, Numeric.",
                initial_fs={}
            ),
            Challenge(
                id=4202,
                title="端口扫描",
                description="使用 nc 扫描 'localhost' 的 80 端口是否开放。",
                expected_command=["nc -zv localhost 80", "nc -z localhost 80"],
                hint="nc -zv 主机 端口",
                success_msg="扫描完成。",
                knowledge_point="nc (netcat): 网络工具瑞士军刀。-z: 扫描模式，不发送数据。",
                initial_fs={}
            )
        ]
    },
    43: {
        "name": "网络配置",
        "challenges": [
            Challenge(
                id=4301,
                title="查看路由",
                description="显示系统的路由表。",
                expected_command=["route -n", "ip route", "netstat -r"],
                hint="route -n 或 ip route",
                success_msg="路由表已显示。",
                knowledge_point="route/ip route: 显示或管理 IP 路由表。",
                initial_fs={}
            ),
            Challenge(
                id=4302,
                title="主机名",
                description="查看当前主机的主机名。",
                expected_command=["hostname", "uname -n"],
                hint="hostname",
                success_msg="主机名：linux-learner",
                knowledge_point="hostname: 显示或设置系统的主机名。",
                initial_fs={}
            )
        ]
    },
    44: {
        "name": "抓包分析",
        "challenges": [
            Challenge(
                id=4401,
                title="TCPDump",
                description="抓取 'eth0' 接口上的前 5 个数据包。",
                expected_command=["tcpdump -i eth0 -c 5", "tcpdump -c 5 -i eth0"],
                hint="tcpdump -i 接口 -c 数量",
                success_msg="抓包完成。",
                knowledge_point="tcpdump: 强大的命令行数据包分析工具。",
                initial_fs={}
            )
        ]
    },
    45: {
        "name": "邮件与消息",
        "challenges": [
            Challenge(
                id=4501,
                title="发送广播",
                description="向所有登录用户发送广播消息 'Server maintenance soon'。",
                expected_command=["wall 'Server maintenance soon'", "wall \"Server maintenance soon\""],
                hint="wall 消息内容",
                success_msg="广播已发送。",
                knowledge_point="wall: 向所有终端用户发送广播消息。",
                initial_fs={}
            )
        ]
    },
    46: {
        "name": "用户与组管理",
        "challenges": [
            Challenge(
                id=4601,
                title="创建用户",
                description="创建一个名为 'newuser' 的新用户。",
                expected_command=["useradd newuser", "adduser newuser"],
                hint="useradd 用户名",
                success_msg="用户创建成功。",
                knowledge_point="useradd: 创建新用户账号。",
                initial_fs={}
            ),
            Challenge(
                id=4602,
                title="查看用户信息",
                description="查看当前用户的 UID 和 GID 信息。",
                expected_command=["id", "id linux-learner"],
                hint="id [用户名]",
                success_msg="用户信息已显示。",
                knowledge_point="id: 显示真实和有效的用户ID(UID)和组ID(GID)。",
                initial_fs={}
            )
        ]
    },
    47: {
        "name": "进程管理",
        "challenges": [
            Challenge(
                id=4701,
                title="查看后台任务",
                description="查看当前终端的后台任务列表。",
                expected_command=["jobs", "jobs -l"],
                hint="jobs",
                success_msg="后台任务列表已显示。",
                knowledge_point="jobs: 显示作业的状态。",
                initial_fs={}
            ),
            Challenge(
                id=4702,
                title="终止进程",
                description="强制终止 PID 为 1234 的进程。",
                expected_command=["kill -9 1234", "kill -SIGKILL 1234"],
                hint="kill -9 PID",
                success_msg="进程已终止。",
                knowledge_point="kill: 发送信号到进程。-9 (SIGKILL) 强制终止。",
                initial_fs={}
            )
        ]
    },
    48: {
        "name": "磁盘分区与格式化",
        "challenges": [
            Challenge(
                id=4801,
                title="查看块设备",
                description="列出所有块设备的信息。",
                expected_command=["lsblk", "lsblk -a"],
                hint="lsblk",
                success_msg="块设备列表已显示。",
                knowledge_point="lsblk: 列出所有可用块设备的信息。",
                initial_fs={}
            ),
            Challenge(
                id=4802,
                title="格式化文件系统",
                description="将 '/dev/sdb1' 格式化为 ext4 文件系统。",
                expected_command=["mkfs.ext4 /dev/sdb1", "mkfs -t ext4 /dev/sdb1"],
                hint="mkfs.ext4 设备名",
                success_msg="格式化完成。",
                knowledge_point="mkfs: 在设备上创建文件系统。",
                initial_fs={}
            )
        ]
    },
    49: {
        "name": "挂载管理",
        "challenges": [
            Challenge(
                id=4901,
                title="挂载设备",
                description="将 '/dev/sdb1' 挂载到 '/mnt/data' 目录。",
                expected_command=["mount /dev/sdb1 /mnt/data"],
                hint="mount 设备 挂载点",
                success_msg="挂载成功。",
                knowledge_point="mount: 挂载文件系统。",
                initial_fs={}
            ),
            Challenge(
                id=4902,
                title="卸载设备",
                description="卸载 '/mnt/data'。",
                expected_command=["umount /mnt/data", "umount /dev/sdb1"],
                hint="umount 挂载点或设备",
                success_msg="卸载成功。",
                knowledge_point="umount: 卸载文件系统。",
                initial_fs={}
            )
        ]
    },
    50: {
        "name": "磁盘维护",
        "challenges": [
            Challenge(
                id=5001,
                title="文件系统检查",
                description="检查 '/dev/sdb1' 文件系统的完整性。",
                expected_command=["fsck /dev/sdb1", "e2fsck /dev/sdb1"],
                hint="fsck 设备名",
                success_msg="检查完成，未发现错误。",
                knowledge_point="fsck: 检查并修复 Linux 文件系统。",
                initial_fs={}
            )
        ]
    },
    51: {
        "name": "计划任务",
        "challenges": [
            Challenge(
                id=5101,
                title="编辑计划任务",
                description="打开当前用户的 crontab 编辑界面。",
                expected_command=["crontab -e"],
                hint="crontab -e",
                success_msg="进入 Crontab 编辑模式（模拟）。",
                knowledge_point="crontab: 维护 crontab 文件以供 cron 守护进程执行。",
                initial_fs={}
            )
        ]
    },
    52: {
        "name": "系统监控",
        "challenges": [
            Challenge(
                id=5201,
                title="虚拟内存统计",
                description="每 2 秒显示一次虚拟内存统计信息，共显示 3 次。",
                expected_command=["vmstat 2 3"],
                hint="vmstat 间隔 次数",
                success_msg="统计信息已显示。",
                knowledge_point="vmstat: 报告虚拟内存统计信息。",
                initial_fs={}
            ),
            Challenge(
                id=5202,
                title="系统负载",
                description="查看系统运行时间和平均负载。",
                expected_command=["uptime"],
                hint="uptime",
                success_msg="系统负载信息已显示。",
                knowledge_point="uptime: 告知系统运行了多长时间。",
                initial_fs={}
            )
        ]
    },
    53: {
        "name": "日志管理",
        "challenges": [
            Challenge(
                id=5301,
                title="查看系统日志",
                description="使用 journalctl 查看最近的系统日志。",
                expected_command=["journalctl", "journalctl -xe"],
                hint="journalctl",
                success_msg="日志已显示。",
                knowledge_point="journalctl: 查询 systemd 日志。",
                initial_fs={}
            )
        ]
    },
    54: {
        "name": "服务管理",
        "challenges": [
            Challenge(
                id=5401,
                title="启动服务",
                description="启动 'nginx' 服务。",
                expected_command=["systemctl start nginx", "service nginx start"],
                hint="systemctl start 服务名",
                success_msg="服务已启动。",
                knowledge_point="systemctl: 控制 systemd 系统和服务管理器。",
                initial_fs={}
            ),
            Challenge(
                id=5402,
                title="查看服务状态",
                description="查看 'nginx' 服务的状态。",
                expected_command=["systemctl status nginx", "service nginx status"],
                hint="systemctl status 服务名",
                success_msg="服务状态：active (running)。",
                knowledge_point="systemctl status: 查看服务运行状态。",
                initial_fs={}
            )
        ]
    },
    55: {
        "name": "软件包管理",
        "challenges": [
            Challenge(
                id=5501,
                title="安装软件",
                description="使用 apt 安装 'git'。",
                expected_command=["apt install git", "apt-get install git"],
                hint="apt install 软件包名",
                success_msg="软件包安装成功。",
                knowledge_point="apt: Debian/Ubuntu 的软件包管理工具。",
                initial_fs={}
            )
        ]
    },
    56: {
        "name": "内核模块",
        "challenges": [
            Challenge(
                id=5601,
                title="列出模块",
                description="列出当前加载的所有内核模块。",
                expected_command=["lsmod"],
                hint="lsmod",
                success_msg="内核模块列表已显示。",
                knowledge_point="lsmod: 显示已加载的内核模块状态。",
                initial_fs={}
            )
        ]
    },
    57: {
        "name": "硬件信息",
        "challenges": [
            Challenge(
                id=5701,
                title="CPU 信息",
                description="查看 CPU 架构信息。",
                expected_command=["lscpu", "cat /proc/cpuinfo"],
                hint="lscpu",
                success_msg="CPU 信息已显示。",
                knowledge_point="lscpu: 显示 CPU 架构信息。",
                initial_fs={}
            )
        ]
    },
    58: {
        "name": "安全与权限",
        "challenges": [
            Challenge(
                id=5801,
                title="切换用户",
                description="切换到 'root' 用户。",
                expected_command=["su -", "su", "su root", "sudo su", "sudo -i"],
                hint="su - 或 sudo -i",
                success_msg="切换成功（模拟）。",
                knowledge_point="su: 切换用户 ID 或成为超级用户。",
                initial_fs={}
            ),
            Challenge(
                id=5802,
                title="查看登录失败",
                description="查看最近登录失败的记录。",
                expected_command=["lastb", "lastb -n 10"],
                hint="lastb",
                success_msg="登录失败记录已显示。",
                knowledge_point="lastb: 显示登录失败的用户列表。",
                initial_fs={}
            )
        ]
    },
    59: {
        "name": "打印管理",
        "challenges": [
            Challenge(
                id=5901,
                title="查看打印队列",
                description="查看当前的打印队列状态。",
                expected_command=["lpq", "lpstat -p"],
                hint="lpq",
                success_msg="打印队列为空。",
                knowledge_point="lpq: 显示打印机队列状态。",
                initial_fs={}
            )
        ]
    },
    60: {
        "name": "终极挑战",
        "challenges": [
            Challenge(
                id=6001,
                title="磁盘空间救援",
                description="根分区 '/' 使用率 100%，找到并删除 '/var/log' 下大于 100MB 的日志文件。",
                expected_command=["find /var/log -size +100M -delete", "find /var/log -size +100M -exec rm {} \\;"],
                hint="find 路径 -size +大小 -delete",
                success_msg="大文件已清理，磁盘空间恢复正常。",
                knowledge_point="find: 强大的文件查找工具，配合 -delete 可快速清理文件。",
                initial_fs={"/var/log/syslog.1": "x" * 1024 * 1024 * 101, "/var/log/auth.log": "normal content"}
            )
        ]
    }
}
