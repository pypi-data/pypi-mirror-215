"""Manage DeviceGraphicsItem objects representing beamline devices.
This class is tightly coupled with BeamlineGraphicsView.
"""

from PyQt5 import QtWidgets, QtCore

from beamline_console.logger.logit import Logit
from beamline_console.devicecontrol.deviceitem.devicegraphicsitem import DeviceGraphicsItem


# ----------------------------------------------------------------------
class BeamlineGraphicsScene(QtWidgets.QGraphicsScene, Logit):
    """
    """
    device_selection_changed = QtCore.pyqtSignal(list)

    # ----------------------------------------------------------------------
    def __init__(self, parent, device_list, settings):


        self._device_list = device_list

        widget_rows = int(settings.option("beamline_ui", "widget_rows"))
        scene_height = int(settings.option("beamline_ui", "section_height"))

        width = len(self._device_list) // widget_rows
        width += 1 if len(self._device_list) % widget_rows else 0
        width *= scene_height

        QtWidgets.QGraphicsScene.__init__(self, QtCore.QRectF(0, 0, width, scene_height), parent)
        Logit.__init__(self)

        self._selected_devices = []
        self.device_items = {}

        horizontal_step = int(settings.option("beamline_ui", "horizontal_step"))
        vertical_step = int(settings.option("beamline_ui", "vertical_step"))
        device_width = int(settings.option("beamline_ui", "device_width"))
        device_height = int(settings.option("beamline_ui", "device_height"))

        shift_x = (horizontal_step - device_width) // 2
        shift_y = (vertical_step - device_height) // 2

        row_count = 0
        column_count = 0
        for device in device_list:
            geometry = [shift_x + column_count*horizontal_step,
                        shift_y + row_count*vertical_step, device_width, device_height]
            self.device_items[device] = DeviceGraphicsItem(self, device, geometry)
            row_count += 1
            if row_count == widget_rows:
                row_count = 0
                column_count += 1
   
    # ----------------------------------------------------------------------
    def mouseMoveEvent(self, event):
        """
        """
        super().mouseMoveEvent(event)
        
        #pos = event.scenePos()

    # ----------------------------------------------------------------------
    def mousePressEvent(self, event):
        """
        """
        super().mousePressEvent(event)

        pos = event.scenePos()

        if QtCore.Qt.ControlModifier != event.modifiers():
            self._selected_devices = []
            
        device_name = self._intersect(pos)
        if device_name:
            if device_name not in self._selected_devices:
                self._selected_devices.append(device_name)
            else:
                self._selected_devices.remove(device_name)

        self.device_selection_changed.emit(self._selected_devices)

    # ----------------------------------------------------------------------
    def _intersect(self, pos):
        """
        """
        for name, graphics_item in list(self.device_items.items()):
            if graphics_item.intersect(pos):
                return name

        return None
