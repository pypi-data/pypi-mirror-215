"""Logger propagating log records to the LoggingWidget.
"""

from logging import StreamHandler
from PyQt5 import QtCore


# ----------------------------------------------------------------------
class GuiLogger(QtCore.QObject, StreamHandler):

    emit_record = QtCore.pyqtSignal(int, str)

    # ----------------------------------------------------------------------
    def __init__(self):
        QtCore.QObject.__init__(self)
        StreamHandler.__init__(self)

    # ----------------------------------------------------------------------
    def emit(self, record):
        self.emit_record.emit(int(record.levelno), f'{record.asctime.split(",")[0]} {record.levelname} {record.msg}')
