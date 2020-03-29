from PySide2 import QtCore, QtGui, QtWidgets

dockAreas = {}
dockSituations = {}
mv = FreeCADGui.getMainWindow()

for dock in mv.findChildren(QtWidgets.QDockWidget):
    dockSituations[dock.objectName()] =  dock.isVisible()
    dockAreas[dock.objectName()] =  str(mv.dockWidgetArea(dock)).rpartition('.')[-1]

class autoHide(QtCore.QObject):
    def __init__(self, dock, area):
        self.side = False
        self.target = dock
        super(autoHide, self).__init__(self.target)
        self.target.installEventFilter(self)
        self.visible = self.target.features()
        self.orgSize = self.target.sizeHint().height()
        if (area == 'LeftDockWidgetArea') or (area == 'RightDockWidgetArea'):
            self.orgSize = self.target.sizeHint().width()
            self.target.setFeatures(QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
            self.side = True
        self.hiden = self.target.features()
        self.TBHeight = self.target.style().pixelMetric(QtWidgets.QStyle.PM_TitleBarHeight)
        if self.side:
            self.target.setFixedWidth(self.TBHeight)
        else:
            self.target.setFixedHeight(self.TBHeight)

    def eventFilter(self, source, event):
        if source is self.target:
            if event.type() == event.Enter:
                self.target.setFeatures(self.visible)
                if self.side:
                    self.target.setFixedWidth(self.orgSize)
                else:
                    self.target.setFixedHeight(self.orgSize)
                return True
            elif event.type() == event.Leave:
                self.target.setFeatures(self.hiden)
                if self.side:
                    self.target.setFixedWidth(self.TBHeight)
                else:
                    self.target.setFixedHeight(self.TBHeight)
                return True
        return super(autoHide, self).eventFilter(source, event)

for key, value in dockAreas.items():
    dock = mv.findChild(QtWidgets.QDockWidget, key)
    situation = dockSituations.get(key)
    area = value
    autoHide(dock, area)
