import QtQuick.Dialogs 1.3
import QtQuick 2.0

Dialog {
    title: qsTr("Nearby devices")

    width: 300
    height: 300

    contentItem: ListView {
        id: nearbyDevicesView

        model: ListModel {
            ListElement {
                name: "IPHONE 5c"
                address: "45:34:23:F5"
                classId: "2342342"
            }

            ListElement {
                name: "NOKIA 3320"
                address: "45:B4:A3:F5"
                classId: "234234232"
            }

            ListElement {
                name: "SAMSUNG J7"
                address: "45:B4:A3:F5"
                classId: "234234232"
            }
        }

        delegate: DeviceDelegate {
            width: nearbyDevicesView.width
        }
    }
}
