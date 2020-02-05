#!/usr/bin/env python3


import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MilkCalculation(QMainWindow):
    def __init__(self, parent=None):
        super(MilkCalculation, self).__init__(parent)
        no_of_days_label = QLabel('No. of Days ')
        self.no_of_days_spinbox = QSpinBox()
        self.no_of_days_spinbox.setRange(1, 31)
        self.no_of_days_spinbox.setValue(3)
        self.no_of_days_spinbox.selectAll()
        # self.no_of_days_submit_button = QPushButton('&Submit')
        # self.no_of_days_submit_button.clicked.connect(self.daysEntered)

        self.main_layout = QVBoxLayout()
        no_of_days_layout = QHBoxLayout()
        no_of_days_layout.addWidget(no_of_days_label)
        no_of_days_layout.addWidget(self.no_of_days_spinbox)
        # no_of_days_layout.addWidget(self.no_of_days_submit_button)
        self.main_layout.addLayout(no_of_days_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        self.setCentralWidget(central_widget)
        self.setMinimumWidth(300)
        self.setWindowTitle("Milk Calculation")
        self.show()

    def keyPressEvent(self, e):
        print("iam called")
        if self.no_of_days_spinbox.hasFocus() and (e.key() == Qt.Key_Enter or
                                                   e.key() == Qt.Key_Return):
            self.daysEntered(self.no_of_days_spinbox.value())


    def daysEntered(self, days):
        """As soon as the submit button beside no of days spinbox is clicked
        this method creates that many quantity and reading spinboxes
        """
        # deleting previous quantity reading layout and results layout if already existed
        if self.main_layout.count() > 1:
            for i in range(1, self.main_layout.count()):
                self.removeLayout(self.main_layout.itemAt(i))
                self.main_layout.itemAt(i).deleteLater()
        quantity_heading = QLabel("<b>Quantity</b>")
        quantity_heading.setAlignment(Qt.AlignCenter)
        reading_heading = QLabel("<b>Reading</b>")
        reading_heading.setAlignment(Qt.AlignCenter)
        self.quantity_reading_layout = QGridLayout()
        self.quantity_reading_layout.addWidget(quantity_heading, 0, 1)
        self.quantity_reading_layout.addWidget(reading_heading, 0, 2)
        # storing the spinboxes in lists
        self.quantities = []
        self.readings = []
        min_value = 1
        max_value = 100
        # creating the spinboxes
        for i in range(days):
            day_label = QLabel("Day {}".format(i+1))
            quantity = QSpinBox()
            quantity.setRange(min_value, max_value)
            quantity.valueChanged.connect(self.spinboxValueChanged)
            self.quantities.append(quantity)
            reading = QSpinBox()
            reading.setRange(50, 100)
            reading.valueChanged.connect(self.spinboxValueChanged)
            self.readings.append(reading)
            self.quantity_reading_layout.addWidget(day_label, i+1, 0)
            self.quantity_reading_layout.addWidget(quantity, i+1, 1)
            self.quantity_reading_layout.addWidget(reading, i+1, 2)
        calculate_button = QPushButton('Calculate')
        calculate_button.clicked.connect(self.calculateMilkPrice)
        self.quantity_reading_layout.addWidget(calculate_button, days+1, 1)
        self.main_layout.addLayout(self.quantity_reading_layout)
        self.resize(self.sizeHint())

    def spinboxValueChanged(self):
        """this method automatically changes focus to next spinbox as soon as
        a quantity or a reading is entered
        """
        value = self.sender().value()
        if len(str(int(value))) == 2:
            self.focusNextChild()

    def removeLayout(self, layout):
        """this method takes a layout and deletes it completely
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
        self.main_layout.sizeHint()


    def calculateMilkPrice(self):
        """this method calculates the total price by taking quantities
        and readings from all spinboxes.
        """
        # deleting results layout if already existed
        if self.main_layout.count() > 2:
            for i in range(2, self.main_layout.count()):
                self.removeLayout(self.main_layout.itemAt(i))
                self.main_layout.itemAt(i).deleteLater()

        quantities = [x.value() / 10 for x in self.quantities]
        readings = [x.value() / 10 for x in self.readings]
        base_price = 26.0  # base price in INR
        base_reading = 5.0
        difference = 0.52  # difference between successive readings
        price_per_litre = [(
            base_price + (reading - base_reading) * 10 * difference) for reading in readings]
        prices = []  # quantity * price_per_litre
        for i in range(len(quantities)):
            prices.append(round(quantities[i] * price_per_litre[i], 2))
        # result widgets
        self.results_layout = QHBoxLayout()
        self.results_label = QLabel("Total Days: <b>{}</b><br>"
                                    "Total Quantity: <b>{:.2f}</b> Litres<br>"
                                    "Total Price: <b>{:.2f}</b> Rs"
                                    "".format(len(quantities),
                                              sum(quantities),
                                              sum(prices)))
        self.results_layout.addWidget(self.results_label)
        self.main_layout.addLayout(self.results_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MilkCalculation()
    app.exec_()
