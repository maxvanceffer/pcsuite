import threading
import bluetooth

from PyQt5.QtCore import pyqtSignal, QThread


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
