import os
import time
from threading import Thread
from pynput.keyboard import Listener
import ctypes
import psutil

def on_press(key):
    print(key)


def get_title():
    user32 = ctypes.windll.LoadLibrary('user32.dll')
    handle = user32.GetForegroundWindow() # 현재 활성화 윈도우 핸들
    buffer = ctypes.create_unicode_buffer(255) # 저장버퍼 할당
    user32.GetWindowTextW(handle, buffer, ctypes.sizeof(buffer)) # 버퍼에 타이들 저장
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(handle, ctypes.byref(pid)) # pid를 얻음
    pid = pid.value
    if pid == 0:
        return 0, ""
    p = psutil.Process(pid)
    title = p.name() + " " + buffer.value
    return pid, title


def win_title():
    pid, title = get_title()
    while True:
        time.sleep(0.1)
        new_pid, new_title = get_title()
        if new_title and title != new_title:
            print("title change %d [%s]" % (new_pid, new_title))
            pid, title = new_pid, new_title

def main():
    with Listener(on_press=on_press) as listener:
        listener.join()

mainThread = Thread(target=main)
titleThread = Thread(target=win_title)

mainThread.start()
titleThread.start()