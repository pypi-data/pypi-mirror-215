# -*- coding: utf-8 -*-
#
# Copyright © {{cookiecutter.company}}
# Author: {{cookiecutter.author}}

# Python imports
# Qt imports
from qtpy.QtCore import Signal

# Local imports
from pyllo import Plugins
from pyllo.core.runtime.spi import PylloDockablePlugin, onPluginAvailable
from pyllo.plugins.toolbar.api import ApplicationToolbars, MainToolbarSections
from .widgets.mainwidget import {{cookiecutter.plugin_class_name}}Widget
from .confpage import {{cookiecutter.plugin_class_name}}ConfigPage


class {{cookiecutter.plugin_class_name}}(PylloDockablePlugin):
    """
    {{cookiecutter.plugin_class_name|lower}} plugin.
    {{cookiecutter.plugin_description}} 
    """

    NAME = "{{cookiecutter.plugin_class_name|lower}}"
    # You can add plugins that this plugin requires. (Pyllo assures you have these when they are defined)
    REQUIRES = [Plugins.Application, Plugins.Preferences, Plugins.Toolbar, Plugins.MainMenu]
    # You can add plugins that this plugin requires optionally.
    OPTIONAL = []

    WIDGET_CLASS = {{cookiecutter.plugin_class_name}}Widget
    CONF_SECTION = NAME
    CONF_WIDGET_CLASS = {{cookiecutter.plugin_class_name}}ConfigPage
    CONF_FILE = False

    # ---- Signals
    # -----------------------------------------------------
    sigTest = Signal()

    # ---- PylloPlugin API
    # -----------------------------------------------------
    def getName(self):
        return "{{cookiecutter.plugin_class_name|lower}}"

    @staticmethod
    def getDescription():
        return "{{cookiecutter.plugin_description}}"

    def getIcon(self):
        return self.createIcon("testPluginIcon")

    def onInitialize(self):
        # Initialize this plugin.
        # Caution:
        # Within this method you should avoid getting other plugins
        # (because they may not be ready), if certain features
        # depend on other plugins, and information of theirs can
        # not be known after their initialization. You must use
        # :meth:`onIntegrate` which called after all of plugins
        # have been self-initialized.
        widget: {{cookiecutter.plugin_class_name}}Widget
        widget = self.getWidget()
        # TODO: add initialization process here

    def onTearDown(self, cancelable=False):
        # Before plugin been teared down.
        # TODO: add teardown process here
        ...

    @onPluginAvailable(plugin=Plugins.Toolbar)
    def onToolbarAvailable(self):
        toolbar = self.getPlugin(Plugins.Toolbar)
        toolbar.addItemToApplicationToolbar(
            self.getContainer().testAction, ApplicationToolbars.Main,
            MainToolbarSections.ApplicationSection
        )
        # TODO: add plugin actions to toolbar here
        ...

    @onPluginAvailable(plugin=Plugins.MainMenu)
    def onMainMenuAvailable(self):
        mainmenu = self.getPlugin(Plugins.MainMenu)
        # TODO: add mainmenu actions or submenus here
        ...

    @onPluginAvailable(plugin=Plugins.Preferences)
    def onPreferencesAvailable(self):
        preferences = self.getPlugin(Plugins.Preferences)
        preferences.registerPluginPreferences(self)


 