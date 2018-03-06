from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class BtService(QObject):
    __host = ''
    __name = ''
    __description = ''
    __provided_by = ''
    __protocol = ''
    __channel_psm = 0
    __svc_classes = []
    __profiles = []
    __service_id = 0

    """ Signals """
    nameChanged = pyqtSignal()
    descriptionChanged = pyqtSignal()
    providedByChanged = pyqtSignal()
    protocolChanged = pyqtSignal()
    channelPsmChanged = pyqtSignal()
    svcClassesChanged = pyqtSignal()
    profilesChanged = pyqtSignal()
    serviceIdChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self.__name

    @pyqtProperty('QString', notify=descriptionChanged)
    def description(self):
        return self.__description

    @pyqtProperty('QString', notify=providedByChanged)
    def provided_by(self):
        return self.__provided_by

    @pyqtProperty('QString', notify=protocolChanged)
    def protocol(self):
        return self.__protocol

    @pyqtProperty('int', notify=channelPsmChanged)
    def channel_psm(self):
        return self.__channel_psm

    @pyqtProperty('QString', notify=svcClassesChanged)
    def svc_classes(self):
        return ', '.join(self.__svc_classes)

    @pyqtProperty('QString', notify=profilesChanged)
    def profiles(self):
        return ', '.join(self.__profiles)

    @pyqtProperty('int', notify=serviceIdChanged)
    def service_id(self):
        return self.__service_id

    def fill(self, properties):
        self.__name = properties["name"]
        self.__host = properties["host"]
        self.nameChanged.emit()

        self.__description = properties["description"]
        self.descriptionChanged.emit()

        self.__provided_by = properties["provider"]
        self.providedByChanged.emit()

        self.__protocol = properties["protocol"]
        self.protocolChanged.emit()

        self.__channel_psm = properties["port"]
        self.channelPsmChanged.emit()

        self.__svc_classes = properties["service-classes"]
        self.svcClassesChanged.emit()

        self.__profiles = properties["profiles"]
        self.profilesChanged.emit()

        self.__service_id = properties["service-id"]
        self.serviceIdChanged.emit()