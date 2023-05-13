#-----------------------------------------------------------
# Copyright (C) 2023 Ben Wirf
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from qgis.PyQt.QtWidgets import QAction

from qgis.core import (Qgis, QgsProject, QgsDefaultRasterLayerLegend)

from qgis.gui import QgsRasterLayerProperties

import os


def classFactory(iface):
    return LoadLegendImagePlugin(iface)


class LoadLegendImagePlugin:
    def __init__(self, iface):
        self.iface = iface
        self.legend_image = os.path.join(os.path.dirname(__file__), "LIMITES_ADMINISTRATIVES_EXPRESS.LATEST-legend.png")

    def initGui(self):
        self.action = QAction('Load Legend Image', self.iface.mainWindow())
        
        # Change run2 to run in the line below to test both approaches
        self.action.triggered.connect(self.run2)
        
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action
    
    # Both methods below set the legend image to an active raster layer in the TOC
    def run(self):
        layer = self.iface.activeLayer()
        if not layer.type() == Qgis.LayerType.Raster:
            return
        layer.setLegendPlaceholderImage(self.legend_image)
        props = QgsRasterLayerProperties(layer, self.iface.mapCanvas())# Note use of self.iface object if this is in a plugin
        props.apply()
        
    def run2(self):
        layer = self.iface.activeLayer()
        if not layer.type() == Qgis.LayerType.Raster:
            return
        legend = QgsDefaultRasterLayerLegend(layer)
        layer.setLegendPlaceholderImage(self.legend_image)
        layer.setLegend(legend)
        legend.itemsChanged.emit()
        
        