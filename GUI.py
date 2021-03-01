from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit, QListWidget, QWidget, QMessageBox, QStatusBar, QCheckBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QThreadPool
import qdarkstyle
import sys
import os
from datetime import datetime


class GUI(QWidget):
    def __init__(self):
        super(GUI, self).__init__()

        self.title = "server"
        self.icon_name = "icon.ico"
        self.thread_pool = QThreadPool()
        self.all_ip = []
        self.all_text = {}  # {ip:{process_name : text}}
        self.cur_ip = ""
        self.cur_proc = ""

        self.InitUI()
        self.load_data()


    def InitUI(self):
        # 기본 설정
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon_name))
        self.setGeometry(200, 200, 1000, 700)

        # 레이아웃 선언부
        mainbox = QVBoxLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox = QHBoxLayout()
        underbox = QHBoxLayout()

        # element 선언부
        self.ip_label = QLabel("연결된 IP 목록", self)
        self.ip_list = QListWidget(self)
        self.ip_list.clicked.connect(self.ip_listview_clicked)

        self.proc_label = QLabel("연결된 프로세스 목록", self)
        self.proc_list = QListWidget(self)
        self.proc_list.clicked.connect(self.proc_listview_clicked)
        self.textarea = QPlainTextEdit(self)
        self.textarea.setReadOnly(True)

        self.statusbar = QStatusBar()
        self.check_label = QLabel('현재 프로세스 추적', self)
        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(True)

        # 위젯 & 레이아웃 정렬
        vbox1.addWidget(self.ip_label)
        vbox1.addWidget(self.ip_list)
        vbox2.addWidget(self.proc_label)
        vbox2.addWidget(self.proc_list)
        hbox.addLayout(vbox1, stretch=4)
        hbox.addLayout(vbox2, stretch=8)
        hbox.addWidget(self.textarea, stretch=15)
        underbox.addWidget(self.statusbar)
        underbox.addWidget(self.check_label)
        underbox.addWidget(self.checkbox)
        mainbox.addLayout(hbox)
        mainbox.addLayout(underbox)
        self.setLayout(mainbox)


    @pyqtSlot()
    def ip_listview_clicked(self):
        """  ip리스뷰 클릭시 """
        item = self.ip_list.currentIndex()
        item = str(item.text())
        self.all_text[self.cur_ip][self.cur_proc] = self.textarea.toPlainText()
        self.cur_ip = item
        if self.all_ip[self.cur_ip]:
            self.cur_proc = next(iter(self.all_ip[self.cur_ip]))  # 가장 처음 시작된 프로세스로
        else:
            self.cur_proc = None
        self.textarea.clear()
        if self.all_text[self.cur_ip][self.cur_proc]:
            self.append_message(self.all_text[self.cur_ip][self.cur_proc])

    def listview_update(self, ips):
        try:
            self.ip_list.clear()
            self.ip_list.addItems(ips)

            if self.cur_ip not in ips:
                self.statusbar.showMessage("연결된 ip가 없습니다")
                return


        except:
            self.statusbar.showMessage("Except!!")

    @pyqtSlot()
    def proc_listview_clicked(self):
        """ process 리스트뷰 클릭시"""
        item = self.ip_list.currentIndex()
        item = str(item.text())
        self.all_text[self.cur_ip][self.cur_proc] = self.textarea.toPlainText()
        self.cur_proc = item
        self.textarea.clear()
        if self.all_text[self.cur_ip][self.cur_proc]:
            self.append_message(self.all_text[self.cur_ip][self.cur_proc])


    def load_data(self):
        """ 기존에 연결된 ip 데이터 로드"""
        for (path, dirc, files) in os.walk(os.getcwd() + "\\log"):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == '.log':
                    ip = path.split("\\")[-1]
                    pname = filename
                    with open(path+'\\'+filename, 'rt') as f:
                        if not ip in self.all_text:
                            self.all_text[ip] = dict()
                        self.all_text[ip][pname] = "".join(f.readlines())


    def save_data(self):
        """ 연결되었던 ip 파일에 로그 저장 """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for ip in self.all_ip:
            for pname in self.all_text[ip]:
                path = os.getcwd() + '\\log\\' + ip + '\\' + pname
                with open(path, 'wt') as f:
                    f.writelines(self.all_text[ip][pname] + now + '\n' + '='*40 + '\n\n')



    def append_message(self, message):
        """ 메세지를 추가함 """
        self.textarea.appendPlainText(
            message)  # insert vs append "\n"이 없냐 있냐 & 자동 스크롤이 안되냐 되냐 차이
        self.textarea.viewport().update()

    def closeEvent(self, event):
        """ 종료시 모든 데이터 저장 """
        close = QMessageBox.question(self,
                                   "QUIT",
                                   "정말 나가시겠습니까??",
                                   QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            self.hide()  # 화면을 숨기고 데이터를 저장후 종료
            self.save_data()
            event.accept()
        else:
            event.ignore()

app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
gui = GUI()
gui.show()
sys.exit(app.exec_())