# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from design.plone.theme import logger
from logging import getLogger
from lxml import etree
from lxml import objectify
from plone import api
from plone.memoize import ram
from plone.memoize.view import memoize
from plone.protect.interfaces import IDisableCSRFProtection
from six.moves import StringIO
from time import time
import requests


try:
    from plone.app.multilingual.interfaces import ITranslationManager
    NO_MULTILINGUA = False
except:
    NO_MULTILINGUA = True

urlparse = requests.utils.urlparse


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

        url = servizi_online_uniba = api.portal.get_registry_record(
            name='design.plone.theme.controlpanel.interfaces.IUnibaPloneThemeSettings.servizi_online_uniba_url')

        parsed = urlparse(url)
        url = '{}://{}{}'.format(parsed.scheme, parsed.hostname, parsed.path)

        # debug
        # URL = api.portal.get().absolute_url()
        # URL = URL.replace('8080', '8081').replace('https','http')

        response = self.safeRetrive(url, parsed.username, parsed.password)
        try:
            obj = objectify.parse(response)
            root = obj.getroot()
            result = etree.tostring(root.body)
            return result
        except Exception as e:
            logger.error("impossibile parserizzare i servizi online {}".format(e))
            pass

        return info

    def safeRetrive(self, url, username=None, password=None):
        result = None
        try:
            logger.debug('apro url {}'.format(url))
            auth = None
            if username and password:
                auth = requests.auth.HTTPBasicAuth(username, password)

            response = requests.get(url,
                                    auth=auth)
            logger.debug(response)
            assert response.status_code == 200
            stream = response.text
            del response
            return StringIO(stream)
        except Exception as e:
            logger.debug(e)
            result = None

        try:
            proxy = {
                "http": "proxy.ict.uniba.it:8080",
                "https": "proxy.ict.uniba.it:8080",
            }

            response = requests.get(url,
                                    auth=auth,
                                    proxies=proxy,
                                    timeout=5)
            assert response.status_code == 200
            stream = response.text
            del response
            return StringIO(stream)
        except Exception as e:
            logger.debug(e)
            result = None

        return result


class Footer(ServiziOnline):

    def __call__(self, **kwargs):
        """prendiamo il contenuto fatto di list-item gia' impaginati
        """
        contents = self.getContents()
        return contents
        
    @memoize
    def getContents(self):
        footer_uniba = api.portal.get_registry_record(
            name='design.plone.theme.controlpanel.interfaces.IUnibaPloneThemeSettings.footer_uniba')

        if footer_uniba:
            # recuperiamo i servizi online dal portale uniba
            return self.getUniBaITFooter()
        else:
            # usiamo la definizione locale
            content_uid = api.portal.get_registry_record(
                name="design.plone.theme.controlpanel.interfaces.IUnibaPloneThemeSettings.footer_content")
            obj = api.content.get(UID=content_uid)

            obj = safe_transalte(obj)
            return obj.text.output

    @ram.cache(lambda *args: time() // (60 * 60))
    def getUniBaITFooter(self,):
        """
        tenta la connessione a uniba.it per il recupero delle informazioni
        """
        info = """<a href="http://www.uniba.it/servizionline"
        >al momento l'informazione non pu&ograve; essere recuperata</a>"""

        url = footer_uniba = api.portal.get_registry_record(
            name='design.plone.theme.controlpanel.interfaces.IUnibaPloneThemeSettings.footer_uniba_url')

        parsed = urlparse(url)
        url = '{}://{}{}'.format(parsed.scheme, parsed.hostname, parsed.path)

        # debug
        # URL = api.portal.get().absolute_url()
        # URL = URL.replace('8080', '8081').replace('https','http')

        response = self.safeRetrive(url, parsed.username, parsed.password)
        try:
            obj = objectify.parse(response)
            root = obj.getroot()
            result = etree.tostring(root.body)
            return result
        except Exception as e:
            logger.error("impossibile parserizzare il footer {}".format(e))
            pass

        return info