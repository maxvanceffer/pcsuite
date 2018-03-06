import QtQuick 2.0
import QtQuick.Controls 1.3
import QtGraphicalEffects 1.0

ApplicationWindow {
    id: applicationWindow
    title: qsTr("PC Suite")
    width: 650
    height: 600

    Theme {
        id: theme
    }

//    ConnectDialog {
//        id: connectDialog
//        visible: false
//    }

    Rectangle {
        id: header

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
//        visible: false

        color: theme.headerColor
        height: 50

        property int fontSize: 20

        Text {
            text: qsTr("PC Suite")

            anchors.left: parent.left
            anchors.leftMargin: 30
            anchors.verticalCenter: parent.verticalCenter
            font.pixelSize: theme.titlePixelSize
            color: theme.headerTextColor
        }

        layer.enabled: true
        layer.effect: DropShadow {
            color: Qt.rgba(0.169, 0.169, 0.169, 0.3)
            transparentBorder: true
            horizontalOffset: 8
            verticalOffset: 8
        }
    }

    Sidebar {
        id: sidebar
        width: 200

        anchors.left: parent.left
        anchors.top: header.bottom
        anchors.bottom: parent.bottom
    }

    StackView {
        id: stackView
        clip: true
        anchors.left: sidebar.right
        anchors.top: header.bottom
        anchors.bottom: footer.top
        anchors.right: parent.right

        initialItem: MenuGrid {}

        function navigateTo(source, properties) {
            properties = properties || {}
            var parts = ['file:/', AppPath, source]
            console.log('Open path ', parts.join('/'))
            stackView.push(parts.join('/'), properties)
        }

        function back() {
            if (depth === 1) return

            pop()
        }
    }

    Footer {
        id: footer

        height: 60

        anchors.left: sidebar.right
        anchors.right: parent.right
        anchors.bottom: parent.bottom
    }

    Component.onCompleted: {
        visible = true
        console.info('Root window created')

        if (BTManager.my_device.host && BTManager.my_device.host.length) {
            BTManager.my_device.update()
        }
    }
}
