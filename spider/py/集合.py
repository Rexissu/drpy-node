# coding=utf-8
# !/usr/bin/python
# 小司机出品 https://a1.zinjljz.cc/
import sys
import requests
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


class Spider(BaseSpider):  # 元类 默认的元类 type
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
                    sid = self.xvHost + sid + "/"
                videos.append({
                    "vod_id": unquote(sid),
                    "vod_name": name,
                    "vod_tag":"folder"
                })
            videos.insert(0, videos.pop())
        #xvideos
        elif tid.startswith("/tags"):
            page = 1
            rsp = self.fetch(self.xvHost + tid,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//ul[@id="tags"]/li')
            for a in aList:
                name = a.xpath("./a/b/text()")[0]
                sid = a.xpath("./a/@href")[0]
                mark = a.xpath("./a/span/text()")[0]
                videos.append({
                    "vod_id": self.xvHost + sid + "/",
                    "vod_name": name,
                    "vod_remarks": "共有" + mark + "部",
                    "vod_tag":"folder"
                })
        #xvideos
        elif tid.startswith(self.xvHost):
            page = 9999
            offset = str(int(pg) - 1)
            url = tid + offset
            rsp = self.fetch(url)
            root = self.html(self.cleanText(rsp.text))
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
                    "vod_id": self.xvHost + sid,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_tag": "file",
                    "vod_remarks": mark + " (" + markb + ")"
                })
        #小仓库
        elif tid == "ck":
            page = 1
            rsp = self.fetch(self.ckHost,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="nav"]/a[not(contains(text(), "首页"))]')
            for a in aList:
                name = a.xpath("./text()")[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    "vod_id": sid,
                    "vod_name": name,
                    "vod_tag":"folder"
                })
        #香蕉
        elif tid == "xj":
            page = 1
            rsp = self.fetch(self.xjHost,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//strong/a')
            for a in aList:
                name = a.xpath("./text()")[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    "vod_id": sid,
                    "vod_name": name,
                    "vod_tag":"folder"
                })
        #玩偶
        elif tid == "hk":
            page = 1
            rsp = self.fetch(self.hkHost,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//ul[@class="menu"]/li/a')
            for i, a in enumerate(aList):
                if i != 1:
                    name = a.xpath("./text()")[0]
                    sid = a.xpath("./@href")[0]
                    videos.append({
                        "vod_id": sid,
                        "vod_name": name,
                        "vod_tag":"folder"
                    })
        #女优
        elif tid == "ny":
            page = 99
            nyUrl = self.nyHost + f'/acter/index---{pg}.html'
            rsp = self.fetch(nyUrl,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="item-tags grid grid-cols-tags-8"]/div')
            for a in aList:
                name = a.xpath(".//b/text()")[0]
                sid = a.xpath("./span[1]/a/@href")[0]
                sid = self.regStr(sid,"(/.*?).html")
                pic = a.xpath(".//img/@data-original")[0]
                mark = a.xpath('.//em/text()')[0]
                videos.append({
                    "vod_id": sid,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": mark,
                    "vod_tag":"folder"
                })
        #吃瓜
        elif tid == "cg":
            page = 1
            rsp = self.fetch(self.cgHost,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//ul[@class="list"]/li/a')
            for i, a in enumerate(aList):
                if i > 0:
                    name = a.xpath("./text()")[0]
                    sid = a.xpath("./@href")[0]
                    videos.append({
                        "vod_id": self.cgHost + sid,
                        "vod_name": name,
                        "vod_tag":"folder"
                    })
        #吃瓜
        elif tid.startswith(self.cgHost):
            page = 99
            url = tid + pg
            rsp = self.fetch(url,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//h2[@class="post-card-title"]/../../../..')
            videos = []
            for a in aList:
                pic = a.xpath('.//script[contains(text(), "loadBannerDirect")]/text()')[0].split("'")[1]
                name = a.xpath('.//h2/text()')[0]
                mark = a.xpath('.//span[@itemprop="datePublished"]/text()')[0]
                sid = a.xpath("./@href")[0]
                realPic = self.getProxyUrl() + '&url=' + pic
                videos.append({
                    "vod_id": self.cgHost + sid,
                    "vod_name": name,
                    "vod_remarks": mark,
                    "vod_tag": "file",
                    "style":{"type": "rect", "ratio": 1.8},
                    "vod_pic": realPic
                })
        #热搜
        elif tid == "hot":
            page = 999
            rsp = self.fetch(self.homeUrl)
            root = self.html(rsp.text)
            aList = root.xpath('//a[@class="btn btn-primary btn-sm tag"]')
            for a in aList:
                name = a.xpath("./text()")[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    #"vod_id": '/q/' + name,
                    "vod_id": sid,
                    "vod_name": name,
                    "vod_pic":"",
                    "style":{"type": "oval", "ratio": 2.2},
                    "vod_tag":"folder"
                })
        #香蕉
        elif "?ttvip=" in tid:
            page = 1
            url = self.xjHost + tid
            rsp = self.fetch(url,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//ul[@class="primary"]/li/a[not(contains(text(), "首页"))]')
            for a in aList:
                name = a.xpath("./text()")[0]
                sid = a.xpath("./@href")[0]
                sid = self.regStr(sid,"(/.*?).html")
                videos.append({
                    "vod_id": self.xjHost + sid,
                    "vod_name": name,
                    "vod_tag":"folder"
                })
        #香蕉
        elif tid.startswith(self.xjHost):
            page = 99
            if "/zb/" in tid:
                url = tid + ".html"
            else:
                url = tid + "-" + pg + ".html"
            rsp = self.fetch(url,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="margin-fix"]/div/a')
            videos = []
            for a in aList:
                name = a.xpath('./@title')[0]
                pic = a.xpath('.//img/@data-original')[0]
                mark = a.xpath('.//div[@class="duration"]/text()')[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    "vod_id": self.xjHost + sid,
                    "vod_name": name,
                    "vod_remarks": mark,
                    "vod_tag":"file",
                    "vod_pic": pic
                })
        #玩偶
        elif tid.startswith(self.hkHost):
            page = 99
            url = tid + pg + ".html"
            rsp = self.fetch(url,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="row"]/div[@class="video-item"]')
            videos = []
            for a in aList:
                name = a.xpath('./div/a/img/@alt')[0]
                try:
                    pic = a.xpath('.//img/@data-src')[0]
                except Exception as e:
                    pic = ""
                try:
                    year = a.xpath('.//div[@class="date"]/text()')[0]
                except Exception as e:
                    year = ""
                try:
                    mark = a.xpath('.//div[@class="duration"]/text()')[0] 
                except Exception as e:
                    mark = ""  
                sid = a.xpath("./div/a/@href")[0]
                videos.append({
                    "vod_id": sid,
                    "vod_name": name,
                    "vod_remarks": mark,
                    "vod_tag":"file",
                    "style":{"type": "rect", "ratio": 1.3},
                    "vod_year":year,
                    "vod_pic": pic
                })
        #女优
        elif tid.startswith("/acter"):
            page = 99
            url = self.nyHost + tid + f'---{pg}.html'
            rsp = self.fetch(url,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="item-new grid grid-cols-wide gap-15-20"]/div/a')
            videos = []
            for a in aList:
                name = a.xpath('./@title')[0]
                pic = a.xpath('.//img/@data-original')[0]
                mark = a.xpath('.//i/text()')[0]
                sid = a.xpath("./@href")[0]
                videos.append({
                    "vod_id": self.nyHost + sid,
                    "vod_name": name,
                    "vod_remarks": mark,
                    "vod_tag":"file",
                    "style":{"type": "rect", "ratio": 1.5},
                    "vod_pic": pic
                })
        #热搜
        elif tid.startswith('/q'):
            page = 99
            hotUrl = self.Host + tid +"?page=" + pg
            rsp = self.fetch(hotUrl)
            root = self.html(rsp.text)
            aList = root.xpath('//div[@class="card"]')
            videos = []
            for a in aList:
                name = a.xpath('.//div[@class="card-body p-2"]//a/text()')[0]
                pic = a.xpath('.//img/@src')[0]
                sid = a.xpath('.//div[@class="card-body p-2"]//@href')[0]
                videos.append({
                    "vod_id": self.Host + sid,
                    "vod_name": name,
                    "vod_tag":"file",
                    "vod_pic": pic
                })
        #小仓库
        elif tid.startswith('/type'):
            page = 1
            url = self.ckHost + tid
            rsp = self.fetch(url,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="links"]/a[contains(@href, "/type")]')
            for a in aList:
                name = a.xpath("./text()")[0]
                sid = a.xpath("./@href")[0]
                sid = self.ckHost + self.regStr(sid,"(/type/.*?).html")
                '''picrsp = self.fetch(sid,headers=self.header)
                picroot = self.html(self.cleanText(picrsp.text))
                pic = picroot.xpath('//div[@class="vods"]/div[@class="vod"][1]//img/@data-original')'''
                videos.append({
                    "vod_id": sid,
                    "vod_name": name,
                    #"vod_pic": pic,
                    "vod_tag":"folder"
                })
        #小仓库
        elif tid.startswith(self.ckHost):
            page = 99
            extend['page'] = '/' + pg
            url = tid + extend['page']
            rsp = self.fetch(url,headers=self.header)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="vod"]')
            for a in aList:
                name = a.xpath('./div[@class="vod-txt"]/a/text()')[0]
                pic = a.xpath('./div[@class="vod-img"]//img/@data-original')[0]
                sid = a.xpath('./div[@class="vod-txt"]/a/@href')[0]
                sid = sid.replace("info","play")
                videos.append({
                    "vod_id": self.ckHost + sid,
                    "vod_name": name,
                    "vod_tag":"file",
                    "vod_pic": pic
                })
        #404
        elif tid.startswith('one/type'):
            page = 1
            url = "https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433." + tid
            rsp = self.fetch(url)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath("//div[@class='web_api_types']/a")
            videos.append({
                "vod_id":"https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433." + tid + "/0",
                "vod_name":"所有分类",
                "vod_tag":"folder"
            })
            for a in aList:
                name = a.xpath('./text()')[0]
                sid = a.xpath("./@href")[0]
                sid = self.regStr(sid,"(/type/.*?).html")
                videos.append({
                    "vod_id":"https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433.one" + unquote(sid),
                    "vod_name":name,
                    "vod_tag":"folder"
                })
        #404
        elif tid.startswith("https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433.one"):
            page = 99
            url = tid + '/' + pg + '/.html'
            rsp = self.fetch(url)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath("//div[@class='web_list_box']/a")
            for a in aList:
                name = a.xpath('.//span[@class="item_title"]/text()')[0]
                pic = a.xpath('.//img/@data-original')[0]
                sid = a.xpath("./@href")[0]
                try:
                    mark = a.xpath(".//span[@class='item_time']/text()")[0]
                except Exception as e:
                    mark = None
                videos.append({
                    "vod_id":"https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433.one" + sid,
                    "vod_name":name,
                    "vod_pic":pic,
                    "vod_tag":"file",
                    "vod_remarks":mark
                })
        else:
            pass
        result['list'] = videos
        result['page'] = 1
        result['pagecount'] = page
        result['limit'] = 9999
        result['total'] = 999999
        return result    
    
    def detailContent(self, array):
        id = array[0]
        result = {}
        if id.startswith(self.nyHost):
            rsp = self.fetch(id)
            root = self.html(self.cleanText(rsp.text))
            aList = root.xpath('//div[@class="play-url items-center flex p-4"]')
            vodItems = []
            for a in aList:
                href = a.xpath('./a/@href')[0]
                name = a.xpath('.//i/text()')[0]
                vodItems.append(name + "$" + href)
            play_url = '#'
            vodItems.reverse()
            play_url = play_url.join(vodItems)
            vod = {
                "vod_id": id,
                "vod_name": "",
                "vod_pic": '',
                "vod_content": "🔥小司机出品,必属精品",
                "vod_play_from": "线路首选Missav",
                "vod_play_url": play_url
            }
        
        else:
            vod = {
                "vod_id": id,
                "vod_name": "",
                "vod_pic": '',
                "vod_content": "🔥小司机出品,必属精品",
                "vod_play_from": "精彩线路",
                "vod_play_url": "播放$" + id
            }
        result = {
            'list': [
                 vod
            ]
        }
        return result
    def searchContent(self, key, quick, pg="1"):
        # '''if key.startwith("女优")
            # searchUrl = self.nyHost + "/acter"
            # rsp = self.fetch(url,headers=self.header)
            # root = self.html(self.cleanText(rsp.text))
            # aList = root.xpath('//div[@class="vod"]')
            # for a in aList:
                # name = a.xpath('./div[@class="vod-txt"]/a/text()')[0]
                # pic = a.xpath('./div[@class="vod-img"]//img/@data-original')[0]
                # sid = a.xpath('./div[@class="vod-txt"]/a/@href')[0]
                # sid = sid.replace("info","play")
                # videos.append({
                    # "vod_id": self.ckHost + sid,
                    # "vod_name": name,
                    # "vod_tag":"file",
                    # "vod_pic": pic
                # })
        # else:'''
        # searchUrl = self.xavHost + "/search"
        # mainrsp = self.fetch(self.xavHost)
        # mainroot = self.html(self.cleanText(mainrsp.text))
        # nameList = mainroot.xpath("//div[@class='apilist']/ul/li/a/text()")
        # videos = []
        # urls = []
        # names = []
        # for i, name in enumerate(nameList):
        #     if i < 3:
        #         continue
        #     url = searchUrl + f'/{name}/{key}.html'
        #     urls.append(url)
        #     names.append(name)
        # with ThreadPoolExecutor() as executor:
        #     urlList = list(executor.map(self.fetch, urls))
        # for rsp, urlname in zip(urlList, names):
        #     try:
        #         root = self.html(self.cleanText(rsp.text))
        #         aList = root.xpath("//span[@class='vodtime']/..")
        #     except Exception as e:
        #         continue
        #     for a in aList:
        #         vodname = a.xpath('./span[@class="vodname"]/text()')[0]
        #         pic = a.xpath('./img/@data-original')[0]
        #         sid = a.xpath("./@href")[0]
        #         videos.append({
        #             "vod_id": self.xavHost + sid,
        #             "vod_name": vodname,
        #             "vod_pic": pic,
        #             "vod_remarks": urlname,
        #             "vod_tag": "file"
        #         })
        # result = {
        #     'list':videos
        # }
        searchUrl = "https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433.one" + "/search"
        mainrsp = self.fetch("https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433.one")
        mainroot = self.html(self.cleanText(mainrsp.text))
        nameList = mainroot.xpath("//div[@class='index_list']/a/text()")
        result = {}
        videos = []
        urls = []
        names = []
        for i, name in enumerate(nameList):
            if i < 3:
                continue
            url = searchUrl + f'/{name}/{key}.html'
            urls.append(url)
            names.append(name)
        with ThreadPoolExecutor() as executor:
            urlList = list(executor.map(self.fetch, urls))
        for rsp, urlname in zip(urlList, names):
            try:
                root = self.html(self.cleanText(rsp.text))
                aList = root.xpath("//div[@class='web_list_box']/a")
            except Exception as e:
                continue
            for a in aList:
                try:
                    name = a.xpath('.//span[@class="item_title"]/text()')[0]
                    pic = a.xpath('.//img/@data-original')[0]
                    sid = a.xpath("./@href")[0]
                    try:
                        mark = a.xpath(".//span[@class='item_time']/text()")[0]
                    except Exception as e:
                        mark = None
                    videos.append({
                        "vod_id":"https://xn--40425072111-404xavcom-lk17a1274jxcd.4042433.one" + sid,
                        "vod_name":name,
                        "vod_pic":pic,
                        "vod_tag":"file",
                        #"vod_year":urlname,
                        "vod_remarks":urlname
                    })
                except Exception as e:
                    continue
        result = {
            'list':videos
        }
        return result
    def playerContent(self, flag, id, vipFlags):
        result = {}
        ps = 1
        '''if id.startswith(self.Host):
            ps = 0
            rsp = self.fetch(id,headers=self.header)
            id = self.regStr(rsp.text,'https://www.m3u8hls.com#(.*?.m3u8)') 
        else:
            ps = 1
         '''
        if id.startswith(self.Host):
            rsp = self.fetch(id)
            root = self.html(self.cleanText(rsp.text))
            id = root.xpath('//h1//a/@href')[0]
            result["header"] = self.header
            result["parse"] = ps
            result["playUrl"] = ''
            result["url"] = id
        elif id.startswith(self.hkHost):
            result["header"] = self.header
            result["parse"] = ps
            result["playUrl"] = ''
            result["url"] = id
            result["click"] = "document.getElementById('player-wrapper').click()"
        else:    
            result["header"] = self.header
            result["parse"] = ps
            result["playUrl"] = ''
            result["url"] = id
        return result
    def localProxy(self, param):
        pic = param['url']
        data = self.decrypt_Aes(pic)
        return [200, "image/jpeg", data]
    def isVideoFormat(self, url):
        return not ('afcdn.net' in url) and ('.m3u8' in url) 
    def manualVideoCheck(self):
        pass