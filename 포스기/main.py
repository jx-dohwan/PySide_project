import sys
import datetime
from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QTimer
from ui import Ui_MainWindow

orders = [
    {"menu":"에스프레소 L", "quantity":"10", "order_amount": "10000", "time":"2022-01-03 10:23", "status":"waiting"},
    {"menu":"아메리카노 M", "quantity":"12", "order_amount": "14000", "time":"2022-01-05 11:00", "status":"done"}
]

menu_widgets = [
    "radio_espersso",
    "radio_americano",
    "radio_latte",
    "radio_mocha",
    "radio_choco_smoothis",
    "radio_strawberry_smoothie"
]

size_widgets = [
    "radio_size_s",
    "radio_size_m",
    "radio_size_l",
    "radio_size_xl"
]



class MainWindow(QMainWindow):
    quantity_lock = False

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QTimer()
        self.timer.setInterval(990)
        self.timer.timeout.connect(self.tick)
        self.timer.start()
        self.load()

        for w in menu_widgets + size_widgets:
            widget = getattr(self.ui, w)
            widget.clicked.connect(self.calc)

        self.calc()

        self.ui.spin_quantity.valueChanged.connect(self.sync_quantity)
        self.ui.hs_quantity.valueChanged.connect(self.sync_quantity)
        self.ui.vs_quantity.valueChanged.connect(self.sync_quantity)
        self.ui.dial_quantity.valueChanged.connect(self.sync_quantity)

        self.ui.btn_order.clicked.connect(self.order)

        self.ui.table_orders.cellDoubleClicked.connect(self.change_order)

    def tick(self):
        now = datetime.datetime.now()
        self.ui.lb_now.setText(f"현재시각 : {now}")


    def load(self):
        self.ui.table_orders.setRowCount(0)
        for d in orders:
            r = self.ui.table_orders.rowCount()
            self.ui.table_orders.insertRow(r)
            self.ui.table_orders.setItem(r, 0 , QTableWidgetItem(d["menu"]))
            self.ui.table_orders.setItem(r, 1 , QTableWidgetItem(d["quantity"]))
            self.ui.table_orders.setItem(r, 2 , QTableWidgetItem(d["order_amount"]))
            self.ui.table_orders.setItem(r, 3 , QTableWidgetItem(d["time"]))
            self.ui.table_orders.setItem(r, 4 , QTableWidgetItem(d["status"]))

            # lcd 주문 현황 업데이트 
            self.ui.lcd_num_of_orders.display(len(orders))
            waiting = [x for x in orders if x["status"] == "waiting"]
            self.ui.lcd_num_of_orders_waiting.display(len(waiting))
            processing = [x for x in orders if x["status"] == "processing"]
            self.ui.lcd_num_of_orders_processing.display(len(processing))
            delivery = [x for x in orders if x["status"] == "delivery"]
            self.ui.lcd_num_of_orders_delivery.display(len(delivery))
            done = [x for x in orders if x["status"] == "done"]
            self.ui.lcd_num_of_orders_done.display(len(done))

    def calc(self):
        menu_price = {
            "에스프레소" : 1000,
            "아메리카노" : 1500,
            "라떼" : 3000,
            "모카" : 3500,
            "초코 스무디" : 4000,
            "딸기 스무디" : 4000
        }
        size_price = {
            "S" : 0,
            "M" : 500,
            "L" : 1000,
            "XL" : 1500
        }
        price = 0
        for w in menu_widgets:
            menu = getattr(self.ui, w)
          
            if menu.isChecked():
                price = menu_price[menu.text()]
                break
        for w in size_widgets:
            size = getattr(self.ui, w)
            if size.isChecked():
                price += size_price[size.text()]
                break

        quantity = self.ui.spin_quantity.value()
        price = price * quantity
        self.ui.lb_order_amount.setText(f"총 주문 금액 : {price}원" )
        return price

    def sync_quantity(self):
        if self.quantity_lock:
            return

        self.quantity_lock = True

        spin = self.ui.spin_quantity
        hs = self.ui.hs_quantity
        vs = self.ui.vs_quantity
        dial = self.ui.dial_quantity

        values = [spin.value(), hs.value(), vs.value(), dial.value()]
        dup = {}
        for v in values:
            dup[v] = dup.get(v,0) + 1
        for k, v in dup.items():
            if v == 1:
                target = k

        spin.setValue(target)
        hs.setValue(target)
        vs.setValue(target)
        dial.setValue(target)

        self.calc()

        self.quantity_lock = False

    def order(self):
        menu = ""
        for w in menu_widgets:
            radio = getattr(self.ui,w)
            if radio.isChecked():
                menu = radio.text()
                break
                
        for w in menu_widgets:
            radio = getattr(self.ui,w)
            if radio.isChecked():
                menu += " " + radio.text()
                break

        quantity = self.ui.spin_quantity.value()

        order = {
            "menu" : menu,
            "quantity" : str(quantity),
            "order_amount" : self.calc(),
            "time" : str(datetime.datetime.now()),
            "status" : "waiting",
        } 

        orders.append(order)
        mb = QMessageBox()
        mb.setText("발주 되었습니다.")
        mb.exec()

        self.load()

    def change_order(self, r, c):
        status = ["waiting","processing","delivery","done","done"] #  뭔소리라? 자료구조 알고리즘인 것 같은데
        orders[r]["status"]= status[status.index(orders[r]["status"]) + 1]

        self.load()

if __name__=="__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
