# -*- coding: utf-8 -*-
from design.plone.theme import logger
from logging import getLogger
from lxml import etree
from lxml import objectify
from plone import api


try:
    from plone.app.multilingual.interfaces import ITranslationManager
    NO_MULTILINGUA=False
except:
    NO_MULTILINGUA=True
    
from plone.memoize import ram
from plone.memoize.view import memoize
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from six.moves import StringIO
from six.moves import urllib
from time import time
from zope.component import getMultiAdapter
from zope.interface import implementer


ProxyHandler = urllib.request.ProxyHandler
URLError = urllib.error.URLError
build_opener =  urllib.request.build_opener
install_opener = urllib.request.install_opener
urlopen = urllib.request.urlopen


def safe_transalte(obj):
    if NO_MULTILINGUA:
        return obj
    obj_translations = ITranslationManager(obj)
    current_language = api.portal.get_current_language()
    if current_language in obj_translations.get_translations():
        return obj_translations.get_translation(current_language)

    # fallback sull'unica traduzione disponibile    
    return obj
        


class ServiziOnline(BrowserView):

    def __call__(self, **kwargs):
        return self.getContents()

    @memoize
    def getContents(self):
        context = self.context
        servizi_online_uniba = api.portal.get_registry_record(
            name='design.plone.theme.controlpanel.interfaces.IUnibaPloneThemeSettings.servizi_online_uniba')
        
        if servizi_online_uniba:
            # recuperiamo i servizi online dal portale uniba
           return self.getUniBaITAccessoRapido()
        else:
            # usiamo la definizione locale
            content_uid = api.portal.get_registry_record(
                name="design.plone.theme.controlpanel.interfaces.IUnibaPloneThemeSettings.servizi_online_content")
            obj = api.content.get(UID=content_uid)

            obj = safe_transalte(obj)
            return obj.text.output

    @ram.cache(lambda *args: time() // (60 * 60))
    def getUniBaITAccessoRapido(
        self,
    ):
        """
        tenta la connessione a uniba.it per il recupero delle informazioni
        """
        info = """<a href="http://www.uniba.it/servizionline"
        >al momento l'informazione non pu&ograve; essere recuperata</a>"""
        URL = "https://www.uniba.it"
        url = servizi_online_uniba = api.portal.get_registry_record(
            name='design.plone.theme.controlpanel.interfaces.IUnibaPloneThemeSettings.servizi_online_uniba_url')
        
        # debug
        #URL = api.portal.get().absolute_url()
        #URL = URL.replace('8080', '8081').replace('https','http')
      
        response = self.safeRetrive(url)
        try:
            obj = objectify.parse(response)
            root = obj.getroot()
            result = etree.tostring(root.body.div)
            return result
        except Exception as e:
            return info

        return info

    def safeRetrive(self, url):
        result = None
        try:
            logger.info('apro url {}'.format(url))
            response = urlopen(url, timeout=5)
            logger.info(response)
            assert response.code == 200
            stream = response.read()
            del response
            return StringIO(stream.decode())
        except Exception as e:
            logger.debug(e)
            result = None

        try:
            proxy = ProxyHandler(
                {
                    "http": "proxy.ict.uniba.it:8080",
                    "https": "proxy.ict.uniba.it:8080",
                }
            )
            opener = build_opener(proxy)
            install_opener(opener)
            response = urlopen(url, timeout=5)
            assert response.code == 200
            stream = response.read()
            del response
            return StringIO(stream.decode())
        except Exception as e:
            logger.debug(e)
            result = None

        return result
