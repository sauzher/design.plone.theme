# -*- coding: utf-8 -*-
from collective.tiles.collection.interfaces import ICollectionTileRenderer
from collective.tiles.collection.interfaces import ICollectionTileData
from datetime import datetime
from DateTime import DateTime
from design.plone.theme import _
from collective.tiles.collection import _ as _c
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.discussion.interfaces import IConversation
from Products.Five.browser import BrowserView
from ZODB.POSException import POSKeyError
from zope.interface import implementer
from zope import schema

import logging


logger = logging.getLogger(__name__)


class HelpersView(BrowserView):
    """
    A set of helper functions for tile collection views.
    """

    def get_image_tag(self, item, scale='large', direction='keep', loading='lazy'):
        try:
            scale_view = api.content.get_view(
                name='images',
                context=item,
                request=self.request,
            )
            return scale_view.tag('image', scale=scale, direction=direction, loading=loading)
        except (InvalidParameterError, POSKeyError, AttributeError):
            # The object doesn't have an image field
            return ''

    def get_bg_url(self, item, scale='thumb'):
        try:
            scale_view = api.content.get_view(
                name='images',
                context=item,
                request=self.request,
            )
            return 'background-image: url("' +\
                   str(scale_view.scale('image', scale=scale).url) + '");'
        except (InvalidParameterError, POSKeyError, AttributeError):
            # The object doesn't have an image field
            return ''

    def get_formatted_date(self, item, date_field='effective'):
        """
        return a formatted date
        """
        # effective = item.effective
        if hasattr(item, date_field):
            effective = getattr(item, date_field)
            if isinstance(effective, datetime):
                effective = DateTime(effective)
            else:
                effective = item.effective

        if effective.year() == 1969:
            # not yet published
            return {}
        return {
            'weekday': u'weekday_{0}'.format(effective.aDay().lower()),
            'month': u'month_{0}'.format(effective.aMonth().lower()),
            'month_abbr': u'month_{0}_abbr'.format(effective.aMonth().lower()),
            'day': effective.day(),
            'year': effective.year()
        }

    def getGalleryTypeIcon(self, portal_type):
        if portal_type in ['Image', 'Folder']:
            return 'photo'

        if portal_type == 'WildcardVideo':
            return 'video'

        return ''

    def getCommentsCount(self, item):
        try:
            conversation = IConversation(item)
        except Exception:
            return {'enabled': False}
        if getattr(item, 'allow_discussion', False) is False:
            return {'enabled': False}
        comments = conversation.total_comments()
        if not comments:
            return {'enabled': False}
        return {
            'enabled': True,
            'comments': conversation.total_comments()
        }

    def is_external_link(self, item):
        # accepts a Link object
        remoteUrl = getattr(item, 'remoteUrl', None)

        if remoteUrl:
            # so it's a Link
            return not remoteUrl.startswith(
                "${portal_url}"
            ) and not remoteUrl.startswith("${navigation_root_url}")

        return False

    def getSlidesToShow(self,):
        return self.data.slidesToShow()
    
    def getImageFormat(self,):
        return self.data.scalaImmagini()


@implementer(ICollectionTileRenderer)
class SightsView(BrowserView):
    """
    Custom view that shows sights
    """

    display_name = _('Sights layout')


@implementer(ICollectionTileRenderer)
class NewsHighlightView(BrowserView):
    """
    Custom view that shows an highlighted news
    """

    display_name = _('News highlight')


@implementer(ICollectionTileRenderer)
class NewsBigPhotoView(BrowserView):
    """
    Custom view that shows a news with a big photo on the background
    """
    display_name = _('News with big photo')


@implementer(ICollectionTileRenderer)
class NewsAreaTematicaView(BrowserView):
    """
    Custom view that shows news in area tematica
    """
    display_name = _('News in area tematica')


@implementer(ICollectionTileRenderer)
class ServiziAreaTematicaView(BrowserView):
    """
    Custom view that shows servizi in area tematica
    """
    display_name = _('Servizi in area tematica')


@implementer(ICollectionTileRenderer)
class NewsView(BrowserView):
    display_name = _('News layout with image')


@implementer(ICollectionTileRenderer)
class VideoView(BrowserView):
    display_name = _('Video layout')


@implementer(ICollectionTileRenderer)
class GalleryView(BrowserView):
    display_name = _('Gallery layout')


@implementer(ICollectionTileRenderer)
class AreeTematicheView(BrowserView):
    display_name = _('Link aree tematiche')


@implementer(ICollectionTileRenderer)
class OnlineServicesView(BrowserView):
    display_name = _('Layout servizi online')


class ICollectionTileDataSlide(ICollectionTileData):
    slidesToShow = schema.Choice(
        title=_("num_slides_to_show", u"Numero slide da mostrare (1-4)"),
        required=False,
        default=4,
        values=[1, 2, 4]
    )
    
    scalaImmagini = schema.Choice(
        title=_('portlet.rapporto_forma_label' , 'Rapporto di forma'),
        description=_('portlet.rapporto_forma_description,',
                      'Scegli il rapporto di forma che verra applicato (crop) a tutte le immagini'
                      ' dello slideshow (default: 1920*800)'),
        vocabulary='plone.app.vocabularies.ImagesScales',
        default='unibaslidehomepage',
    )

    renderer = schema.Choice(
        title=_c("collection_tile_renderer", u"Renderer"),
        description=_c(
            "collection_tile_renderer_help",
            u"Select one of the available possible layouts for this tile.",
        ),
        vocabulary="collective.tiles.collection.vocabulary.renderers",
        required=True,
        default="sights_renderer",
    )

    css_class = schema.TextLine(
        title=_c("collection_tile_css_class", u"CSS class"),
        description=_c(
            "collection_tile_css_class_help",
            u"Insert a list of additional css classes for this tile.",
        ),
        required=False,
        default=u"carousel",
    )
