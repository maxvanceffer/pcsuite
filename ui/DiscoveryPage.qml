import QtQuick 2.4
import QtQuick.Controls 1.2

Item {
    property string pageTitle: qsTr("Near by devices")

    Theme {
        id: theme
    }

    Item {
        id: controls

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 10

        height: 40

        RadiusButton {
            source: "images/up.svg"

            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 30

            transform: Rotation { angle: -90 }

            onClicked: {
                console.log('clicked back')
                stackView.back()
            }
        }

        RadiusButton {
            source: "images/search.svg"

            anchors.right: parent.right
            anchors.top: parent.top

            visible: !BTManager.discovering

            onClicked: {
                console.log('clicked search')
                BTManager.search()
            }
        }
    }

    ListView {
        id: devicesListView

        clip: true

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.top: controls.bottom
        anchors.margins: 10

        model: BTManager.nearby_devices

        delegate: Item {
            width: devicesListView.width; height: 55;

            Item {
                anchors.fill: parent
                anchors.topMargin: 10
    //            Rectangle {
    //                anchors.fill: parent
    //                color: Qt.rgba(1.000, 0.514, 0.133, 0.4)
    //            }

                Image {
                    id: device_icon
                    source: "images/device_%1.svg".arg(type)
                    width: 40
                    height: 40

                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    id: title_text
                    text: name
                    font.pixelSize: theme.titlePixelSize
                    font.bold: true
                    anchors.left: device_icon.right
                    anchors.leftMargin: 20
                    anchors.right: inline_controls.left
                }

                Text {
                    text: qsTr("Address: %1").arg(host)
                    font.pixelSize: theme.subtitlePixelSize
                    anchors.left: device_icon.right
                    anchors.right: inline_controls.left
                    anchors.top: title_text.bottom
                    anchors.leftMargin: 20
                    anchors.topMargin: 5
                }

                Item {
                    id: inline_controls
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 7

                    width: 80
                    height: 45

                    Row {
                        anchors.fill: parent
                        spacing: 10

                        RadiusButton {
                            source: "images/select.svg"
                            width: 32
                            height: 32
                            visible: BTManager.my_device.host != host
                            onClicked: {
                                console.log('clicked select', modelData.host)
                                BTManager.my_device = modelData
                            }
                        }

                        RadiusButton {
                            source: "images/services.svg"

                            width: 32
                            height: 32

                            visible: !BTManager.discovering

                            onClicked: {
                                console.log('clicked search')
                            }
                        }
                    }
                }
            }
        }
    }
}