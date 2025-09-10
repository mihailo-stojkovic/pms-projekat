# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dizajn.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLCDNumber, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)
from ui.PlotCanvas import PlotCanvas

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(841, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonStart = QPushButton(self.centralwidget)
        self.buttonStart.setObjectName(u"buttonStart")
        self.buttonStart.setGeometry(QRect(640, 410, 75, 23))
        self.buttonStop = QPushButton(self.centralwidget)
        self.buttonStop.setObjectName(u"buttonStop")
        self.buttonStop.setGeometry(QRect(750, 410, 75, 23))
        self.labelBrzinaHoda = QLabel(self.centralwidget)
        self.labelBrzinaHoda.setObjectName(u"labelBrzinaHoda")
        self.labelBrzinaHoda.setGeometry(QRect(660, 10, 81, 16))
        self.lcdNumberBrzina = QLCDNumber(self.centralwidget)
        self.lcdNumberBrzina.setObjectName(u"lcdNumberBrzina")
        self.lcdNumberBrzina.setGeometry(QRect(740, 10, 71, 23))
        self.lcdNumberBrzina.setSegmentStyle(QLCDNumber.Flat)
        self.labelBrojKoraka = QLabel(self.centralwidget)
        self.labelBrojKoraka.setObjectName(u"labelBrojKoraka")
        self.labelBrojKoraka.setGeometry(QRect(660, 40, 81, 16))
        self.lcdNumberBrojKoraka = QLCDNumber(self.centralwidget)
        self.lcdNumberBrojKoraka.setObjectName(u"lcdNumberBrojKoraka")
        self.lcdNumberBrojKoraka.setGeometry(QRect(740, 40, 71, 23))
        self.lcdNumberBrojKoraka.setSegmentStyle(QLCDNumber.Flat)
        self.labelAx = QLabel(self.centralwidget)
        self.labelAx.setObjectName(u"labelAx")
        self.labelAx.setGeometry(QRect(710, 90, 31, 20))
        self.lcdNumberAx = QLCDNumber(self.centralwidget)
        self.lcdNumberAx.setObjectName(u"lcdNumberAx")
        self.lcdNumberAx.setGeometry(QRect(740, 90, 71, 23))
        self.lcdNumberAx.setSegmentStyle(QLCDNumber.Flat)
        self.labelAy = QLabel(self.centralwidget)
        self.labelAy.setObjectName(u"labelAy")
        self.labelAy.setGeometry(QRect(710, 120, 31, 20))
        self.lcdNumberAy = QLCDNumber(self.centralwidget)
        self.lcdNumberAy.setObjectName(u"lcdNumberAy")
        self.lcdNumberAy.setGeometry(QRect(740, 120, 71, 23))
        self.lcdNumberAy.setSegmentStyle(QLCDNumber.Flat)
        self.labelAz = QLabel(self.centralwidget)
        self.labelAz.setObjectName(u"labelAz")
        self.labelAz.setGeometry(QRect(710, 150, 31, 20))
        self.lcdNumberAz = QLCDNumber(self.centralwidget)
        self.lcdNumberAz.setObjectName(u"lcdNumberAz")
        self.lcdNumberAz.setGeometry(QRect(740, 150, 71, 23))
        self.lcdNumberAz.setSegmentStyle(QLCDNumber.Flat)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(640, 210, 113, 20))
        self.lineVert = QFrame(self.centralwidget)
        self.lineVert.setObjectName(u"lineVert")
        self.lineVert.setGeometry(QRect(623, 0, 20, 431))
        self.lineVert.setFrameShape(QFrame.Shape.VLine)
        self.lineVert.setFrameShadow(QFrame.Shadow.Sunken)
        self.buttonPragPrimeni = QPushButton(self.centralwidget)
        self.buttonPragPrimeni.setObjectName(u"buttonPragPrimeni")
        self.buttonPragPrimeni.setGeometry(QRect(760, 210, 61, 23))
        self.buttonMinPrimeni = QPushButton(self.centralwidget)
        self.buttonMinPrimeni.setObjectName(u"buttonMinPrimeni")
        self.buttonMinPrimeni.setGeometry(QRect(760, 280, 61, 23))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(640, 280, 113, 20))
        self.labelPragDetekcija = QLabel(self.centralwidget)
        self.labelPragDetekcija.setObjectName(u"labelPragDetekcija")
        self.labelPragDetekcija.setGeometry(QRect(640, 190, 111, 16))
        self.labelMinBrzina = QLabel(self.centralwidget)
        self.labelMinBrzina.setObjectName(u"labelMinBrzina")
        self.labelMinBrzina.setGeometry(QRect(640, 260, 111, 16))
        
        # PROMENJENO OD IZVORNO UI FAJLA
        self.plotWidget = PlotCanvas(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")
        self.plotWidget.setGeometry(QRect(10, 10, 611, 381))
       
        self.lineHor = QFrame(self.centralwidget)
        self.lineHor.setObjectName(u"lineHor")
        self.lineHor.setGeometry(QRect(0, 390, 831, 20))
        self.lineHor.setFrameShape(QFrame.Shape.HLine)
        self.lineHor.setFrameShadow(QFrame.Shadow.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 841, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Kontrolna Tabla", None))
        self.buttonStart.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.buttonStop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.labelBrzinaHoda.setText(QCoreApplication.translate("MainWindow", u"BRZINA HODA:", None))
        self.labelBrojKoraka.setText(QCoreApplication.translate("MainWindow", u"BROJ KORAKA:", None))
        self.labelAx.setText(QCoreApplication.translate("MainWindow", u"a_X:", None))
        self.labelAy.setText(QCoreApplication.translate("MainWindow", u"a_Y", None))
        self.labelAz.setText(QCoreApplication.translate("MainWindow", u"a_Z", None))
        self.buttonPragPrimeni.setText(QCoreApplication.translate("MainWindow", u"PRIMENI", None))
        self.buttonMinPrimeni.setText(QCoreApplication.translate("MainWindow", u"PRIMENI", None))
        self.labelPragDetekcija.setText(QCoreApplication.translate("MainWindow", u"PRAG ZA DETEKCIJU", None))
        self.labelMinBrzina.setText(QCoreApplication.translate("MainWindow", u"MINIMALNA BRZINA", None))
    # retranslateUi

