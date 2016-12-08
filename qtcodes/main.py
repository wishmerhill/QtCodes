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

import PyQt4.uic
from PyQt4 import QtGui
import signal
import vobject


class quitDialog(QtGui.QDialog):
    """
    the quit dialog
    """

    def __init__(self, parent=None):
        super(quitDialog, self).__init__(parent)

        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/quitDialog.ui', self)

        self.pushButtonYes.clicked.connect(app.quit)
        self.pushButtonNo.clicked.connect(self.close)


class MainWindow(QtGui.QMainWindow):
    """
    The main window, who whould have supposed?
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/mainWindow.ui', self)

        # Setting the Text tab as active. Better so.
        if DEBUG_MODE:
            print("DEBUG: Setting plain text tab as active")
        self.tabWidget.setCurrentIndex(0)

        self.generateButton.clicked.connect(self.generateQR)

        self.selectFileButton.clicked.connect(self.selectFile)

        self.actionQuit.triggered.connect(self.doClose)

        self.filename = 'filename.png'


    def generateQR(self):
        """

        """
        data = unicode(self.textEdit.toPlainText())
        if DEBUG_MODE:
            print(data)

        # create the QR
        qr = pyqrcode.create(data, error='H', mode=None, encoding=None)

        # generate the PNG file *** TODO: let the use choose filetype, scale and other parameters.
        qr.png(self.filename, scale=3)

        # store the file as pixmap
        pixmap = QtGui.QPixmap(self.filename)

        self.qrPreview.setPixmap(pixmap)


        self.qrPreview.adjustSize()

    def selectFile(self):
        '''
        Just a small function to open a file dialog
        '''

        self.filenameEdit.setText(QtGui.QFileDialog.getOpenFileName())

        # encode the resulting filename as UNICODE text
        self.filename=unicode(self.filenameEdit.text())

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
    if ( not app ):
        app = QtGui.QApplication([])

    window = MainWindow()
    window.show()

    if (app):
        app.exec_()
