# -*- coding: utf-8 -*-
from Products.CMFPlone.browser.exceptions import ExceptionView as base_ExceptionView
from plone import api


class ExceptionView(base_ExceptionView):
 
    def __call__(self,):
        response = self.request.response
        newpath = self.immediate_redirect()
        if newpath:
            self.request.physicalPathToURL(newpath)
            response.redirect(newpath, status=301, lock=1)
            return
        
        return super(ExceptionView, self).__call__()
         
    def immediate_redirect(self,):
        portal = api.portal.get()
        
        path_info = self.request.PATH_INFO
        if path_info.startswith('/it/') or \
           path_info.startswith('/en/'):
            return
        
        try:
            newpath = 'it{}'.format(path_info)
            obj = portal.restrictedTraverse(newpath)
            return obj.absolute_url()
        except:
            pass
        
        try:
            newpath = 'en{}'.format(path_info)
            obj = portal.restrictedTraverse(newpath)
            return obj.absolute_url()
        except:
            pass        
        