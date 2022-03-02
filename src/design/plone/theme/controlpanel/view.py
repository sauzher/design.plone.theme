# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from design.plone.theme.controlpanel.interfaces import IDesignPloneThemeSettings  # noqa
from design.plone.theme.controlpanel.interfaces import IUnibaPloneThemeSettings  # noqa


class DesignPloneThemeEditForm(controlpanel.RegistryEditForm):
    """settings form."""
    schema = IDesignPloneThemeSettings
    id = 'DesignPloneThemeSettingsEditForm'
    label = u'Configurazione tema agid'
    description = u''


class DesignPloneThemeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):  # noqa
    """settings control panel.
    """
    form = DesignPloneThemeEditForm

class UnibaPloneThemeEditForm(controlpanel.RegistryEditForm):
    """settings form."""
    schema = IUnibaPloneThemeSettings
    id = 'UnibaPloneThemeSettingsEditForm'
    label = u'Configurazione tema agid UniBa'
    description = u''


class UnibaPloneThemeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):  # noqa
    """ uniba settings control panel.
    """
    form = UnibaPloneThemeEditForm
