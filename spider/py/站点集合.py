"""
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: '新浪CMS',
  lang: 'hipy'
})
"""

# coding=utf-8
# !/usr/bin/python
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
import time
from urllib import request, parse
import urllib
import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree as et

"""
配置示例:
t4的配置里ext节点会自动变成api对应query参数extend,但t4的ext字符串不支持路径格式，比如./开头或者.json结尾
api里会自动含有ext参数是base64编码后的选中的筛选条件
 {
    "key":"hipy_t4_新浪资源",
    "name":"新浪资源(hipy_t4)",
    "type":4,
    "api":"http://192.168.31.49:5707/api/v1/vod/新浪资源",
    "searchable":1,
    "quickSearch":0,
    "filterable":1,
    "ext":""
},
{
    "key": "hipy_t3_新浪资源",
    "name": "新浪资源(hipy_t3)",
    "type": 3,
    "api": "{{host}}/txt/hipy/新浪资源.py",
    "searchable": 1,
    "quickSearch": 0,
    "filterable": 1,
    "ext": ""
},
"""


class Spider(BaseSpider):  # 元类 默认的元类 type
    def getName(self):
        return "站点集合"  

    filterate = False

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass
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

    config = {
        "player": {},
        "filter": {}
    }
    header = {}

    def localProxy(self, params):
        pic = param['url']
        data = self.decrypt_Aes(pic)
        return [200, "image/jpeg", data]


if __name__ == '__main__':
    from t4.core.loader import t4_spider_init

    spider = Spider()
    t4_spider_init(spider)
    print(spider.homeContent(True))
    print(spider.homeVideoContent())

# T=Spider()
# T. homeContent(filter=False)
# T.custom_classification()
# l=T.homeVideoContent()
# l=T.searchContent(key='柯南',quick='')
# l=T.categoryContent(tid='22',pg='1',filter=False,extend={})
# for x in l['list']:
# 	print(x['vod_name'])
# mubiao= l['list'][2]['vod_id']
# # print(mubiao)
# playTabulation=T.detailContent(array=[mubiao,])
# # print(playTabulation)
# vod_play_from=playTabulation['list'][0]['vod_play_from']
# vod_play_url=playTabulation['list'][0]['vod_play_url']
# url=vod_play_url.split('$$$')
# vod_play_from=vod_play_from.split('$$$')[0]
# url=url[0].split('$')
# url=url[1].split('#')[0]
# # print(url)
# m3u8=T.playerContent(flag=vod_play_from,id=url,vipFlags=True)
# print(m3u8)
