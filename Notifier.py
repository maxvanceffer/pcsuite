from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty

# This is the type that will be registered with QML.  It must be a
# sub-class of QObject.
class ServiceType(QObject):

    valueChanged = pyqtSignal()
    nameChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialise the value of the properties.
        self._name = ''
        self._value = 0

    # Define the getter of the 'name' property.  The C++ type of the
    # property is QString which Python will convert to and from a string.
    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name

    # Define the setter of the 'name' property.
    @name.setter
    def name(self, name):
        self._name = name

    # Define the getter of the 'shoeSize' property.  The C++ type and
    # Python type of the property is int.
    @pyqtProperty(int, notify=valueChanged)
    def value(self):
        return self._value

    # Define the setter of the 'shoeSize' property.
    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = value
            self.valueChanged.emit()

    def setup(self, name, value=0):
        self._name = name
        self._value = value
        return self


class Notifier(QObject):
    __services = []
    __tooltip = ''

    nearByChanged = pyqtSignal()
    servicesChanged = pyqtSignal()
    tooltipChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__services.append(ServiceType(self).setup('nearby'))
        self.__services.append(ServiceType(self).setup('info'))
        self.__services.append(ServiceType(self).setup('calendar'))
        self.__services.append(ServiceType(self).setup('sms'))
        self.__services.append(ServiceType(self).setup('calls'))
        self.__services.append(ServiceType(self).setup('manager'))

    @pyqtProperty(QQmlListProperty, notify=servicesChanged)
    def services(self):
        return QQmlListProperty(ServiceType, self, self.__services)

    def update_service(self, name, value):
        for service in self.__services:
            if service.name == name:
                service.value = value
                break

    @pyqtProperty('QString', notify=tooltipChanged)
    def tooltip(self):
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, text):
        self.__tooltip = text
        self.tooltipChanged.emit()
