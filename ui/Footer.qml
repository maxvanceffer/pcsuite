import QtQuick 2.4
import QtQuick.Controls 1.3

Item {

    Theme {
        id: theme
    }

    Rectangle {
        anchors.fill: parent
        color: theme.footerColor
    }

    Item {
        id: near_by_updating

        anchors.fill: parent
        visible: BTManager.discovering && !tool_tip.visible

        BusyIndicator {
            id: busy_indicator
            width: 18
            height: 18

            anchors.left: parent.left
            anchors.margins: 10
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            text: qsTr("Updating near by devices...")
            color: theme.footerTextColor

            anchors.left: busy_indicator.right
            anchors.margins: 10
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    Item {
        id: tool_tip

        anchors.fill: parent
        visible: BTNotifier.tooltip && BTNotifier.tooltip.length

        Text {
            text: BTNotifier.tooltip
            color: theme.footerTextColor

            anchors.left: parent.left
            anchors.margins: 10
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}