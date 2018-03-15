import Device
import Sms
import threading
import bluetooth

from PyQt5.QtCore import pyqtSignal, QThread


class SendSmsThread(QThread):
    done = pyqtSignal()
    error = pyqtSignal(int)
    dongleNotFound = pyqtSignal()

    NO_SERVICE_FOUND = 1001

    sms = None

    def run(self):
        print('Start send sms')
        if self.sms is None or self.sms.is_empty():
            print('Missing required argument sms, or not sms is empty')
            self.done.emit()
            self.terminate()
            return

        address = self.sms.device.host
        dun_port = 0

        services = bluetooth.find_service(address=address)

        # for service in services:
        #     if service["name"] == "Dial-up Networking":
        #         dun_port = service["port"]
        #         print("BT Profile: %s" % service["name"])
        #         print(" Host: %s" % service["host"])
        #         print(" Description: %s" % service["description"])
        #         print(" Provided By: %s" % service["provider"])
        #         print(" Protocol: %s" % service["protocol"])
        #         print(" channel/PSM: %s" % service["port"])
        #         print(" service classes: %s " % service["service-classes"])
        #         print(" profiles: %s " % service["profiles"])
        #         print(" service id: %s " % service["service-id"])
        dial_up = bluetooth.find_service(address=address, uuid=bluetooth.DIALUP_NET_CLASS)
        if len(dial_up):
            dun_port = dial_up[0]['port']

        if dun_port is 0:
            self.error.emit(self.NO_SERVICE_FOUND)
            self.done.emit()
            self.terminate()
            return

        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        connection = socket.connect((address, dun_port))

        socket.send("AT\r")
        print(socket.recv(1024))

        socket.send("AT+CMGF=1\r")
        print(socket.recv(1024))
        socket.send('AT+CMGS="'+self.sms.to_phone+'"\r')
        print(socket.recv(1024))
        socket.send(self.sms.message + chr(26))
        print(socket.recv(1024))
        print(socket.recv(1024))
        socket.close()

        self.sms.complete = True
        self.done.emit()
