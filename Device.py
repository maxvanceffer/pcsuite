from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, QSettings

import Manager


class Device(QObject):
    """ Bluez tools """
    __updating = False
    __connected = False
    __available = False

    __name = ''
    __host = ''
    __class_id = ''
    __image = 'images/unknown_device.png'
    __services = []
    __type = 'unknown'

    """ Signals """
    nameChanged = pyqtSignal()
    hostChanged = pyqtSignal()
    classChanged = pyqtSignal()
    imageChanged = pyqtSignal()
    updatingChanged = pyqtSignal()
    servicesChanged = pyqtSignal()
    availableChanged = pyqtSignal()
    typeChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name != self.__name:
            self.__name = name
            self.nameChanged.emit()

    @pyqtProperty('QString', notify=hostChanged)
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        if host != self.__host:
            self.__host = host
            self.hostChanged.emit()

    @pyqtProperty('QString', notify=classChanged)
    def class_id(self):
        return self.__class_id

    @class_id.setter
    def class_id(self, class_id):
        if class_id != self.__class_id:
            self.__class_id = class_id
            self.type = class_id
            self.classChanged.emit()

    @pyqtProperty('QString', notify=imageChanged)
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        if image != self.__class_id:
            self.__class_id = image
            self.classChanged.emit()

    @pyqtProperty('QVariantMap', notify=servicesChanged)
    def services(self):
        return self.__services

    @services.setter
    def services(self, services):
        self.__services = services
        self.servicesChanged.emit()

    @pyqtProperty('bool', notify=availableChanged)
    def available(self):
        return self.__available

    @available.setter
    def available(self, status):
        self.__available = status
        self.availableChanged.emit()

    @pyqtProperty('bool', notify=updatingChanged)
    def updating(self):
        return self.__updating

    @updating.setter
    def updating(self, status):
        if status != self.__updating:
            self.__updating = status
            self.updatingChanged.emit()

    @pyqtProperty('QString', notify=typeChanged)
    def type(self):
        return self.__type

    @type.setter
    def type(self, id_of_type):
        real_type = self.__type
        if id_of_type is not None and str(hex(int(id_of_type))) == '0x5a020c' or str(hex(int(id_of_type))) == '0x7a020c':
            real_type = 'phone'
        elif id_of_type is None and str(hex(int(id_of_type))) == '0x240404':
            real_type = 'speaker'

        if real_type != self.__type:
            self.__type = real_type
            self.updatingChanged.emit()

    @pyqtSlot()
    def update(self):
        self.check_status()

    @pyqtSlot()
    def check_status(self):
        if len(self.__host) == 0:
            print('No device host address set')
            return False

        self.__updating = True
        self.updatingChanged.emit()

        Manager.Manager().find_device_state(self)

