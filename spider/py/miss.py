# -*- coding: utf-8 -*-

import re
import socket
import sys
from urllib.parse import urlparse
from pyquery import PyQuery as pq
sys.path.append('..')
try:
    # from base.spider import Spider as BaseSpider
    from base.spider import BaseSpider
except ImportError:
    from t4.base.spider import BaseSpider


class Spider(BaseSpider):

    def init(self, extend=""):
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    host = 'https://missav.mrst.one'
    # host = 'https://missav.ai'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': f'{host}',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="130", "Google Chrome";v="130"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    Config = {
        "class": [
            {
                "type_name": "最近更新",
                "type_id": "new"
            },
            {
                "type_name": "新作上市",
                "type_id": "release"
            },
            {
                "type_name": "无码流出",
                "type_id": "uncensored-leak"
            },
            {
                "type_name": "中文字幕",
                "type_id": "chinese-subtitle"
            },
            {
                "type_name": "女优",
                "type_id": "actresses"
            },
            {
                "type_name": "类型",
                "type_id": "genres"
            },
            {
                "type_name": "发行商",
                "type_id": "makers"
            }
        ],
    }

    fts = [
        {
            'key': 'filters',
            'name': '类型',
            'value': [
                {'n': '单人作品', 'v': 'individual'},
                {'n': '多人作品', 'v': 'multiple'},
                {'n': '中文字幕', 'v': 'chinese-subtitle'}
            ]
        },
        {
            'key': 'sort',
            'name': '排序',
            'value': [
                {'n': '发行日期', 'v': 'released_at'},
                {'n': '最近更新', 'v': 'published_at'},
                {'n': '收藏数', 'v': 'saved'},
                {'n': '今日浏览数', 'v': 'today_views'},
                {'n': '本周浏览数', 'v': 'weekly_views'},
                {'n': '本月浏览数', 'v': 'monthly_views'},
                {'n': '总浏览数', 'v': 'views'}
            ]
        }
    ]

    def homeContent(self, filter):
        html = self.getpq(self.fetch(f"{self.host}/cn",headers=self.headers))
        result = {}
        filters = {}
        classes=[]
        for i in list(html('.mt-4.space-y-4').items())[:2]:
            for j in i('ul li').items():
                classes.append({
                    'type_name': j.text(),
                    'type_id': j('a').attr('href').split('/')[-1]
                })
        result['class'] = classes
        result['filters'] = filters
        result['list'] = self.getlist(html('.grid-cols-2.md\\:grid-cols-3 .thumbnail.group'))
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        params={
            'page':'' if pg=='1' else pg
        }
        params.update(extend)
        params={k: v for k, v in params.items() if v != ""}
        data=self.getpq(self.fetch(f"{self.host}/cn/{tid}",headers=self.headers,params=params))
        result = {}
        result['list'] = self.getlist(data('.grid-cols-2.md\\:grid-cols-3 .thumbnail.group'))
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        v=self.getpq(self.fetch(ids[0],headers=self.headers))
        sctx=v('body script').text()
        js_pattern = r"eval\(function\(p,a,c,k,e,d\).*?return p\}(.*?)\)\)"
        js_match = re.search(js_pattern, sctx).group(0)
        urls=self.execute_js(js_match)
        c=v('.space-y-2 .text-secondary')
        vod = {
            'type_name': c.eq(-3)('a').text(),
            'vod_year': c.eq(0)('span').text(),
            'vod_remarks': c.eq(1)('span').text(),
            'vod_actor': c.eq(3)('a').text(),
            'vod_director': c.eq(-2)('a').text(),
            'vod_content': v('.text-secondary.break-all').text(),
            'vod_play_from': 'MissAV',
            'vod_play_url': urls if urls else f"嗅探${ids[0]}",
        }
        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        data=self.getpq(self.fetch(f"{self.host}/cn/search/{key}",headers=self.headers,params={'page':pg}))
        return {'list': self.getlist(data('.grid-cols-2.md\\:grid-cols-3 .thumbnail.group')),'page':pg}

    def playerContent(self, flag, id, vipFlags):
        p=0 if '嗅' in flag else 1
        return {'parse': p, 'url': id, 'header': self.headers}

    def localProxy(self, param):
        pass

    def getpq(self, response):
        response=response.text
        try:
            return pq(response)
        except Exception as e:
            print(f"{str(e)}")
            return pq(response.encode('utf-8'))

    def getlist(self,data):
        videos = []
        for i in data.items():
            k = i('.overflow-hidden.shadow-lg a')
            id=k.eq(0).attr('href')
            if id:
                videos.append({
                    'vod_id': id,
                    'vod_name': i('.text-secondary').text(),
                    'vod_pic': k.eq(0)('img').attr('data-src'),
                    'vod_year': '' if len(list(k.items())) < 3 else k.eq(1).text(),
                    'vod_remarks': k.eq(-1).text(),
                    'style': {"type": "rect", "ratio": 1.33}
                })
        return videos

    def execute_js(self, js_code):
        """
        使用项目中的QuickJS执行JavaScript代码
        """
        try:
            # 导入Java类
            from com.whl.quickjs.wrapper import QuickJSContext
            self.log("成功导入QuickJSContext类")
            ctx = QuickJSContext.create()
            ctx.evaluate(js_code)
            result = []
            common_vars = ["source", "source842", "source1280"]

            for var_name in common_vars:
                try:
                    value = ctx.getGlobalObject().getProperty(var_name)
                    if value is not None:
                        if isinstance(value, str):
                            value_str = value
                        else:
                            value_str = value.toString()
                        if "http" in value_str:
                            result.append(f"{var_name}${value_str}")
                            self.log(f"找到变量 {var_name} = {value_str[:50]}...")
                except Exception as var_err:
                    self.log(f"获取变量 {var_name} 失败: {var_err}")
                    # 释放资源
            self.log("释放QuickJS资源...")
            ctx.destroy()
            return '#'.join(result)

        except Exception as e:
            self.log(f"执行JavaScript代码失败: {e}")

            return None
