import threading
import bluetooth
import Device
import json
from PyQt5.QtBluetooth import QBluetoothAddress, QBluetoothTransferRequest

from PyQt5.QtCore import pyqtSignal, QThread


class ConnectDeviceThread(QThread):
    done = pyqtSignal()
    error = pyqtSignal(int)
    dongleNotFound = pyqtSignal()

    NO_SERVICE_FOUND = 1001

    device = None
    retry = 4

    def run(self):
        self.device.updating = True

        services = []
        while len(services) is 0 and self.retry > 0:
            services = bluetooth.find_service(address=self.device.host)
            if len(services) > 0:
                self.retry = 0

        if len(services) is 0:
            print('No services found for device, stop connect')
            self.device.updating = False
            self.error.emit(self.NO_SERVICE_FOUND)
            self.done.emit()
            return

        a = json.dumps(services)

        self.device.services = services

        # If device not yet know it's manufacturer it's first connect
        if len(self.device.vendor) == 0:
            pnp_info_service = self.device.get_service_by_name('PnPInformation')
            if pnp_info_service:
                print('PnpService found')

        self.device.updating = False
