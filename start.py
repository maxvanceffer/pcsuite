from sys import argv

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

import os
import Manager
import Device
import Notifier


def main():
    app = QGuiApplication(argv)

    qmlRegisterType(Manager.Manager, 'BTManager', 1, 0, 'BTManager')
    qmlRegisterType(Notifier.Notifier, 'BTNotifier', 1, 0, 'BTNotifier')
    qmlRegisterType(Device.Device, 'Device', 1, 0, 'Device')

    print('Create my device')

    notifier = Notifier.Notifier()
    manager = Manager.Manager()
    manager.set_notifier(notifier)

    print('Bluetooth manager create')

    path = os.path.dirname(__file__)
    print('Detect run path')

    print('Run GUI')
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('AppPath', path)
    engine.rootContext().setContextProperty('MyDevice', manager.my_device)
    engine.rootContext().setContextProperty('BTManager', manager)
    engine.rootContext().setContextProperty('BTNotifier', notifier)
    engine.load('ui/Main.qml')

    print('Start search for near by devices')
    manager.search(True)

    print('Execute app')
    exit(app.exec_())


main()
