"""
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: '天空影视',
  lang: 'hipy'
})
"""

from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES, PKCS1_v1_5
import sys,time,json,base64,urllib3,hashlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')
try:
    # from base.spider import Spider as BaseSpider
    from base.spider import BaseSpider
except ImportError:
    from t4.base.spider import BaseSpider

class Spider(BaseSpider):
    host, android_id, init_sign_salt, app_cert_sha1, private_key, token, timeout, headers = ('','','','','','','',
    {
        'User-Agent': "okhttp-okgo/jeasonlzy",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Accept-Language': "zh-CN,zh;q=0.8",
        'sign': "",
        'devicename': "Xiaomi 15",
        'deviceos': "15",
        'bundleid': "",
        'versionname': "2.1.0",
        'versioncode': "2001000",
        'vendor': "Xiaomi",
        'chid': "26002",
        'subchid': "26002",
        'os': "1",
        'screenpx': "2670*1200",
        'nettype': "wifi",
        'audit': "1",
        'force': "1"
    })

    def init(self, extend=''):
        try:
            config = json.loads(extend)
        except (json.JSONDecodeError, TypeError):
            config = {}
        self.timeout = config.get('timeout', 15)
        self.host = config.get('host', 'http://api-live.vfilm.life')
        self.android_id = config.get('android_id', '6617a62678360a86')
        self.init_sign_salt = config.get('init_sign_salt', 'lsdfnrtpmslscndy')
        self.app_cert_sha1 = config.get('app_cert_sha1', '70:27:C9:DC:98:96:75:CD:35:DB:0C:CE:AC:CA:84:0A:B7:1E:B5:7F')
        self.private_key = config.get('private_key', 'MIICWwIBAAKBgQDYJzTUOgYdR/eIhsjpNMYWQGYl3pBycwKDoL6KThpPwrZQ9+xv\nLSaPj92HQknVaWR/RD6tHVRysChoeqAFyyQUe4UXAYnJDNlurpELb5HUIBFgmO97\niIOJCK6zbmnHT6WOHYaODTqrmX6NBgLjoFiDYBPYxG1T/K1uZ47xQDHFQQIDAQAB\nAoGAEpT8Q6phUC8ZppD/wJya0tribSr++/fLJYmyF62zMVwp1DgcCUq2X+0cPD6E\nnmYbD53MTZGR6vId5y1ziEv4Y+nu5EUyDk1xeGIxojpLhxuRoCbBt+LMJ1YUxv6p\n6F4SNwQ10U78m829Ud50mJBvkt2Vg8607SUrWheydvWHyAECQQDvayhgX5XEFaha\nUtPp5pPIkKBqHnLGm4et8be/jIIFhY9CIJbKLsqc0OFwNvz46GtRQwrtHP7LxTEF\nYT0C6CahAkEA5x+OqN/iykZIHc6Z2qZfAiLjPnQJu9DTXC/kt3TlsCc3XPNkXlAu\nq786LluH6dzQfDbLpmODtzNWavfgCtE6oQJAdTsJKDdlg//+0UthTFSE5F48zfle\nxfT9+KQ1Duvj9oQxY3XFn/ZNa3+0A1hJgi977Oxg+z2JXYmOuU2lrDi0QQJAMWwA\nF4B4gIRy21zYbXbyDgTjzvEFO9I1wBrFr60hiH96STgKmFhRAozLpioQcCO1uToG\nZjgVbFFgA1Op5uZCwQJAL1ziHIphaoCpHnnESidt3Nlrzqj/5uEpdHu7ZvPuZYya\nU8e1AhjeP+zKvfJUiXwDGuDZLx5Xe0BK8Bu72sdKcQ==')
        self.headers['bundleid'] = config.get('bundleid', 'com.ytwl.fhtq')
        self.token = config.get('token', '')
        imsi_id = config.get('imsi_id', '1')
        self.headers['sign'] = self.sign_encrypt(f'jing##&&&wei##&&&fuwu##{imsi_id}&&&idian##&&&she##{self.android_id}&&&mdian##{self.android_id}&&&olian##&&&an##{self.android_id}')

    def homeContent(self, filter):
        if not self.host: return None
        timestamp = self.timestamp()
        payload = {
            'applock': "0",
            'ncode': self.init_sign(timestamp),
            'force': "1",
            'retime': timestamp
        }
        response = self.post(f'{self.host}/news/tv/columns', data=payload, headers=self.headers, timeout=self.timeout, verify=False).json()
        classes = []
        for i in response['data']['list']:
            if i['is_show_recommend'] == 1:
                home_class_id = i.get('column_id')
                continue
            classes.append({'type_id': i['column_id'], 'type_name': i['name']})
        timestamp = self.timestamp()
        payload = {
            'column_id': home_class_id or '164',
            'ncode': self.init_sign(timestamp),
            'page': "1",
            'retime': timestamp
        }
        response = self.post(f'{self.host}/news/tv/sectionsPageByColumn', data=payload, headers=self.headers, timeout=self.timeout, verify=False).json()
        section_list = response['data']['section_list']
        videos = []
        for i in section_list:
            for j in i.get('tv_list', []):
                videos.append({
                    'vod_id': j.get('news_id'),
                    'vod_name': j.get('title', j.get('sub_title')),
                    'vod_pic': j.get('ver_pic')
                })
        return {'class': classes, 'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        timestamp = self.timestamp()
        payload = {
            'column_id': tid,
            'ncode': self.init_sign(timestamp),
            'page': pg,
            'retime': timestamp
        }
        response = self.post(f'{self.host}/news/tv/tvListByColumn', data=payload, headers=self.headers, timeout=self.timeout, verify=False).json()
        videos = []
        for i in response['data']['list']:
            up_count = i.get('up_count', '')
            if up_count:
                up_count = f'{up_count}集'
            videos.append({
                'vod_id': i.get('news_id'),
                'vod_name': i.get('title'),
                'vod_pic': i.get('ver_pic'),
                'vod_remarks': up_count,
                'vod_area': i.get('area'),
                'vod_class': i.get('cat'),
                'vod_score': i.get('score'),
                'vod_year': i.get('pubdate')
            })
        return {'list': videos, 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        timestamp = self.timestamp()
        payload = {
            'ncode': self.init_sign(timestamp),
            'signKey': self.signKey(timestamp),
            'page': pg,
            'is_check': "0",
            'keyword': key,
            'retime': timestamp
        }
        response = self.post(f'{self.host}/search/wordinfo', data=payload, headers=self.headers, timeout=self.timeout, verify=False).json()
        videos = []
        for i in response['data']['search_list']:
            for j in i.get('list',[]):
                vod_remarks = j.get('up_count')
                if vod_remarks:
                    vod_remarks = f'{vod_remarks}集'
                else:
                    vod_remarks = j.get('news_type_name')
                videos.append({
                    'vod_id': j.get('news_id'),
                    'vod_name': j.get('origin_title',j.get('title')),
                    'vod_pic': j.get('ver_pic'),
                    'vod_content': j.get('desc'),
                    'vod_remarks': vod_remarks,
                    'vod_area': j.get('area'),
                })
        return {'list': videos, 'page': pg}

    def detailContent(self, ids):
        timestamp = self.timestamp()
        payload = {
            'ncode': self.init_sign(timestamp),
            'signKey': self.signKey(timestamp),
            'news_id': ids[0],
            'retime': timestamp
        }
        response = self.post(f'{self.host}/news/tv/detail', data=payload, headers=self.headers, timeout=self.timeout, verify=False).json()
        data = response['data']
        timestamp2 = self.timestamp()
        payload = {
            'next': "0",
            'pl_id': "",
            'playlink_num': "1",
            'ncode': self.init_sign(timestamp2),
            'format': "high",
            'mobile': "",
            'check': "0",
            'mpl_id': "",
            'news_id': ids[0],
            'retime': timestamp2,
            'resite': "",
            'signKey': self.signKey(timestamp2),
            'bid': "300",
            'retry': "0"
        }
        response = self.post(f'{self.host}/news/tv/multiDetail', data=payload, headers=self.headers, timeout=self.timeout, verify=False).json()
        data_ = response['data']['data']
        data2_ = self.decrypt(data_)
        data2 = json.loads(data2_)
        max_up_count = data2.get('max_up_count',data2.get('up_count'))
        news_id = data2['news_id']
        site_list_test = data2.get('test')
        if site_list_test:
            site_list = site_list_test.get('site_list',[])
        vod_play_froms = []
        vod_play_froms.extend(site_list)
        vod_play_froms = [str(item) for item in vod_play_froms]
        vod_play_urls = []
        for i in vod_play_froms:
            urls = []
            for j in range(1,int(max_up_count) + 1):
                urls.append(f"第{j}集${j}@{news_id}@{i}")
            vod_play_urls.append('#'.join(urls))
        videos = []
        up_count = data.get('up_count',data.get('max_up_count'))
        if up_count:
            up_count = f'{up_count}集'
        videos.append({
            'vod_id': data.get('news_id'),
            'vod_name': data.get('title'),
            'vod_content': data.get('desc'),
            'vod_director': data.get('dir'),
            'vod_actor': data.get('act'),
            'vod_class': data.get('cat'),
            'vod_remarks': up_count,
            'vod_area': data.get('area'),
            'vod_play_from': '$$$'.join(vod_play_froms),
            'vod_play_url': '$$$'.join(vod_play_urls)
        })
        return {'list': videos}

    def playerContent(self, flag, id, vipflags):
        jx, url, play_header = 0, '', {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 15; 24129PN74C Build/AP3A.240617.008)'}
        episodes, news_id, resite = id.split('@', 2)
        timestamp = self.timestamp()
        payload = {
            'next': "0",
            'pl_id': "",
            'playlink_num': episodes,
            'ncode': self.init_sign(timestamp),
            'format': 'high',
            'mobile': "",
            'check': "0",
            'mpl_id': "",
            'news_id': news_id,
            'retime': timestamp,
            'resite': resite,
            'signKey': self.signKey(timestamp),
            'bid': '300',
            'retry': "0"
        }
        response = self.post(f'{self.host}/news/tv/multiDetail', data=payload, headers=self.headers,timeout=self.timeout, verify=False).json()
