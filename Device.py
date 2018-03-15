from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, QSettings

import Manager


class Device(QObject):
    """ Bluez tools """
    __updating = False
    __connected = False
    __available = False
    __mm_support = False

    __name = ''
    __host = ''
    __class_id = ''
    __image = 'images/unknown_device.png'
    __services = []
    __type = 'unknown'
    __vendor = ''

    """ Signals """
    nameChanged = pyqtSignal()
    hostChanged = pyqtSignal()
    classChanged = pyqtSignal()
    imageChanged = pyqtSignal()
    updatingChanged = pyqtSignal()
    servicesChanged = pyqtSignal()
    availableChanged = pyqtSignal()
    typeChanged = pyqtSignal()
    vendorChanged = pyqtSignal()
    mmControlsSupportChanged = pyqtSignal()

    major_classes = ("miscellaneous", "computer", "phone", "lan", "multimedia", "peripheral", "imaging")

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

    @pyqtProperty('QString', notify=vendorChanged)
    def vendor(self):
        return self.__vendor

    @vendor.setter
    def vendor(self, vendor):
        if vendor != self.__vendor:
            self.__vendor = vendor
            self.vendorChanged.emit()

    @pyqtProperty('bool', notify=mmControlsSupportChanged)
    def mm_controls_supported(self):
        return self.__mm_support

    @mm_controls_supported.setter
    def mm_controls_supported(self, supported):
        if supported != self.__mm_support:
            self.__mm_support = supported
            self.mmControlsSupportChanged.emit()

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
            self.classChanged.emit()

            major_class = (int(class_id) >> 8) & 0xf
            if major_class < 7:
                self.type = self.major_classes[major_class]
            else:
                self.type = 'unknown'

    @pyqtProperty('QString', notify=imageChanged)
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        if image != self.__image:
            self.__image = image
            self.classChanged.emit()

    @pyqtProperty('QVariantMap', notify=servicesChanged)
    def services(self):
        return self.__services

    @services.setter
    def services(self, services):
        self.__services = services
        self.servicesChanged.emit()

        self.mm_controls_supported = \
            self.has_service('name', 'AVRCP Device') or \
            self.has_service('description', 'Remote Control Device')

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
    def type(self, type_name):
        if type_name != self.__type:
            self.__type = type_name
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

    def get_service_by_name(self, name):
        for service in self.__services:
            if 'name' in service and service['name'] == name:
                return service

        return None

    def has_service(self, prop, value):
        for service in self.__services:
            if prop in service and service[prop] == value:
                return True

        return False

    def is_empty(self):
        return self.host is None and len(self.host) == 0
