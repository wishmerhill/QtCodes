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


"""
TODO: let the quitDialog appear even when the main windows is closed in other ways;
TODO: let the program check for 'unsaved' material also in the vCard fields;
FIXME: get rid of my DEBUG_MODE and stick to the right way as in https://docs.python.org/2/howto/logging.html
"""


class quitDialog(QtGui.QDialog):
    """
    Just the quit dialog.
    I added a button box instead of single buttons. 
    TODO: minor design flaws, like *unresizeable* widget.
    """

    def __init__(self, parent=None):
        super(quitDialog, self).__init__(parent)

        # load the ui
        # NOTE: ui is done with qtdesigner
        self.ui = PyQt4.uic.loadUi('ui/quitDialog.ui', self)
        
        # connect the buttons to the appropriate signals
        
        # quit the program
        self.buttonBox.accepted.connect(app.quit)
        
        # dismiss the quit dialog
        self.buttonBox.rejected.connect(self.close)


class MainWindow(QtGui.QMainWindow):
    """
    The main window, who whould have supposed?
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/mainWindow.ui', self)
        
        # **************************************
        # setup some class globals for the vCard
        self.family = ""
        self.given  = ""
        self.prefix = ""
        # ***************************************

        # Setting the Text tab as active. Better so.
        if DEBUG_MODE:
            print("DEBUG: Setting plain text tab as active")
        self.tabWidget.setCurrentIndex(0)

        # set the current date as default in the birthday field
        # FIXME: is it really clever (or needed)? What would be a better option?
        self.dateBirthday.setDateTime(QtCore.QDateTime.currentDateTime())

        # Set the date format in Italian standard.
        # FIXME: maybe let the user choose? Far too advanced
        self.dateBirthday.setDisplayFormat("dd MMMM yyyy")

        # Start connecting signals to the appropriate functions
        # TIP: I choose to use une function per task, avoiding all purpose functions which prooved to be
        #      way too complex (I have sender() and its results...)
        
        # This is the core: generate the QR (two steps: setUpQR checks the active tab
        # then runs the appropriate generator
        self.generateButton.clicked.connect(self.setUpQR)

        # a simple way to open a file selection window
        self.selectFileButton.clicked.connect(self.selectFile)
        # and a default filename, full of creativity.
        self.filename = 'filename.png'
        
        
        # the quit action in the File menu. A classical approach, isn't it?
        self.actionQuit.triggered.connect(self.doClose)

        # let's do something it the tab is changed. Actually, I use it to initilize the vCard stuff.
        # TODO: check if there is a better way, maybe doing it directly in the __init__?
        self.tabWidget.currentChanged.connect(self.tabChanged)

        # the whole vCard fields stuff.
        # FIXME: naming convention is crap: try to get more consistency!
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
        
        # initialize the vCard global container. Later on it will be a vobject.vCard object.
        self.vCard = None

    def updatevCardName(self, data):
        """
        We just update the "given" name.
        FIXME: as noted before, inconsistency in naming!
        """
        self.given = unicode(data)
        self.updateName()

    def updatevCardSurname(self, data):
        """
        We just update the "family" name.
        FIXME: as noted before, inconsistency in naming!
        """
        self.family = unicode(data)
        self.updateName()

    def updatevCardPrefix(self, data):
        """
        We just update the "prefix" of the name.
        """
        self.prefix = unicode(data)
        self.updateName()
        
    def updateName(self):
        """
        Taking care of both N and FN mandatory vCard attributes.
        we don't need any argument as we use class globals already defined.
        """
        # fill in
        self.vCard.n.value = vobject.vcard.Name(given=self.given, family=self.family, prefix=self.prefix)
        
        # this was tricky (for me) as I had to use conditional string formatting to avoid spaces 
        # where they were not needed.
        # Proud of myself! :)
        self.vCard.fn.value = (self.prefix + "{}" + self.given + "{}" + self.family).format(" " if self.prefix != "" else "",
                                                                                            " " if (self.given != "") and (self.family != "") else "")
        if DEBUG_MODE:
            print(self.vCard.fn.value)
        self.updatevCard()

    def updatevCardEmail(self, data):
        """
        Updating the 'email'.
        TODO: consider if we want more than one email address?
        """
        # check if email attribute already exists: if not create it.
        # FIXME: use variables to store the single objects, as done for the many phone numbers
        #        it's easier to clean up the vCard data if needed!
        if not hasattr(self.vCard, 'email'):
            if DEBUG_MODE:
                print('Adding attribute "email"')
            self.vCard.add('email')
        # same as above, just for the type_param
        if not hasattr(self.vCard.email, 'type_param'):
            if DEBUG_MODE:
                print('Adding attribute "type_param = INTERNET"')
            self.vCard.email.type_param = "INTERNET"

        # fill in the value...
        self.vCard.email.value = unicode(data)

        # update the vCard
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
