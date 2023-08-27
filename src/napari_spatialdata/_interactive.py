from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import napari
import shapely
from napari.utils.events import EventedList

from napari_spatialdata._sdata_widgets import SdataWidget
from napari_spatialdata.utils._utils import NDArrayA, _get_sdata_key, get_duplicate_element_names

if TYPE_CHECKING:
    from spatialdata import SpatialData
import matplotlib.pyplot as plt

from napari_spatialdata.utils._test_utils import save_image


class Interactive:
    """
    Interactive visualization of spatial data.

    Parameters
    ----------
    sdata
        SpatialData object.
    headless
        Run napari in headless mode, default False.

    Returns
    -------
    None
    """

    def add_element(self, coordinate_system_name: str, element: str) -> None:
        elements = {}
        duplicate_element_names, _ = get_duplicate_element_names(self._sdata)

        for index, sdata in enumerate(self._sdata):
            for element_type, element_name, _ in sdata.filter_by_coordinate_system(
                coordinate_system_name
            )._gen_elements():
                elements_metadata = {
                    "element_type": element_type,
                    "sdata_index": index,
                    "original_name": element_name,
                }
                name = element_name if element_name not in duplicate_element_names else element_name + f"_{index}"
                if element_name == element:
                    name_to_add = name
                elements[name] = elements_metadata

        sdata, multi = _get_sdata_key(self._sdata, elements, element_name)
        metadata = elements.get(name_to_add)
        if metadata:
            element_type = metadata["element_type"]
            if element_type == "images":
                self._sdata_widget.viewer_model.add_sdata_image(sdata, coordinate_system_name, name_to_add, multi)
            elif element_type == "labels":
                self._sdata_widget.viewer_model.add_sdata_labels(sdata, coordinate_system_name, name_to_add, multi)
            elif element_type == "points":
                self._sdata_widget.viewer_model.add_sdata_points(sdata, coordinate_system_name, name_to_add, multi)
            elif element_type == "shapes":
                if type(sdata.shapes[element].iloc[0][0]) == shapely.geometry.point.Point:
                    self._sdata_widget.viewer_model.add_sdata_circles(sdata, coordinate_system_name, name_to_add, multi)
                elif (type(sdata.shapes[element].iloc[0][0]) == shapely.geometry.polygon.Polygon) or (
                    type(sdata.shapes[element].iloc[0][0]) == shapely.geometry.multipolygon.MultiPolygon
                ):
                    self._sdata_widget.viewer_model.add_sdata_shapes(sdata, coordinate_system_name, name_to_add, multi)
        else:
            raise ValueError("Element {element_name} not found in coordinate system {coordinate_system_name}.")

    def create_folders(self, tested_notebook: str, test_target: str) -> str:
        main_folder = os.getcwd()  # Get the current working directory
        tests_folder = os.path.join(main_folder, "tests")
        screenshots_folder = os.path.join(tests_folder, "screenshots")
        notebook_folder = os.path.join(screenshots_folder, tested_notebook)
        cell_folder = os.path.join(notebook_folder, test_target)

        os.makedirs(screenshots_folder, exist_ok=True)
        os.makedirs(tests_folder, exist_ok=True)
        os.makedirs(notebook_folder, exist_ok=True)
        os.makedirs(cell_folder, exist_ok=True)

        return cell_folder

    def __init__(
        self,
        sdata: SpatialData,
        coordinate_system_name: str | None = None,
        headless: bool = False,
        _tested_notebook: str | None = None,
        _test_target: str | None = None,
        _take_screenshot: str | None = None,
    ) -> None:
        viewer = napari.current_viewer()
        self._viewer = viewer if viewer else napari.Viewer()
        if isinstance(sdata, list):
            self._sdata = EventedList(data=sdata)
        else:
            self._sdata = EventedList(data=[sdata])
        self._sdata_widget = SdataWidget(self._viewer, self._sdata)
        self._list_widget = self._viewer.window.add_dock_widget(
            self._sdata_widget, name="SpatialData", area="left", menu=self._viewer.window.window_menu
        )
        self._viewer.window.add_plugin_dock_widget("napari-spatialdata", "View")

        if _tested_notebook is not None:
            assert _test_target is not None
            assert coordinate_system_name is not None

            filepath = self.create_folders(_tested_notebook, _test_target)

            for _, element_name, _ in self._sdata.filter_by_coordinate_system(coordinate_system_name)._gen_elements():
                self.add_element(coordinate_system_name=coordinate_system_name, element=element_name)

                if _take_screenshot:
                    save_image(self.screenshot(canvas_only=True), os.path.join(filepath, element_name + ".png"))
                else:
                    plt.imshow(self.screenshot(canvas_only=True))

        if not headless:
            self.run()

    def run(self) -> None:
        napari.run()

    def screenshot(self, canvas_only: bool) -> NDArrayA | Any:
        return self._viewer.screenshot(canvas_only=canvas_only)
