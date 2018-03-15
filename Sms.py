from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal


class Sms(QObject):
    """ Properties """
    __message = ''
    __from_phone = ''
    __to_phone = ''
    __device = None
    __complete = False

    """ Signals """
    messageChanged = pyqtSignal()
    fromChanged = pyqtSignal()
    toChanged = pyqtSignal()
    deviceChanged = pyqtSignal()
    completeChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtProperty('QString', notify=messageChanged)
    def message(self):
        return self.__name

    @message.setter
    def message(self, message):
        if message != self.__message:
            self.__message = message
            self.messageChanged.emit()

    @pyqtProperty('QString', notify=fromChanged)
    def from_phone(self):
        return self.__from_phone

    @from_phone.setter
    def from_phone(self, from_phone):
        if from_phone != self.__from_phone:
            self.__from_phone = from_phone
            self.fromChanged.emit()

    @pyqtProperty('QString', notify=toChanged)
    def to_phone(self):
        return self.__to_phone

    @to_phone.setter
    def to_phone(self, to_phone):
        if to_phone != self.__to_phone:
            self.__to_phone = to_phone
            self.toChanged.emit()

    @pyqtProperty('QString', notify=toChanged)
    def device(self):
        return self.__device

    @device.setter
    def device(self, device):
        self.__device = device
        self.deviceChanged.emit()

    @pyqtProperty('bool', notify=completeChanged)
    def complete(self):
        return self.__complete

    @complete.setter
    def complete(self, complete):
        if complete != self.__complete:
            self.__complete = complete
            self.completeChanged.emit()

    def is_empty(self):
        check1 = self.__device is None
        check2 = self.__message is None or len(self.__message) == 0
        check3 = self.__from_phone is None or self.__to_phone is None
        return check1 or check2 or check3
