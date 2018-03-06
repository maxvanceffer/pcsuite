import QtQuick 2.0

Image {
    id: btn
    clip: true
    smooth: true
    width: 30
    height: 30

    signal clicked()

    Ink {
        anchors.fill: parent
        onClicked: btn.clicked()
        circular: true
        centered: true
        cursorShape: Qt.PointingHandCursor
    }
}