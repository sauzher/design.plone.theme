# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from design.plone.theme import _ # noqa
from design.plone.theme.controlpanel.interfaces import IDesignPloneThemeSettings  # noqa
from design.plone.theme.controlpanel.interfaces import IUnibaPloneThemeSettings  # noqa
from design.plone.theme.controlpanel.interfaces import IUnibaReindexUid  # noqa
from z3c.form import form
from z3c.form import field
from z3c.form import button
from plone import api



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


class UnibaUIDReindexForm(form.Form):
    """settings form."""
    schema = IUnibaReindexUid
    fields = field.Fields(IUnibaReindexUid)
    ignoreContext=True
    
    id = 'UnibaUIDReindexForm'
    label = u'Reindicizzazione UID specifici'
    description = u'In caso di compromissione degli indici di Solr o per reindicizzare in genere '
    'una lista di specifici oggetti'

    @button.buttonAndHandler(_('Reindicizza'), name='reindicizza')
    def reindicizza(self, action):
        data, errors = self.extractData()
        if errors:
            self.status="error"
            return
        indici = data.get('indici')
        
        for i, uid in enumerate(data.get('uids')):
            uid = uid.strip()
            uid = uid.replace('"','')
            uid = uid.replace("'",'')
            uid = uid.replace(',','')
            if not uid:
                continue
            obj = api.content.get(UID=uid)
            if obj is not None:
                obj.reindexObject(idxs=indici)
                
        self.status="Reindicizzazi {} oggetti".format(i)
        
        
        
        


class UnibaUIDReindexControlPanel(controlpanel.ControlPanelFormWrapper):  # noqa
    """ uniba settings control panel.
    """
    form = UnibaUIDReindexForm
