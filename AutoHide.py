from PySide2 import QtCore, QtGui, QtWidgets

Vertical = 30
Horizontal =30


dockAreas = {}
dockSituations = {}
mv = FreeCADGui.getMainWindow()

for dock in mv.findChildren(QtWidgets.QDockWidget):
    dockSituations[dock.objectName()] =  dock.isVisible()
    dockAreas[dock.objectName()] =  str(mv.dockWidgetArea(dock)).rpartition('.')[-1]

class autoHide(QtCore.QObject):
    def __init__(self, dock, area, situation):
        self.target = dock
        self.side = False
        super(autoHide, self).__init__(self.target)
        self.target.installEventFilter(self)
        self.visible = self.target.features()
        if (area == 'LeftDockWidgetArea') or (area == 'RightDockWidgetArea'):
            self.target.setFeatures(QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
            self.target.setFixedWidth(Vertical)
            self.side = True
        self.hiden = self.target.features()

    def eventFilter(self, source, event):
        if source is self.target:
            if event.type() == event.Enter:
                print ("Mouse Entered")
                self.target.setFeatures(self.visible)
                if self.side:
                    self.target.setFixedWidth(300)
                else:
                    self.target.setFixedHeight(300)
                return True
            elif event.type() == event.Leave:
                print("Mouse Left")
                self.target.setFeatures(self.hiden)
                if self.side:
                    self.target.setFixedWidth(Vertical)
                else:
                    self.target.setFixedHeight(Horizontal)
                return True
        return super(autoHide, self).eventFilter(source, event)

for key, value in dockAreas.items():
    dock = mv.findChild(QtWidgets.QDockWidget, key)
    situation = dockSituations.get(key)
    area = value
    autoHide(dock, area, situation)
