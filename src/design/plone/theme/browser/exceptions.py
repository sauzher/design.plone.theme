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
         
    def get_path_info(self, portalid):
        if 'VIRTUAL_URL_PARTS' in self.request:
            path_info = '/'+'/'.join(self.request.VIRTUAL_URL_PARTS[1:])
            
        else:
            path_info = self.request.PATH_INFO
            if path_info.startswith('/{}'.format(portalid)):
                path_info = path_info.replace('/{}'.format(portalid),'')
        
        return path_info
    
    def immediate_redirect(self,):
        portal = api.portal.get()
        
        path_info = self.get_path_info(portalid = portal.getId())
        if path_info.startswith('/it/') or \
           path_info.startswith('/en/'):
            return
        
        #if path_info.split('/')[0]==portal.getId()
        
        languages = ['it', 'en']
        for lang in languages:
            try:
                newpath = '{}{}'.format(lang, path_info)
                obj = portal.restrictedTraverse(newpath)
                return '{}/{}'.format(portal.absolute_url(), newpath)
            except:
                pass