import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from UI import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_hi.clicked.connect(self.click)

    def click(self):
        mb_hi = QMessageBox()
        mb_hi.setText("안녕하세요")
        mb_hi.exec() # 무엇을 클릭했는지 메시지 박스가 알려주기 위해 반환하기 위함

        mb_quiz = QMessageBox()
        mb_quiz.setText("1+1?")
        btn_answer_2 = mb_quiz.addButton("2", QMessageBox.ActionRole)
        btn_answer_3 = mb_quiz.addButton("3", QMessageBox.ActionRole)
        mb_quiz.exec()

    def click(self):
        self.ui.chk_1.setChecked(True)
        self.ui.chk_2.setChecked(True)
        self.ui.chk_3.setChecked(True)

        if self.ui.radio_1.isChecked():
            self.ui.radio_2.setChecked(True)
        elif self.ui.radio_2.isChecked():
            self.ui.radio_1.setChecked(True)
        else:
            self.ui.radio_1.setChecked(True)


        # if mb_quiz.clickedButton() == btn_answer_2:
        #     mb_success = QMessageBox()
        #     mb_success.setText("정답입니다.!")
        #     mb_success.exec()
            
        # elif mb_quiz.clickedButton() == btn_answer_3:
        #     mb_fail = QMessageBox()
        #     mb_fail.setText("오답입니다.")
        #     mb_fail.exec()

if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 
    # sys.exit 는 파이썬 프로그램을 끄겠다는 것이다.
    # app.exec()는 QApplication()을 실행시키는 것이다. 
    # QApplication이 꺼지면 파이썬도 같이 꺼진다.