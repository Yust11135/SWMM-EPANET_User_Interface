from PyQt4 import QtCore, QtGui
from frmMapDimensionsDesigner import Ui_frmMapDimensionsDesigner

class frmMapDimensions(QtGui.QDialog):
    def __init__(self, main_form=None, *args):
        self._main_form = main_form
        QtGui.QDialog.__init__(self)
        self.ui = Ui_frmMapDimensionsDesigner()
        self.ui.setupUi(self)
        self.options = None
        if args is not None and len(args) > 0:
            self.options = args[0]
        self.ui.rdoUnitDegrees.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitNone.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitFeet.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitMeters.toggled.connect(self.changeLinearMapUnit)
        self.ui.txtULx.textChanged.connect(lambda:self.checkCoords(self.ui.txtULx.text()))
        self.ui.txtULy.textChanged.connect(lambda:self.checkCoords(self.ui.txtULy.text()))
        self.ui.txtLRx.textChanged.connect(lambda:self.checkCoords(self.ui.txtLRx.text()))
        self.ui.txtLRy.textChanged.connect(lambda:self.checkCoords(self.ui.txtLRy.text()))
        self.ui.buttonBox.accepted.connect(self.setExtent)
        self.setupOptions()

    def setExtent(self):
        if self._main_form is None:
            return
        if self._main_form.map_widget is None:
            return
        val1, is_val_good1 = self.floatTryParse(self.ui.txtULx.text())
        val2, is_val_good2 = self.floatTryParse(self.ui.txtULy.text())
        val3, is_val_good3 = self.floatTryParse(self.ui.txtLRx.text())
        val4, is_val_good4 = self.floatTryParse(self.ui.txtLRy.text())

        if is_val_good1 and is_val_good2 and is_val_good3 and is_val_good4:
            self._main_form.map_widget.coord_origin.float_x = val1
            self._main_form.map_widget.coord_origin.float_y = val2
            self._main_form.map_widget.coord_fext.float_x = val3
            self._main_form.map_widget.coord_fext.float_x = val4
        pass

    def setupOptions(self):
        if self._main_form is None:
            return
        if self._main_form.map_widget is None:
            return
        lu = self._main_form.map_widget.mapLinearUnit
        if lu == 'none':
            self.ui.rdoUnitNone.setChecked(True)
        elif lu == 'feet':
            self.ui.rdoUnitFeet.setChecked(True)
        elif lu == 'meters':
            self.ui.rdoUnitMeters.setChecked(True)
        elif lu == 'degrees':
            self.ui.rdoUnitDegrees.setChecked(True)

        self.ui.txtULx.setText('{:.3f}'.format(self._main_form.map_widget.coord_origin.float_x))
        self.ui.txtULy.setText('{:.3f}'.format(self._main_form.map_widget.coord_origin.float_y))
        self.ui.txtLRx.setText('{:.3f}'.format(self._main_form.map_widget.coord_fext.float_x))
        self.ui.txtLRy.setText('{:.3f}'.format(self._main_form.map_widget.coord_fext.float_x))

    def floatTryParse(self, value):
        try:
            return float(value), True
        except ValueError:
            return value, False

    def changeLinearMapUnit(self):
        if self._main_form is None:
            return
        if self._main_form.map_widget is None:
            return
        if self.ui.rdoUnitDegrees.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'degrees'
        elif self.ui.rdoUnitMeters.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'meters'
        elif self.ui.rdoUnitNone.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'none'
        elif self.ui.rdoUnitFeet.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'feet'
        return

    def checkCoords(self, avalue):
        if len(avalue) ==0:
            return
        if len(avalue) == 1 and avalue[0] == '-':
            return
        val, value_is_good = self.floatTryParse(avalue)
        if not value_is_good:
            msg = QtGui.QMessageBox()
            msg.setWindowTitle('Map Dimension')
            msg.setText('Coordinate value is not valid numeric value.')
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
            del msg
        pass


