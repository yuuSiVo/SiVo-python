# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *

# Create an PyQT4 application object.
a = QApplication(sys.argv)

# The QWidget widget is the base class of all user interface objects in PyQt4.
w = QWidget()

# Show a message box
result = QMessageBox.information(w, 'SiVo', "Synthesize.....")

sys.exit(a.exec_())