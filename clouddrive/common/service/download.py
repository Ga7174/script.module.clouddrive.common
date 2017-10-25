'''
    OneDrive for Kodi
    Copyright (C) 2015 - Carlos Guzman

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    Created on Mar 1, 2015
    @author: Carlos Guzman (cguZZman) carlosguzmang@hotmail.com
'''


from clouddrive.common.service.base import BaseService, BaseHandler
from clouddrive.common.service.rpc import RpcUtil
from clouddrive.common.ui.utils import KodiUtils
from urllib2 import HTTPError
from clouddrive.common.exception import ExceptionUtils
from clouddrive.common.ui.logger import Logger


class DownloadService(BaseService):
    def __init__(self):
        super(DownloadService, self).__init__()
        self._service_name = 'download'
        self._handler = Download
    
class Download(BaseHandler):
    def do_GET(self):
        data = self.path.split('/')
        code = 307
        headers = {}
        content = None
        if len(data) > 3:
            try:
                item = RpcUtil.execute_remote_method(data[1], 'get_item', kwargs = {
                    'driveid' : data[2],
                    'item_driveid' : data[3],
                    'item_id' : data[4],
                    'include_download_info' : True
                })
                headers['location'] = item['download_info']['url']
            except Exception as e:
                httpex = ExceptionUtils.extract_exception(e, HTTPError)
                if httpex:
                    code = httpex.code
                else:
                    code = 500
                content = ExceptionUtils.full_stacktrace(e)
                Logger.error('DownloadException:')
                Logger.error(content)
        else:
            code = 400
            content = 'Not enough parameters'
        self.write_response(code, content=content, headers=headers)
        

class DownloadServiceUtil(object):
    @staticmethod
    def build_download_url(addonid, driveid, item_driveid, item_id, name):
        return 'http://'+BaseService._interface+':%s/%s/%s/%s/%s/%s' % (KodiUtils.get_addon_setting('download.service.port', 'script.module.clouddrive.common'), addonid, driveid, item_driveid, item_id, name)
        
        