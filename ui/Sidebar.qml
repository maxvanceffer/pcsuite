import QtQuick 2.0
import QtQuick.Controls 1.3

Item {
    Theme {
        id: theme
    }

    Rectangle {
        anchors.fill: parent
        color: theme.sidebarColor
    }

    Image {
        id: my_device_picture
        source: MyDevice.image

        smooth: true
        fillMode: Image.PreserveAspectFit

        width: 240 / 2.5
        height: 494 / 2.5

        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 20

        BusyIndicator {
            width: 20
            height: 20
            visible: running
            running: BTManager.my_device.updating
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 10
        }

        Image {
            source: BTManager.my_device.available ? "images/online.png" : "images/offline.png"
            width: 20
            height: 20
            smooth: true
            fillMode: Image.PreserveAspectFit
            visible: (BTManager.my_device.host && BTManager.my_device.host.length) || !BTManager.my_device.updating

            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 10

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {
                    var text = ''
                    if (BTManager.my_device.available && BTManager.my_device.connected)
                        text = qsTr("%1 near by, and connected").arg(BTManager.my_device.name)
                    else if (BTManager.my_device.available && !BTManager.my_device.connected)
                        text = qsTr("%1 near by, but not yet connected").arg(BTManager.my_device.name)
                    else
                        text = qsTr("%1 not found. Maybe bluetooth is OFF").arg(BTManager.my_device.name)

                    BTNotifier.tooltip = text
                }

                onExited: BTNotifier.tooltip = ''
            }
        }
    }

    Label {
        text: qsTr("No device selected")
        anchors.top: my_device_picture.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 20
        color: theme.sidebarTextColor
        visible: !BTManager.my_device.name || BTManager.my_device.name.length === 0
    }

    Label {
        text: BTManager.my_device.name
        anchors.top: my_device_picture.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 20
        color: theme.sidebarTextColor
        visible: (BTManager.my_device && BTManager.my_device.name != undefined && BTManager.my_device.name.length > 0)
    }
}