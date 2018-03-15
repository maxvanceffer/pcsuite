import QtQuick 2.0

Image {
    id: btn
    clip: true
    smooth: true
    width: size
    height: size

    property double size: 30

    signal clicked()

    Ink {
        anchors.fill: parent
        onClicked: btn.clicked()
        circular: true
        centered: true
        cursorShape: Qt.PointingHandCursor
    }
}