import QtQuick 2.0
import QtQuick.Controls 1.4

ApplicationWindow {
    id: applicationWindow

    width: 450
    height: 600

    ConnectDialog {
        id: connectDialog
        visible: false
    }

    Rectangle {
        id: header
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        color: '#373737'
        height: 50

        property int fontSize: 20

        Row {
            anchors.left: parent.left
            anchors.leftMargin: 30
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter

            spacing: 15

            Label {
                text: qsTr("Connect")
                font.pixelSize: header.fontSize

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true
                    onClicked: connectDialog.visible = true
                }
            }

            Label {
                text: qsTr("Settings")
                font.pixelSize: header.fontSize
            }

            Label {
                text: qsTr("About")
                font.pixelSize: header.fontSize
            }
        }
    }
}
