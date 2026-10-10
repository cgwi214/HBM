import subprocess
import sys
import os
import logging
from typing import Tuple, Union

logging.getLogger("subprocess").setLevel(logging.WARNING)

def subprocess_run(cmd: Union[Tuple[str], str], isasync=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding ="utf-8", shell=False, **kwargs):
    """
    在子进程中运行命令并返回实例。
    如果设置了编码，则在处理文本时无需对输入/输出进行编码/解码。

    cmd: list|str
        The command to run.
        
    Returns
    =======
    pipeline
    """
    # shell 为True时，cmd可以是字符串，否则是列表。列表的第一个元素是命令，后面的元素是传递给shell的参数。
    if isasync:
        # 异步非阻塞执行
        return subprocess.Popen(cmd, stdout=stdout, stderr=stderr, stdin=stdin, encoding=encoding, shell=shell, **kwargs)
    else:
        # 同步阻塞执行
        return subprocess.run(cmd, stdout=stdout, stderr=stderr, stdin=stdin, encoding=encoding, shell=shell, **kwargs)
    
    