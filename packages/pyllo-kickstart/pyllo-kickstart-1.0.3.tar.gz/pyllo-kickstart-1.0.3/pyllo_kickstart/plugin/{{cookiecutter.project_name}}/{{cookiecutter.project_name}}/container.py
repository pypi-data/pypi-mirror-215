# -*- coding: utf-8 -*-
#
# Copyright © {{cookiecutter.company}}
# Author: {{cookiecutter.author}}

"""
{{cookiecutter.plugin_class_name}} widget.
"""

# Third party imports
from qtpy.QtCore import QSize, Signal, Slot
from qtpy.QtWidgets import QMessageBox

# Local imports
from pyllo.ui.plugin import PluginMainContainer
from .api import {{cookiecutter.plugin_class_name}}Actions


class {{cookiecutter.plugin_class_name}}Container(PluginMainContainer):
    """
    Container for {{cookiecutter.plugin_class_name|lower}}.
    
    TODO: add description here.
    """

    # Declare signals here
    sigTest = Signal()

    # ---- PluginMainContainer API
    # -----------------------------------------------
    def setup(self):
        
        #TODO: setup actions here.
        self.testAction = self.createAction(
            {{cookiecutter.plugin_class_name}}Actions.Test,
            text='Test',
            tip='Test',
            icon=self.createIcon('test'),
            triggered=self.test
        )

    def updateActions(self):
        # update actions
        ...

    def test(self):
        QMessageBox.information(self,
                                self.getName(),
                                "[{{cookiecutter.plugin_class_name}}]: Test action for demo.",
                                QMessageBox.Ok)
