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

    TextEdit {
        id: sms_text_edit

        width: 140
        height: 50

        anchors.left: parent.left
        anchors.top: controls.bottom
        anchors.margins: 10
    }

    Button {
        anchors.top: sms_text_edit.bottom
        anchors.right: sms_text_edit.right
        onClicked: BTManager.send_sms(sms_text_edit.displayText, '060047856')
    }
}
