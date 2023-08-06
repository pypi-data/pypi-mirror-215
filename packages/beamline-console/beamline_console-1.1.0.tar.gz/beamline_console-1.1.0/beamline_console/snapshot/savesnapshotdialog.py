import json
import os
import logging

from PyQt5 import QtWidgets, QtGui

from beamline_console.constants import APP_NAME
from beamline_console.snapshot.beamsnapshot import BeamlineSnapshot
from beamline_console.devices.motordevice import MotorBasedDevice
from beamline_console.gui.SaveSnapshotDialog_ui import Ui_SaveSnapshotDialog

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class SaveSnapshotDialog(QtWidgets.QDialog):

    # ----------------------------------------------------------------------
    def __init__(self, beamline_hal, selection, snapshot_manager, parent=None):
        super().__init__(parent)

        self.beamline_hal = beamline_hal
        self.snapshot_manager = snapshot_manager
        
        self.device_selection = None
        if selection is not None:
            self.device_selection = [str(name) for name in json.loads(str(selection))["devices"]]

        self.columns = ["Motor Name", "Save", "Step"]
        self.motor_tuples = []

        self._ui = Ui_SaveSnapshotDialog()
        self._ui.setupUi(self)

        self._ui.btnSaveSnapshot.clicked.connect(self.save_snapshot)
        self._ui.btnSelectAll.clicked.connect(self.select_all)
        self._ui.chbShowAllMotors.stateChanged.connect(self.show_all_toggled)

        self.show_motors(self.device_selection)

        self.select_all()

    # ----------------------------------------------------------------------
    def show_motors(self, selection=None):
        # called when devicewidget sends save_snapshot signal
        self._ui.twDevices.clear()
        self._ui.twDevices.setColumnCount(len(self.columns))
        self._ui.twDevices.setHorizontalHeaderLabels(self.columns)

        self.motor_tuples = []
        for dev_idx, (dev_name, dev_handle) in enumerate(self.beamline_hal.device_map.items()):
            if (isinstance(dev_handle, MotorBasedDevice) and
                (selection is None or dev_name in selection)):
                for motor in list(dev_handle.motors.values()):
                    chb_save = QtWidgets.QCheckBox(self._ui.twDevices)
                    sb_step = QtWidgets.QSpinBox(self._ui.twDevices)
                    sb_step.setEnabled(False)
                    sb_step.setRange(1, 1000)
                    sb_step.setValue(1)
                    chb_save.toggled.connect(sb_step.setEnabled)

                    self.motor_tuples.append((dev_name, motor.name,
                                              chb_save, sb_step, self._next_color(dev_idx)))

        self._ui.twDevices.setRowCount(len(self.motor_tuples))

        for motor_idx, motor_tuple in enumerate(self.motor_tuples):
            #name_item = QtWidgets.QTableWidgetItem(motor_tuple[1])
            name_item = QtWidgets.QTableWidgetItem("{}/{}".format(*motor_tuple[:2]))    # full name?
            name_item.setBackground(QtGui.QBrush(QtGui.QColor(*motor_tuple[4])))
            
            self._ui.twDevices.setItem(motor_idx, 0, name_item)
            self._ui.twDevices.setCellWidget(motor_idx, 1, motor_tuple[2])
            self._ui.twDevices.setCellWidget(motor_idx, 2, motor_tuple[3])

        self._ui.twDevices.resizeColumnsToContents()
        self._ui.twDevices.resizeRowsToContents()
        self._ui.twDevices.setColumnWidth(0, 180)

    # ----------------------------------------------------------------------
    def show_all_toggled(self, flag):
        self.show_motors(None if flag else self.device_selection)

    # ----------------------------------------------------------------------
    def select_all(self):
        n_selected = 0
        for row in range(self._ui.twDevices.rowCount()):
            n_selected += 1 if self._ui.twDevices.cellWidget(row, 1).isChecked() else 0

        flag = not (n_selected == self._ui.twDevices.rowCount())
        for row in range(self._ui.twDevices.rowCount()):
            self._ui.twDevices.cellWidget(row, 1).setChecked(flag)

    # ----------------------------------------------------------------------
    def save_snapshot(self):
        snapshot_name = str(self._ui.leSnapshotName.text()).strip()

        if not BeamlineSnapshot().is_valid_name(snapshot_name):
            QtWidgets.QMessageBox.warning(self, "Error",
                                      "Snapshot name may consist of \
(alphanumeric_-=) characters only and cannot contain word 'general'!",
                                      QtWidgets.QMessageBox.Ok)
            return

        snapshot = BeamlineSnapshot(name=snapshot_name)

        for _, motor_tuple in enumerate(self.motor_tuples):                 # to be saved motors
            enabled_widget = motor_tuple[2]
            if enabled_widget.isChecked():
                step_widget = motor_tuple[3]

                dev_name, motor_name = motor_tuple[:2]
                position = self.beamline_hal.motor_position(f"{dev_name}/{motor_name}")
                snapshot.add_item(dev_name, motor_name, position, step_widget.value())

        if snapshot.empty():
            QtWidgets.QMessageBox.warning(self, "Error", "Select at least one motor!",
                                      QtWidgets.QMessageBox.Ok)
            return

        try:
            self.snapshot_manager.add_snapshot(snapshot)
            filename = f"{os.path.join(self.snapshot_manager.snapshots_dir(), snapshot_name)}.xml"
            snapshot.save(filename)
        except RuntimeError as err:
            # report_error() TODO
            QtWidgets.QMessageBox.warning(self, "Error", f"{str(err)}!",
                                      QtWidgets.QMessageBox.Ok)
        else:
            super().accept()

    # ----------------------------------------------------------------------
    @staticmethod
    def _next_color(devIdx):
        colors = [(220, 250, 220),
                  (250, 220, 220),
                  (250, 250, 220),
                  (220, 220, 250)]
        
        return colors[devIdx % len(colors)]