# -*- coding: utf-8 -*-
#
# Copyright © {{cookiecutter.company}}
# Author: {{cookiecutter.author}}

# Qt imports
from qtpy.QtCore import QSize, Signal, Slot
from qtpy.QtWidgets import QLabel, QVBoxLayout, QGroupBox, QMessageBox


# Local imports
from pyllo.ui.plugin import PluginMainWidget
from ..api import {{cookiecutter.plugin_class_name}}Actions



class {{cookiecutter.plugin_class_name}}Widget(PluginMainWidget):
    """
    Main widget for {{cookiecutter.plugin_class_name|lower}}
    
    TODO: add description here.
    """

    # --- Signals
    # ----------------------------------------------
    sigTest = Signal()

    # --- PluginMainWidget API
    # ----------------------------------------------
    def setup(self):
        # Widgets
        self.label = QLabel("{{cookiecutter.plugin_class_name|lower}} widget label.")

        # Widgets
        self.label = QLabel("{{cookiecutter.plugin_class_name|lower}} plugin dockable window widget label.")
        self.gb = QGroupBox("{{cookiecutter.plugin_class_name|lower}} plugin")

        # Layouts
        gbLayout = QVBoxLayout()
        gbLayout.addWidget(self.label)
        self.gb.setLayout(gbLayout)

        layout = QVBoxLayout()
        layout.addWidget(self.gb)
        self.setLayout(layout)

        # TODO: setup actions here.
        self.testAction = self.createAction(
            {{cookiecutter.plugin_class_name}}Actions.Test,
            text='Test',
            tip='Test',
            icon=self.createIcon('test'),
            triggered=self.test
        )

    def getTitle(self):
        return "{{cookiecutter.plugin_class_name|lower}}"

    def updateActions(self):
        # update actions
        ...

    def test(self):
        QMessageBox.information(self,
                                self.getName(),
                                "[{{cookiecutter.plugin_class_name}}]: Test action for demo.",
                                QMessageBox.Ok)

