import threading
import bluetooth

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QSettings, QFile
from PyQt5.QtQml import QQmlListProperty
from PyQt5.QtBluetooth import QBluetoothTransferManager, QBluetoothTransferRequest, QBluetoothAddress

import Device
import Sms
import SendSmsThread
import DiscoveryThread
import ConnectDeviceThread


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
    __device_state = None
    __threads = []
    __transfer_manager = None

    """ Signals """
    searchingChanged = pyqtSignal()
    nearByDevicesChanged = pyqtSignal()
    servicesFound = pyqtSignal()
    notifierChanged = pyqtSignal()
    discoveringChanged = pyqtSignal()
    deviceChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__transfer_manager = QBluetoothTransferManager()
        self.__device = Device.Device()
        self.__settings = QSettings("PCSuite", "maxvanceffer")

        self.__settings.beginGroup("device")
        all_groups = self.__settings.allKeys()
        if len(all_groups):
            self.__device.host = self.__settings.value('host')
            self.__device.name = self.__settings.value('name')
            self.__device.class_id = self.__settings.value('class_id')

        self.__settings.endGroup()
        if self.__device.is_empty() is False:
            self.find_device_state(self.__device)

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

        self.__task = DiscoveryThread.DiscoveryThread()
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
        # print('V is ')

    @pyqtSlot()
    def find_device_state(self, device):
        if device is None or device.is_empty():
            print('Device is empty, can check it\'s state')
            return

        if self.__device_state and self.__device_state.device.host == device.host:
            print('Already scanning device for it\'s state')
            return

        print('Start search for device [%s] status' % device.host)
        self.__device_state = ConnectDeviceThread.ConnectDeviceThread(self)
        self.__device_state.device = self.__device
        self.__device_state.done.connect(self.find_device_state_found)
        self.__device_state.run()

    @staticmethod
    def find_device_state_found():
        print('Device status found ')

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
        sms = Sms.Sms(self)
        sms.to_phone = to
        sms.from_phone = '06875989'
        sms.message = message
        sms.device = self.__device

        sms_thread = SendSmsThread.SendSmsThread()

        sms_thread.done.connect(sms_thread.terminate)
        sms_thread.error.connect(sms_thread.terminate)

        sms_thread.sms = sms
        sms_thread.run()

    @pyqtSlot(str)
    def send_file(self, path):
        print('Sending file %s' % path)

        address = QBluetoothAddress(self.__device.host)
        request = QBluetoothTransferRequest(address)
        file = QFile(path)
        reply = self.__transfer_manager.put(request, file)
        # if reply:
            # reply.transferProgress.connect(self.progress)
        # else:
            # print('oooops no reply')

    def progress(self, current, total):
        print('Progress send %d' % current)
        print('Progress send %d' % total)
