# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getSiteLogo
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from design.plone.theme.controlpanel.interfaces import IDesignPloneThemeSettings
from design.plone.theme.vocabularies import SHARES
from plone import api
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.layout.viewlets import common as base
from plone.app.layout.viewlets.common import SearchBoxViewlet
from plone.app.layout.viewlets.content import ContentRelatedItems as BaseContentRelatedItems
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.app.multilingual.browser.selector import LanguageSelectorViewlet
from plone.memoize.view import memoize
from six.moves.urllib.parse import quote
from zope.component import getMultiAdapter
import logging


logger = logging.getLogger(__name__)

socialCSSClassDict = {
    'facebook': 'fab fa-facebook-f',
    'twitter': 'fab fa-twitter',
    'instagram': 'fab fa-instagram',
    'telegram': 'fab fa-telegram',
    'youtube': 'fab fa-youtube',
    'linkedin': 'fab fa-linkedin-in',
    'medium': 'fab fa-medium-m',
    'newsletter': 'far fa-newspaper',
    'rss': 'fas fa-rss',
    'google': 'fab fa-google-plus-g',
    'pinterest': 'fab fa-pinterest',
    'flickr': 'fab fa-flickr',
    'pocket': 'fab fa-get-pocket',
    'spotify': 'fab fa-spotify',
}


class CustomDocumentBylineViewlet(DocumentBylineViewlet):

    index = ViewPageTemplateFile('templates/document_by_line.pt')

    def show(self):
        # always show: anonymous need to see some infos
        return True

    def creator(self):
        """ show creator infos only for authenticated users """
        return not self.anonymous and self.context.Creator() or ''


class SocialViewlet(base.ViewletBase):
    def __init__(self, context, request, view, manager):
        super(SocialViewlet, self).__init__(context, request, view, manager)

    def render(self):
        """
        """
        allowed_types = api.portal.get_registry_record(
            'available_types', interface=IDesignPloneThemeSettings
        )
        if self.context.portal_type in allowed_types:
            return self.index()
        return ''

    def get_socials(self):
        socials = api.portal.get_registry_record(
            'available_socials', interface=IDesignPloneThemeSettings
        )
        return socials

    def get_css_class(self, social_type):
        cssClass = SHARES[social_type]['cssClass']
        return cssClass or ''

    def get_sharer_url(self, social_type):
        share_url = SHARES[social_type]['share_url']
        title = quote(self.context.title.encode('utf-8'))
        item_url = self.context.absolute_url()
        if social_type == 'linkedin':
            return share_url.format(item_url, title)
        if social_type == 'twitter':
            return share_url.format(item_url, title)
        if social_type == 'pinterest':
            return share_url.format('', item_url, 'false', title)
        if social_type == 'pocket':
            return share_url.format(item_url, title)
        return share_url.format(item_url)

    def get_target(self, social_type):
        return SHARES.get(social_type, {}).get('target', '_blank')


class LogoViewlet(base.ViewletBase):
    index = ViewPageTemplateFile('templates/logo.pt')

    @memoize
    def getZonaImage(self,):
        nav_root = api.portal.get_navigation_root(self.context)
        portal = api.portal.get()
        if portal == nav_root:
            return

        if nav_root.portal_type != 'Zona':
            return

        src = nav_root.absolute_url()+'/@@images/logo'
        return src

    def update(self):

        self.portal_state = getMultiAdapter(
            (self.context, self.request), name=u"plone_portal_state"
        )
        self.site_url = self.portal_state.portal_url()
        self.navigation_root_url = self.portal_state.navigation_root_url()
        self.site_title = api.portal.get_registry_record('plone.site_title')

        zona_src = self.getZonaImage()
        self.logo_title = self.site_title
        site_logo = getSiteLogo()
        site_logo = site_logo if not site_logo.endswith('logo.png') else ''
        self.img_src = zona_src or site_logo
        self.navigation_root_title = self.portal_state.navigation_root().title


class HeaderSocialViewlet(base.ViewletBase):
    '"Follow us" viewlet'
    index = ViewPageTemplateFile('templates/header_social_viewlet.pt')

    def get_links_list(self):
        try:
            return api.portal.get_registry_record(
                'follow_us_links', interface=IDesignPloneThemeSettings
            )
        except InvalidParameterError:
            return []

    def get_social_links(self):
        links = self.get_links_list()
        res = []
        for link in links:
            try:
                social, url = link.split('|')
                cssClass = socialCSSClassDict.get(social.strip(), '')
                res.append({'id': social, 'url': url, 'cssClass': cssClass})
            except ValueError:
                logger.warning(
                    '[HeaderSocialViewlet] - skipped entry "{0}"'
                    ' because is malformed. Check it in control panel.'
                )
                continue
        return res


class SkipLinksViewlet(base.ViewletBase):
    'Skiplinks viewlet'
    index = ViewPageTemplateFile('templates/skip_links_viewlet.pt')


class AgidSearchBoxViewlet(SearchBoxViewlet):
    """ Search viewlet """

    index = ViewPageTemplateFile('templates/searchbox.pt')


class HeaderBannerViewlet(LanguageSelectorViewlet):
    """ Header banner viewlet """

    def get_value_from_registry(self, record):
        try:
            value = api.portal.get_registry_record(
                record, interface=IDesignPloneThemeSettings
            )
        except KeyError:
            value = u''

        return value

    def get_bool_value_from_registry(self, record):
        try:
            value = api.portal.get_registry_record(
                record, interface=IDesignPloneThemeSettings
            )
        except KeyError:
            value = False

        return value

    def update(self):
        self.tool = api.portal.getToolByName(self.context, 'portal_languages', None)


        self.header_link_label = self.get_value_from_registry(
            'header_link_label'
        )
        self.header_link_url = self.get_value_from_registry('header_link_url')
        self.header_second_link_label = self.get_value_from_registry(
            'header_second_link_label'
        )
        self.header_second_link_url = self.get_value_from_registry(
            'header_second_link_url'
        )
        self.login_button_visible = self.get_bool_value_from_registry(
            'login_button_visible'
        )

    def showLanguageSelector(self):
        return (
            (self.header_link_label and self.header_link_url)
            or (self.header_second_link_url and self.header_second_link_url)
            or self.login_button_visible
            or self.available()
        )

    def getUserInfos(self):
        if api.user.is_anonymous():
            return {}
        user = api.user.get_current()
        return {
            'id': user.getProperty('id'),
            'fullname': user.getProperty('fullname') or user.getProperty('id'),
        }


class ContentRelatedItems(BaseContentRelatedItems):
    def related2brains(self, related):
        """Return a list of brains based on a list of relations. Will filter
        relations if the user has no permission to access the content.

        :param related: related items
        :type related: list of relations
        :return: list of catalog brains
        """
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = []
        for r in related:
            path = getattr(r, 'to_path', None)
            if path is None:
                # Item was deleted.  The related item should have been cleaned
                # up, but apparently this does not happen.
                continue
            # the query will return an empty list if the user
            # has no permission to see the target object
            brains.extend(catalog(path=dict(query=path, depth=0)))
        return brains
