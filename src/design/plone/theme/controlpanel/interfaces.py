# -*- coding: utf-8 -*-
from doctest import debug_script
from design.plone.theme import _
from plone.supermodel import model
from zope import schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives as form
from plone.app.z3cform.widget import RelatedItemsWidget
from plone.app.vocabularies.catalog import CatalogSource

class IDesignPloneThemeSettings(model.Schema):

    available_types = schema.List(
        title=_(u'heading_available_portaltypes',
                default=u'Shareable content types'),
        description=_(u'description_available_portaltypes',
                      default=u'List of content-types that can be enable '
                              u'for social sharing.'),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.UserFriendlyTypes'
        )
    )

    available_socials = schema.List(
        title=_(u'heading_available_socials',
                default=u'Enabled social networks'),
        description=_(u'description_available_socials',
                      default=u'List of social networks enabled for sharing.'),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(
            vocabulary='design.plone.theme.vocabularies.SocialsVocabulary'
        )
    )

    follow_us_links = schema.List(
        title=_(u'follow_us_links_label',
                default=u'Follow us links'),
        description=_(u'follow_us_links_description',
                      default=u'List of links to external social networks.'
                              u' These links are showed in the header.\n'
                              u'If there isn\'t a related icon in the theme, '
                              u'the link will not appear properly.\n'
                              u'Available icons are: facebook, twitter, '
                              u'youtube, medium, linkedin, storify, rss, '
                              u'newsletter and instagram.\n'
                              u'Insert a list of values (one per row) in the '
                              u'following form: social_id|url where social_id'
                              u' is one of the social with available icons.'),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.TextLine()
    )

    header_link_label = schema.TextLine(
        title=_(u'header_link_label',
                default=u'Header link label'),
        description=_(u'header_link_label_desc',
                      default=u'Label for the link in the header of the site'),
        required=False,
    )

    header_link_url = schema.URI(
        title=_(u'header_link_url',
                default=u'Header link url'),
        description=_(u'header_link_url_desc',
                      default=u'URL of the link in the header'),
        required=False,
    )

    header_second_link_label = schema.TextLine(
        title=_(u'header_second_link_label',
                default=u'Header second link label'),
        description=_(u'header_second_link_label_desc',
                      default=u'Label for the link in the header of\
                              the site at right'),
        required=False
    )

    header_second_link_url = schema.URI(
        title=_(u'header_second_link_url',
                default=u'Header second link url'),
        description=_(u'header_second_link_url_desc',
                      default=u'URL of the link in the header at right'),
        required=False
    )

    login_button_visible = schema.Bool(
        title=_(u'login_button_bisible',
                default=u'Show login button'),
        default=False,
        required=False
    )






class IUnibaPloneThemeSettings(model.Schema):
    """ configurazione Tema UniBa
    """

    servizi_online_uniba = schema.Bool(
        title=_(u'servizi_online_uniba',
                default=u'Usa il menu\' definito sul portale UniBa.it'),
        default=True,
        required=False
    )

    servizi_online_uniba_url = schema.URI(
        title=_(u'servizi_online_uniba_url',
                default=u'URL da cui recuperare i servizi online'),
        description=_(u'servizi_online_uniba_url_desc',
                      default=u'Inserire l\'url completo dei servizi online con cui '
                      'popolare il menu\''),
        default="https://www.uniba.it/@@uniba.servizi_online",
        required=False
    )

    servizi_online_content = schema.ASCIILine(
        title=_(u'menu_servizi_online_topbar', default="Menu' servizi online della topbar uniba"),
        required=False,
        description=_('description_servizi_online_topbar', 'Documento da referenziare contenente il menu\''),
    )
    form.widget(
        'servizi_online_content', RelatedItemsWidget,
        pattern_options={
            "closeOnSelect": False,
            "selectableTypes":  ["Document"],
            "mode": "search",
            "rootPath": "/",
        }
    )