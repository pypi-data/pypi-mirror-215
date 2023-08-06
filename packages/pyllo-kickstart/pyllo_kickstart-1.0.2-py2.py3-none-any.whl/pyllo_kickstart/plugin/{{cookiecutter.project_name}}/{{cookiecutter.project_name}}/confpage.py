# -*- coding: utf-8 -*-
#
# Copyright © {{cookiecutter.company}}
# Author: {{cookiecutter.author}}

# Python imports

# Qt imports
from qtpy.QtWidgets import (QButtonGroup, QGroupBox, QHBoxLayout, QLabel,
                            QVBoxLayout)

# Local imports
from pyllo.core.runtime.environ import getCwdOrHome
from pyllo.ui.preferences import PluginConfigPage


class {{cookiecutter.plugin_class_name}}ConfigPage(PluginConfigPage):
    """
    {{cookiecutter.plugin_class_name|lower}} configuration page.
    """
    def setupPage(self):
        aboutLabel = QLabel("This <b>{{cookiecutter.plugin_class_name|lower}} plugin</b> is "
                            "auto-generated. You should customize it to fit your needs.")
                
        aboutLabel.setWordWrap(True)
        

        testGroup = QGroupBox("First Group")
        testBg = QButtonGroup(testGroup)
        testLabel = QLabel("Test label:")
        testLabel.setWordWrap(True)

        firstRadio = self.createRadiobutton(
            "The first radio button",
            option="test/first",
            default=True,
            tip="First selection",
            buttonGroup=testBg
        )

        secondRadio = self.createRadiobutton(
            "The second radio button",
            option="test/second",
            default=False,
            tip="Second selection",
            buttonGroup=testBg
        )

        dirBd = self.createBrowseDir("",
                                    'test/test_directory',
                                    getCwdOrHome())

        vbox1 = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(secondRadio)
        hbox1.addWidget(dirBd)
        
        vbox1.addWidget(testLabel)
        vbox1.addWidget(firstRadio)
        vbox1.addLayout(hbox1)
        testGroup.setLayout(vbox1)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(aboutLabel)
        vbox2.addSpacing(10)
        vbox2.addWidget(testGroup)
        vbox2.addStretch(1)
        self.setLayout(vbox2)

