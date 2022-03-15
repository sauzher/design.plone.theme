# -*- coding: utf-8 -*-
# Browser view utilities

from Acquisition import aq_base
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from design.plone.theme import logger
from json import dump
from logging import getLogger
from os import environ
from plone import api
from plone.memoize import ram
from plone.memoize.view import memoize
from plone.protect.interfaces import IDisableCSRFProtection
from six.moves import StringIO
from time import time
from transaction import commit
import requests
from Products.CMFPlone import utils
from zope.interface import alsoProvides
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IFolderish
try:
    from Products.ATContentTypes.interfaces.topic import IATTopic as ITopic
except ImportError:
    from plone.app.contenttypes.interfaces import ICollection as ITopic


try:
    from plone.app.multilingual.interfaces import ITranslationManager
    NO_MULTILINGUA = False
except:
    NO_MULTILINGUA = True


logger = getLogger('uniba.utils')

class UnibaUtils(BrowserView):
    
    
    def inZona(self, context=None, request={}):
        """Vedi interfaces"""
        context = aq_inner(self.context)
        portal = api.portal.get()
        root = api.portal.get_navigation_root(context)
        obj = context
        

        while obj is not root and aq_base(obj) is not aq_base(
            portal
            ):
            obj = utils.parent(obj)
            
        if obj is root and aq_base(obj) is not aq_base(portal):
            return obj.getId()
        else:
            return 0

    def cssZona(self, context=None, request={}):
        context = aq_inner(self.context)
        request = self.request
        root = api.portal.get()

        obj = self.inZona()
        css = "%s.css" % obj
        if obj:
            if not hasattr(root, css):
                logger("uniba.skin", 'info', "Nessun CSS associato alla zona '%s'" % obj)
                return ""

            return context.unrestrictedTraverse(css)(context, request)
        else:
            return ""

    def localReindex(self, idxs=[], recursive=True, context=None, force=False):
        """
        reindicizza tutti gli oggetti del sottoalbero
        si possono specificare indici specifici
        """

        if context is None:
            context = aq_inner(self.context)

        request = self.request
        alsoProvides(request, IDisableCSRFProtection)

        idxs = idxs or self.request.get("idxs", [])
        if type(idxs) == str:
            idxs = [idxs]

        # eliminiamo eventuali stringhe vuote
        idxs = [x for x in idxs if x]

        force = force or self.request.get("force", False)
        path = "/".join(context.getPhysicalPath())

        portal = api.portal.get()
        catalog = portal.portal_catalog

        totals = catalog(path=path)

        if len(totals) > 1000 and not force:
            # qs = self.request.QUERY_STRING+'&force:int=1'

            return ViewPageTemplateFile("templates/localReindex.pt")(self)
            # return msg%(self.request.URL0+"?"+qs)

        if ITopic.providedBy(context):
            context=context.aq_parent

        if IContentish.providedBy(context):
            logger.info(
            u"Reindicizzo gli indici {} del contenuto di {}".format(
                idxs,
                context.absolute_url())
        )
            context.reindexObject(idxs=idxs)

        if IFolderish.providedBy(context):
            logger.info(
            u"Reindicizzo gli indici {} dei contenuti di {}".format(
                idxs, context.absolute_url())
        )
            i=0
            for obj in context.objectValues():
                if i and not i%100:
                    logger.info('commit intermedio {}'.format(i))
                    commit()
                i+=1
                if ITopic.providedBy(obj):
                    continue

                if IContentish.providedBy(obj):
                    self.localReindex(idxs=idxs,
                                  recursive=True,
                                  context=obj)
            logger.info('commit finale {}'.format(context.absolute_url()))
            commit()

        return "+1"

    def whichInstance(
    self,
    ):
        stream = environ.get("INSTANCE_HOME", "nessuna instance_home")
        stream += "\n\n"

        for k, v in environ.items():
            if "proxy" not in k.lower() + str(v).lower():
                continue
            stream += "%s: %s\n" % (k, v)
        return stream    