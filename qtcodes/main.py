#!/usr/bin/python ~/devel/QtCodes/qtcodes/main.py

# define authorship information
__authors__ = ['Alberto "wishmehill" Azzalini']
__author__ = ','.join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2014'
__license__ = 'GPL'

# maintanence information
__maintainer__ = 'Alberto Azzalini'
__email__ = 'alberto.azzalini@gmail.com'

# Set the debug mode (0 = off; 1 = on)
DEBUG_MODE = 1

try:
    import pyqrcode
except ImportError:
    if DEBUG_MODE:
        print('DEBUG: *** Warning *** pyqrcodes not found - Please install before going on! ***')
    exit()

import signal

import PyQt4.uic
import vobject
from PyQt4 import QtGui, QtCore


class quitDialog(QtGui.QDialog):
    """
    the quit dialog
    """

    def __init__(self, parent=None):
        super(quitDialog, self).__init__(parent)

        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/quitDialog.ui', self)
        self.buttonBox.accepted.connect(app.quit)
        self.buttonBox.rejected.connect(self.close)


class MainWindow(QtGui.QMainWindow):
    """
    The main window, who whould have supposed?
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/mainWindow.ui', self)

        self.family = ""
        self.given = ""
        self.prefix = ""

        # Setting the Text tab as active. Better so.
        if DEBUG_MODE:
            print("DEBUG: Setting plain text tab as active")
        self.tabWidget.setCurrentIndex(0)

        self.dateBirthday.setDateTime(QtCore.QDateTime.currentDateTime())

        self.dateBirthday.setDisplayFormat("dd MMMM yyyy")

        self.generateButton.clicked.connect(self.setUpQR)

        self.selectFileButton.clicked.connect(self.selectFile)

        self.actionQuit.triggered.connect(self.doClose)

        self.tabWidget.currentChanged.connect(self.tabChanged)

        self.lineName.textChanged.connect(self.updatevCardName)
        self.lineSurname.textChanged.connect(self.updatevCardSurname)
        self.linePrefix.textChanged.connect(self.updatevCardPrefix)
        self.lineEmail.textChanged.connect(self.updatevCardEmail)
        self.checkBoxPhone.stateChanged.connect(self.enablePhone)
        self.linePhone.textChanged.connect(self.updatevCardPhone)
        self.checkBoxOffice.stateChanged.connect(self.enableOffice)
        self.lineOffice.textChanged.connect(self.updatevCardOffice)
        self.checkBoxMobile.stateChanged.connect(self.enableMobile)
        self.lineMobile.textChanged.connect(self.updatevCardMobile)

        self.filename = 'filename.png'

        self.vCard = None

    def updatevCardName(self, data):
        """

        :param data:
        :return:
        """
        self.given = unicode(data)
        self.updateName()

    def updatevCardSurname(self, data):
        """

        :param data:
        :return:
        """
        self.family = unicode(data)
        self.updateName()

    def updatevCardPrefix(self, data):
        """

        :param data:
        :return:
        """
        self.prefix = unicode(data)
        self.updateName()

    def updatevCardEmail(self, data):
        """

        :param data:
        :return:
        """
        if not hasattr(self.vCard, 'email'):
            if DEBUG_MODE:
                print('Adding attribute "email"')
            self.vCard.add('email')
        if not hasattr(self.vCard.email, 'type_param'):
            if DEBUG_MODE:
                print('Adding attribute "type_param = INTERNET"')
            self.vCard.email.type_param = "INTERNET"

        self.vCard.email.value = unicode(data)

        self.updatevCard()

    def enablePhone(self):
        """

        :return:
        """
        if self.checkBoxPhone.isChecked():
            # adding 'tel' attribute upon checking the checkBox
            self.phone = self.vCard.add('tel')

            # enabling the lineEdit qwidget
            self.linePhone.setEnabled(True)

            # if lineEdit contains something, update the vCard
            if ((self.linePhone.text()) != ""):
                self.updatevCardPhone(self.linePhone.text())

            if DEBUG_MODE:
                print("Enabling Phone")
        elif not self.checkBoxPhone.isChecked():

            # remove the attribute if checkbox is unflagged
            self.vCard.remove(self.phone)

            # disable the lineEdit widget
            self.linePhone.setEnabled(False)

            # update the vCard
            self.updatevCard()

    def updatevCardPhone(self, data):
        """

        :param data:
        :return:
        """

        if not hasattr(self.phone, 'home'):
            print('Adding attribute "type_param = HOME"')
            self.phone.type_param = 'HOME'
        self.phone.value = unicode(data)

        self.updatevCard()

    def enableOffice(self):
        """

        :return:
        """
        if self.checkBoxOffice.isChecked():
            # adding 'tel' attribute upon checking the checkBox
            self.work = self.vCard.add('tel')

            # enabling the lineEdit qwidget
            self.lineOffice.setEnabled(True)

            # if lineEdit contains something, update the vCard
            if ((self.lineOffice.text()) != ""):
                self.updatevCardOffice(self.lineOffice.text())

            if DEBUG_MODE:
                print("Enabling Office")
        elif not self.checkBoxOffice.isChecked():

            # remove the attribute if checkbox is unflagged
            self.vCard.remove(self.work)

            # disable the lineEdit widget
            self.lineOffice.setEnabled(False)

            # update the vCard
            self.updatevCard()

    def updatevCardOffice(self, data):
        """

        :param data:
        :return:
        """
        if not hasattr(self.work, 'work'):
            print('Adding attribute "type_param = WORK"')
            self.work.type_param = 'WORK'
        self.work.value = unicode(data)

        self.updatevCard()

    def enableMobile(self):
        """

        :return:
        """
        if self.checkBoxMobile.isChecked():
            # adding 'tel' attribute upon checking the checkBox
            self.mobile = self.vCard.add('tel')

            # enabling the lineEdit qwidget
            self.lineMobile.setEnabled(True)

            # if lineEdit contains something, update the vCard
            if ((self.lineMobile.text()) != ""):
                self.updatevCardMobile(self.lineMobile.text())

            if DEBUG_MODE:
                print("Enabling Office")
        elif not self.checkBoxMobile.isChecked():

            # remove the attribute if checkbox is unflagged
            self.vCard.remove(self.mobile)

            # disable the lineEdit widget
            self.lineMobile.setEnabled(False)

            # update the vCard
            self.updatevCard()

    def updatevCardMobile(self, data):
        """

        :param data:
        :return:
        """

        if not hasattr(self.mobile, 'cell'):
            print('Adding attribute "type_param = CELL"')
            self.mobile.type_param = 'CELL'
        self.mobile.value = unicode(data)

        self.updatevCard()

    def updateName(self):
        self.vCard.n.value = vobject.vcard.Name(given=self.given, family=self.family, prefix=self.prefix)
        self.vCard.fn.value = (self.prefix + "{}" + self.given + "{}" + self.family).format(" " if self.prefix != "" else "",
                                                                                            " " if (self.given != "") and (self.family != "") else "")
        if DEBUG_MODE:
            print(self.vCard.fn.value)
        self.updatevCard()

    def updatevCard(self):
        vCardText = self.vCard.serialize()
        if DEBUG_MODE:
            print(vCardText)
        self.textvCardPreview.setText(vCardText)

    def tabChanged(self, tabIndex):
        """
        Initialize the vCard if needed
        :param tabIndex:
        :return:
        """
        if (tabIndex == 1) and (not self.vCard):
            self.vCard = vobject.vCard()
            self.vCard.add('fn')
            self.vCard.add('n')

            self.updatevCard()

            # self.work = self.vCard.add('tel')
            # self.phone = self.vCard.add('tel')
            # self.mobile = self.vCard.add('tel')

    def setUpQR(self):
        """
        check what to do and just do it

        """

        activeTab = self.tabWidget.currentIndex()

        if DEBUG_MODE:
            print("Active tab is: ", activeTab)
        if (self.tabWidget.currentIndex() == 0):
            if DEBUG_MODE:
                print('Working on Plain Text')
            self.PlainTextQR()
        else:
            if DEBUG_MODE:
                print("Working on vCards")
            self.vCardQR()

    def PlainTextQR(self):
        """

        """
        data = unicode(self.textEdit.toPlainText())
        if DEBUG_MODE:
            print(data)
        # create the QR
        self.generateQR(data)

    def vCardQR(self):
        """
        Will use vobjects to generate an appropriate QR.
        Actually, we should use the text in the preview to generate the QR.
        """
        data = unicode(self.textvCardPreview.toPlainText())

        # create the QR
        self.generateQR(data)

    def generateQR(self, data):
        """

        :param data:
        :return:
        """

        qr = pyqrcode.create(data, error='H', mode=None, encoding=None)
        # generate the PNG file *** TODO: let the use choose filetype, scale and other parameters.
        qr.png(self.filename, scale=3)
        # store the file as pixmap
        pixmap = QtGui.QPixmap(self.filename)
        self.qrPreview.setPixmap(pixmap)
        self.qrPreview.adjustSize()

    def selectFile(self):
        """
        Just a small function to open a file dialog
        """

        self.filenameEdit.setText(QtGui.QFileDialog.getOpenFileName())

        # encode the resulting filename as UNICODE text
        self.filename = unicode(self.filenameEdit.text())

    def doClose(self):
        '''
        Let's ask to confirm quit if there is still some text in the text area
        '''

        data = unicode(self.textEdit.toPlainText())
        if not data:
            self.close()
            if DEBUG_MODE:
                print('Bye!')
        else:
            confirmQuit = quitDialog()
            confirmQuit.show()


if (__name__ == '__main__'):
    # brutal way to catch the CTRL+C signal if run in the console...
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = None
    if (not app):
        app = QtGui.QApplication([])

    window = MainWindow()
    window.show()

    if (app):
        app.exec_()
