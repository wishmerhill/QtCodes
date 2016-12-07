#!/usr/bin/python ~/devel/QtCodes/main.py

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
        print('*** Warning *** pyqrcodes not found - Please install before going on! ***')
    exit()

import PyQt4.uic
from PyQt4 import QtGui
import signal

class MainWindow(QtGui.QMainWindow):
    """
    The main window, who whould have supposed?
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/mainWindow.ui', self)

        self.pushButton.clicked.connect(self.generateQR)

    def generateQR(self):
        """

        """
        data = unicode(self.textEdit.toPlainText())
        if DEBUG_MODE:
            print(data)
        qr = pyqrcode.create(data, error='H', mode=None, encoding=None)

        qr.png('filename.png', scale=2)
        pixmap = QtGui.QPixmap('filename.png')
        # width = pixmap.width()
        # height = pixmap.height()
        self.qrPreview.setPixmap(pixmap)
        self.qrPreview.adjustSize()
        return



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
