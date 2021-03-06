import QtQuick 2.0
import QtQuick.Controls 2.0
import "."

Item {
    height: layout.implicitHeight + 20

    SystemPalette { id: myPalette; colorGroup: SystemPalette.Active }

    Theme {
        id: theme
    }

    Rectangle {
        anchors.fill: parent
        color: hoverArea.containsMouse

        Behavior on color { ColorAnimation { duration: 250 } }
    }

    Image {
        id: devicePicture

        width: 48
        height: 48

        source: "images/device_%1.svg".arg(type)
        smooth: true
        antialiasing: true

        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
    }

    Column {
        id: layout
        anchors.left: devicePicture.right
        anchors.right: actions.left
        anchors.top: devicePicture.top

        Label {
            text: name
            font.bold: true
            font.pixelSize: theme.titlePixelSize
            color: myPalette.windowText
        }

        Label {
            text: qsTr("   <b>MAC</b>: %1").arg(address)
            font.bold: true
            font.pixelSize: theme.subtitlePixelSize
            color: myPalette.windowText
        }

        Label {
            text: qsTr("   <b>ID</b>: %1").arg(classId)
            font.bold: true
            font.pixelSize: theme.subtitlePixelSize
            color: myPalette.windowText
        }
    }

    Item {
        id: actions

        width: 40

        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter

        opacity: hoverArea.containsMouse ? 1 : 0

        Behavior on opacity { SmoothedAnimation { duration: 250 } }
    }

    MouseArea {
        id: hoverArea
        hoverEnabled: true
        propagateComposedEvents: false
    }
}
