import sys
import random
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from ui2 import Ui_MainWindow
from PySide6.QtCore import QTimer

class MainWindow(QMainWindow):
    last_read = 0

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) # 나에게 ui로부터 셋업 ui를 한다.    

        self.ui.btn_send.clicked.connect(self.send)
        self.ui.edit_text.returnPressed.connect(self.send)

        nickname = self.random_nickname()
        self.ui.edit_nickname.setText(nickname)

        # 환영합니다. 메세지
        with open("./server.txt", "a+", encoding="utf-8") as f:
            f.writelines(f"--------{nickname}님이 입장하셨습니다.--------\n")

        self.listen()

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.listen)
        self.timer.start()

    def send(self):
        nickname = self.ui.edit_nickname.text()
        text = self.ui.edit_text.text()
        msg = f"{nickname}:{text}"

        # 파일에다가 msg 쓰는 거에요
        
        with open("./server.txt","a+",encoding="utf-8") as f:
            f.writelines(msg + "\n")

        self.ui.edit_text.clear()


    def random_nickname(self):
        nickname = random.choice(["홍길동", "박보검", "정소민", "강도리"])
        num = random.randint(1,1000)
        return f"{nickname}{num}"

    def listen(self):
        try:
            with open("./server.txt", "r", encoding='utf-8') as f:
                lines = f.readlines()
            lines = [x.strip() for x in lines]
            self.ui.list_chat.addItems(lines[self.last_read:])
            self.last_read = len(lines)
            self.ui.list_chat.scrollToBottom()
        except:
            pass

        
     

if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
