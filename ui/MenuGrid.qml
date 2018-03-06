import QtQuick 2.4
import QtQuick.Layouts 1.2

Item {

    property var additional: {
        'nearby': {title: qsTr("Near By"), icon: "images/search.svg", source: "/ui/DiscoveryPage.qml"},
        'info': {title: qsTr("Phone info"), source: "", icon: "images/search.svg"},
        'calendar': {title: qsTr("Calendar"), source: "", icon: "images/calendar.svg"},
        'sms': {title: qsTr("Sms "), source: "/ui/SmsPage.qml", icon: "images/sms.svg"},
        'calls': {title: qsTr("Calls"), source: "", icon: "images/calls.svg"},
        'manager': {title: qsTr("File manager"), source: "", icon: "images/file_manager.svg"}
    }

    property int cellWidth: 100
    property int cellHeight: 100

    Timer {
        id: update_cell_size_timer
        interval: 100
        onTriggered: updateCellSize()
    }

    onWidthChanged: update_cell_size_timer.start()

    function updateCellSize ()
    {
        cellWidth  = Math.max((Math.round(width / gridView.columns)), 100) - 40
        cellHeight = Math.max((Math.round(height / gridView.columns)), 100) - 40
    }

    Grid {
        id: gridView
        anchors.fill: parent
        anchors.margins: 20

        columns: 3
        columnSpacing: 10
        rowSpacing: 10
        spacing: 10

        horizontalItemAlignment: Qt.AlignHCenter
        verticalItemAlignment: Qt.AlignVCenter

        Repeater {
            model: BTNotifier.services

            Item {
                width: cellWidth
                height: 100

                ColumnLayout {
                    anchors.fill: parent

                    Image {
                        width: 40
                        height: 40
                        source: additional[name].icon

                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 40
                    }

                    Text {
                        text: additional[name].title
                        horizontalAlignment:  Text.AlignHCenter
                        Layout.alignment: Qt.AlignHCenter
                    }
                }

                Rectangle {
                    width: 20
                    height: 20
                    radius: 20
                    color: 'red'

                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.margins: 10

                    visible: (value > 0)

                    Text {
                        anchors.centerIn: parent
                        text: (value < 9) ? value : '9+'
                        color: 'white'
                        font.bold: true
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        var url = additional[name].source
                        if (url.length) {
                            console.log('Open url ', AppPath, url)
                            stackView.navigateTo(additional[name].source)
                        }
                        else
                            console.log('Page source not set')
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        console.log('Menu grid completed')
    }
}
