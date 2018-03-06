import threading
import bluetooth

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QThread, QSettings
from PyQt5.QtQml import QQmlListProperty

import Device


class DiscoveryThread(QThread):

    done = pyqtSignal()
    iteration = pyqtSignal(list)
    dongleNotFound = pyqtSignal(bool)

    drop_cache = True

    def run(self):
        print("discovery thread started ", threading.get_ident())
        event = threading.Event()
        try:
            nearby_devices = bluetooth.discover_devices(lookup_names=True, flush_cache=self.drop_cache, lookup_class=True)
            print('found devices %d ' % len(nearby_devices))
            self.iteration.emit(nearby_devices)
            event.wait()
            self.done.emit()
            self.dongleNotFound.emit(True)
        except OSError as e:
            print('Bluetooth library error %s' % e)
            self.dongleNotFound.emit(False)
            event.wait()
            self.done.emit()


def my__discover(searcher):
    print("start discovery in thread ", threading.get_ident())
    try:
        import bluetooth
        nearby_devices = bluetooth.discover_devices(lookup_names=True, flush_cache=False, lookup_class=True)
        print("found %d devices" % len(nearby_devices))

        searcher.found([])
    except Exception as e:
        print(e)
        searcher.found([])


def my__services(target):
    if target == "all": target = None

    services = bluetooth.find_service(address=target)

    if len(services) > 0:
        print("found %d services on %s" % (len(services), target))
        print("")
    else:
        print("no services found")

    print('Callback')
    return services


def discover_device_status(device):
    nearby_devices = bluetooth.discover_devices(lookup_names=True, flush_cache=False, lookup_class=True, duration=10)
    print("found %d devices near by" % len(nearby_devices))

    for host, name, class_id in nearby_devices:
        if host == device.host():
            print('Target device found in range')
            device.set_available(True)

            # Search device services
            services = bluetooth.find_service(address=device.host())

            if len(services) > 0:
                print("found %d services on %s" % (len(services), device.host()))
                print("")
                device.set_services(services)
            else:
                print("no services found for % device" % device.host())


class Manager(QObject):
    """ Bluez tools """
    __searching = False
    __discovering = False
    __near_by = []
    __services = []
    __notifier = None
    __device = None
    __settings = None
    __has_dongle = True

    ''' Threads '''
    __task = None

    """ Signals """
    searchingChanged = pyqtSignal()
    nearByDevicesChanged = pyqtSignal()
    servicesFound = pyqtSignal()
    notifierChanged = pyqtSignal()
    discoveringChanged = pyqtSignal()
    deviceChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__device = Device.Device()

        self.__settings = QSettings("PCSuite", "maxvanceffer")

        all_groups = self.__settings.allKeys()
        if 'device' in all_groups:
            self.__settings.beginGroup("device")

            self.__device.host = self.__settings.value('host')
            self.__device.name = self.__settings.value('name')
            self.__device.class_id = self.__settings.value('class_id')

            self.__settings.endGroup()

    def notifier(self):
        return self.__notifier

    def set_notifier(self, notifier):
        self.__notifier = notifier
        self.notifierChanged.emit()

    @pyqtProperty('bool', notify=discoveringChanged)
    def discovering(self):
        return self.__discovering

    @pyqtProperty('bool', notify=searchingChanged)
    def searching(self):
        return self.__searching

    @pyqtProperty('QVariant', notify=deviceChanged)
    def my_device(self):
        return self.__device

    @my_device.setter
    def my_device(self, device):
        self.__device = device
        self.select_device(device)
        self.deviceChanged.emit()

    @pyqtProperty(QQmlListProperty, notify=nearByDevicesChanged)
    def nearby_devices(self):
        print("build near by devices ", threading.get_ident())
        devices = []
        for host, name, class_id in self.__near_by:
            d = Device.Device(self)
            d.name = name
            d.host = host
            d.class_id = class_id
            d.available = True
            devices.append(d)

        return QQmlListProperty(Device.Device, self, devices)

    @pyqtProperty('QVariant', notify=servicesFound)
    def services(self):
        return self.__services

    @pyqtSlot()
    def search(self, drop_cache=False):
        if self.discovering or self.__has_dongle is False:
            print('Already searching or no dongle present')
            return

        print('Start search in thread ', threading.get_ident())
        self.__discovering = True
        self.discoveringChanged.emit()

        self.__near_by.clear()
        self.nearByDevicesChanged.emit()

        self.__task = DiscoveryThread()
        self.__task.drop_cache = drop_cache
        self.__task.done.connect(self.__task.terminate)
        self.__task.dongleNotFound.connect(self.dongle_status)
        self.__task.iteration.connect(self.__found)
        self.__task.start()

        print('searched')

    @pyqtSlot()
    def service(self, target=''):
        if self.searching:
            print('Already searching')
            return

        print('Start search %s' % target)
        self.__searching = True
        self.searchingChanged.emit()
        self.__services.clear()

        # self.__pool.map_async(my__services, args=(self.__services_found, self.__services_done, target))
        # x = Process(target=my__services, args=(self.__services_found, self.__services_done, target))
        # x.start()

        self.res = self.__pool.apply_async(my__services, (target, ), callback=self.__services_found)
        # print('V is ')

    @pyqtSlot()
    def find_device_state(self, device):
        print('Start search for device [%s] status' % device.host())
        self.__pool.apply_async(discover_device_status, (device, ), callback=self.find_device_state_found)

    @staticmethod
    def find_device_state_found(device):
        print('Device status found ', device.name())
        device.set_updating(False)

    @pyqtSlot()
    def local_address(self):
        return ''

    @pyqtSlot()
    def select_device(self, device):
        self.__settings.beginGroup('device')
        self.__settings.setValue('host', device.host)
        self.__settings.setValue('image', device.image)
        self.__settings.setValue('class_id', device.class_id)
        self.__settings.setValue('name', device.name)
        self.__settings.endGroup()

    def __found(self, devices):
        print("search near by devices done ", threading.get_ident())
        # self.__discovery_thread.join()
        self.__near_by = devices
        self.nearByDevicesChanged.emit()

        found = False
        if len(self.__device.host):
            for host, name, class_id in devices:
                if self.__device.host == str(host) and self.__device.class_id == str(class_id):
                    found = True

        self.__device.available = found

        if self.__notifier:
            self.__notifier.update_service('nearby', len(devices))

        self.__discovering = False
        self.discoveringChanged.emit()

    def __services_found(self, services):
        print('Service discovery done')
        self.__services = services
        self.__services_done()

    def __services_done(self):
        self.__searching = False
        self.searchingChanged.emit()
        self.servicesFound.emit()

    @pyqtSlot(bool)
    def dongle_status(self, status):
        self.__has_dongle = status
        if self.__has_dongle is False:
            self.__searching = False
            self.__discovering = False
            self.discoveringChanged.emit()
            self.searchingChanged.emit()

            self.my_device.available = False
            self.my_device.connected = False

    @pyqtSlot(str, str)
    def send_sms(self, to, message):
        sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sockfd.connect((self.__device.host, 1))  # BT Address
        res = sockfd.send('ATZ\r')
        res = sockfd.send('AT+CMGF=1\r')
        res = sockfd.send('AT+CMGS=”'+to+'”\r')  # TO PhoneNumber
        res = sockfd.send(message+'\n')
        res = sockfd.send(chr(26))  # CTRL+Z
        sockfd.close()

