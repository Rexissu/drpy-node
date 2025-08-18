"""
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: '集合',
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
import base64
from urllib.parse import unquote
from lxml import etree
import re
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
class Spider(BaseSpider):
    def getName(self):
        return "站点集合"

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass
    headers = {
  'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E230 Safari/601.1",
  'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  'Accept-Language': "zh-CN,zh;q=0.9",
  'Cookie': "user_uuid=7c21cb26-edbc-4128-8a43-462b7a8ded5f; _ga=GA1.1.1284984711.1743438899; _ga_9FFNX13PHD=GS1.1.1743438898.1.1.1743439146.0.0.0; XSRF-TOKEN=eyJpdiI6IjAyTmpycWFrTDJGSW5tNEIrYkhRcVE9PSIsInZhbHVlIjoiUzlnQ0xJQmJzRkIxTTRDS3A2aXpoZ1JSR05UZDZRSVpyaGdaK08zOFFBajRqZUpYa2JUMld4bTR6R1UxcVhoaG9oSi9XQ0Jzc2xqVVBIZE5tblRaQTB5VEpUUXhxSHBhKy80VWVvV3RQZmlxdFR2eE9qVEtXRDNUVGVMbEtVYWIiLCJtYWMiOiI0YzA0OTYwNDk5MDU0YzFjYjE0Y2UxYjEwNDYwYWZjM2M1OTdjNGU0YWU4ODliNTIwOWU0YmY3MDM5ZmQxYjk4IiwidGFnIjoiIn0%3D; missav_session=eyJpdiI6IkNqRzAzWE9nWXQ3blNzdDhtWXA4YXc9PSIsInZhbHVlIjoiY1hXVzJjR2kyejZ0RkRVZzRYc2Q2OGhESzV0OVR0SjVka1gvL3U3bFAzNVZ4a0p2VHRvZEI4M2daZStJN3pucHREMWk4MWYwNWI4TzIxbzJiZU9DYlpDczZZY3JuTStKUmJXY01sa3pEZG9SWUpEQitUcHI2eDVieTNkNHBKV1ciLCJtYWMiOiJjYWYxNTM5ODg3YzI0OWQ4YTAwYTVjNDE5YmM5MTZjOGFlNzhiZWViYmNkMjQ2N2RlN2IwOGY4NjQ2OWQ4YmEzIiwidGFnIjoiIn0%3D; crDl1fnw84Bc8k20aVCPw1AFIDST5hjTq97COFD7=eyJpdiI6IkNNVlIxSTRUMk83cDdiWk1TK0xWcnc9PSIsInZhbHVlIjoiM1VCZE9xTTFJRjNIbGp0S2p4dE9PR3VCTHFSN2hnMUVvNnBlVGhBdHhWMjFsWGd3UWNBZTNyazRURE40NzJIV1cxRzFGSGZMZGdMOEZrSUV2SzZqajRoQ2pQcXF4Y3Q1aG43aXZYZDFDdUxCbHIzd2FaNk9JYUJacW1yNlNnbVoyWi9BWjNLMFpVaTRnR2dNdkVrVFRkY1gweThYb2FuRXpNZk8rM09LR3dtRVdFcGpCb1NRNjZhWXVVeDRxZ3dhL2dvUGF4Z2lVZjUwSzRpQUVTV1VBT0dlVWkrenNNTW1sZEJMVm81SFQ2bjFjOU1YeXErQmdscEV0dW1DM3R1VTM0UC9XS05HQWhlWk1PUWtqbnY0R01SaFVoWEQ4d2w1RGNnMW5XcC9FWVQreFhEVnBjbnlOT3M1dEl0aXF2MEZucE81VVZaa2QyNWl4dlFpQm9zajdWcVRQT0FxRWRCdnRDNkhKSVFLYUxqY0psUE9pZm5mem5pMGhEbE1qKzJQdS8yTzhBYlFNb08vQTRwVWZRMHduZz09IiwibWFjIjoiZGVkMTNiNjY4NzA3ZWJiZDM2NDdjZGEwYzg0YjdlNTI1NGRjMWJiMjIwOWRlY2YyM2QzNWZmNjVlNDU2MGJkNCIsInRhZyI6IiJ9"
    }

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }
    def regStr(self, src, reg, group=1):
        m = re.search(reg, src)
        src = ''
        if m:
            src = m.group(group)
        return src
    def decrypt_Aes(self,url):
        rsp = self.fetch(url)
        base64_encoded_data = base64.b64encode(rsp.content)
        key = b'f5d965df75336270'
        iv = b'97b60394abc2fbe1'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(base64_encoded_data)), AES.block_size)
        return decrypted_bytes
    def homeContent(self, filter):
        result = {}
        cateManual = {
            "300分类":"300",
            "热搜":"hot",
            "资源聚合":"404",
            "xvideos":"xv",
            "小仓库":"ck",
            #"香蕉综合":"xj",
            "玩偶":"hk",
            #"女优":"ny",
            "女优一览":"nyyl",
            "吃瓜":"cg",
            "其他站点待定":"待定"
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_flag':"2",
                'type_id': cateManual[k]
                
            })
        result['class'] = classes
        return result

    def homeVideoContent(self):
        result = {
            'list': []
        }
        '''
        host = 'https://zh.xvideos.help'
        try:
            rsp = self.fetch(host + '/best')
            root = self.html(rsp.text)
            aList = root.xpath('//div[@class="mozaique cust-nb-cols"]/div')
            videos = []
            for a in aList:
                name = a.xpath('./div[2]/p/a/@title')[0]
                pic = a.xpath('./div[1]//img/@data-src')[0]
                sid = a.xpath("./div[2]/p/a/@href")[0]
                try:
                    mark = a.xpath('./div[2]/p/a/span/text()')[0]
                    markb = a.xpath('.//span[@class="video-hd-mark"]/text()')[0]
                except Exception as e:
                    None
                videos.append({
                    "vod_id": host + sid,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": mark + " (" + markb + ")"
                })
            result = {
                'list': videos
            }
        except Exception as e:
            pass
        '''
        return result
    def __init__(self):
        #self.xavHost = self.getxavHost()
        #https://www.pornlulu.com
        #self.Host = "https://www.pornbest.org"
        #self.Host = "https://www.yhrg.net"
        self.Host = "https://www.pornlulu.net"
        #self.homeUrl = "https://www.pornbest.org/node/keywords"
        self.homeUrl = self.Host + "/node/keywords"
        self.ckHost = "https://wangbaomen136.buzz"
        self.xjHost = "https://28ggxx.vip"
        self.hkHost = "https://hongkongdollvideo.com"
        self.nyHost = "https://avtop10.com"
        self.nyylHost = "https://missav.mrst.one/"
        self.xvHost = "https://zh.xvideos.help"
        self.cgHost = "https://beside.dhcpzck.xyz"
        #https://www.13av.com/
    '''def getxavHost(self):
        try:
            findrsp = self.fetch("https://findme-404.404xav.top/jump/")
            xavHost = self.regStr(findrsp.text, '(https://[^\s]+)/')
        except Exception as e:
            xavHost = None
        return xavHost
    '''
    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        videos = []
        #300
        if tid == "300":
            page = 1
            rsp = self.fetch(self.Host,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//ul[@id="w4"]//a')
            for a in aList:
                name = a.xpath('./p/text()')[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    "vod_id":sid,
                    "vod_name":name,
                    "style":{"type": "grid", "ratio": 1},
                    "vod_tag":"folder"
                })
        #300
        elif tid.startswith('/cat'):
            page = 99
            hotUrl = self.Host + tid +"?page=" + pg
            rsp = self.fetch(hotUrl)
            root = self.html(rsp.text)
            aList = root.xpath('//div[@id="videos"]//img/..')
            videos = []
            for a in aList:
                name = a.xpath('./img/@alt')[0]
                pic = a.xpath('./img/@src')[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    "vod_id": self.Host + sid,
                    "vod_name": name,
                    "vod_tag":"file",
                    "vod_pic": pic
                })
        #404
        elif tid == "404":
            page = 1
            rsp = self.fetch("https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433.one/")
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath("//div[@class='index_list']/a")
            for a in aList:
                name = a.xpath('./text()')[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    "vod_id":"one" + sid,
                    "vod_name":name,
                    "vod_tag":"folder"
                })
        #女优一览
        elif tid == "nyyl":
            page = 9999
            url = self.nyylHost+"cn/actresses?page=" + pg
            rsp = self.fetch(url,headers=self.headers)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="space-y-4"]')
            for a in aList:
                name = a.xpath(".//h4/text()")[0]
                sid = a.xpath("./a/@href")[0]
                try:
                    pic = a.xpath("./a//img/@src")[0]
                except Exception as e:
                    pic = ""
                remark = a.xpath(".//p[1]/text()")[0]
                videos.append({
                    "vod_id": unquote(sid),
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark,
                    "style":{"type": "full", "size": 0.75},
                    "vod_tag":"folder"
                })
        #女优一览
        elif tid.startswith(self.nyylHost):
            page = 999
            url = tid + "?page=" + pg
            rsp = self.fetch(url,headers=self.headers)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="relative aspect-w-16 aspect-h-9 rounded overflow-hidden shadow-lg"]')
            for a in aList:
                name = a.xpath("./a//img/@alt")[0]
                sid = a.xpath("./a/@href")[0]
                try:
                    pic = a.xpath("./a//img/@data-src")[0]
                except Exception as e:
                    pic = ""
                try:
                    remark = a.xpath("./a[2]/span/text()")[0]
                except Exception as e:
                    remark = ""
                videos.append({
                    "vod_id": unquote(sid),
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark,
                    "vod_tag":"file"
                })
        #xvideos
        elif tid == "xv":
            page = 1
            rsp = self.fetch(self.xvHost,headers=self.header)
            root = self.html(rsp.text)
            aList = root.xpath('//ul[@id="main-cats-sub-list"]/li')
            for a in aList:
                name = a.xpath("./a/text()")[0]
                sid = a.xpath("./a/@href")[0]
                if sid.startswith("/tags"):
                    sid = sid
                elif "k=" in sid:
                    sid = self.xvHost + sid.replace("top", "p=")
                else:
                    s
