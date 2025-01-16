const {requestHtml} = $.require('./_lib.request.js');

const rule = {
    title: '吃瓜[密]',
    host: 'https://h4dez1.vojrq1.net',
    url: 'fyclass/fypage',
    searchUrl: '/index/search_article?word=**&page=fypage',
    searchable: 1,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    },
    class_parse: async function () {
        let html = await requestHtml(rule.host, {
            headers: rule.headers
        });
        let classes = []
        const $ = pq(html)
        for (const it of $(".joe_header__above-nav a")) {
            const name = it.attribs.title
            const href = it.attribs.href
            if (name === "官方公告") {
            break;
        }
            classes.push({
                type_id: href,
                type_name: name
            })
        }
        return {
            class: classes
        }
    },
    hikerListCol: "card_pic_1",
    hikerClassListCol: "movie_3_marquee",
    lazy: async function (flag, id, flags) {
        let {input} = this
        return {parse: 0, url: id}
    },
    play_parse: true,
    limit: 6,
    proxy_rule: async function () {
        let {input} = this
        if (input) {
            let t1 = new Date().getTime();
            let _type = input.split('.').slice(-1)[0];
            let data = (await req(input, {
                headers: rule.headers,
                buffer: 2
            })).content;
            let t2 = new Date().getTime();
            // let encrypted = Image_decrypt('f5d965df75336270', '97b60394abc2fbe1', data);
            let encrypted = Image_decrypt2('f5d965df75336270', '97b60394abc2fbe1', data);
            // .toString(CryptoJS.enc.Utf8).toTypedArray(CryptoJS.enc.Utf8); //直接转参数3可用的字节流方法
            let img_base64 = 'data:image/' + _type + ';base64,' + encrypted;
            let t3 = new Date().getTime();
            log(`已获取图片${input}解密耗时:${t3 - t2}ms`);
            // // input = [200, 'text/plain', img_base64];
            // input = [302, 'text/html', '', {Location:'https://www.baidu.com'}];
            return [200, 'image/' + _type, img_base64, null, 1];
            // input = [200, 'text/plain', data];
        }
    },
    预处理: async function () {
        rule.cate_exclude = '';
    },
    推荐: async () => {
        return []
    },
    //推荐: async function () {
       // let 一级 = rule.一级.bind(this);
    //    return await 一级('/category/0.html', '1');
   // },
    一级: async function (tid, pg, filter, extend) {
        let {getProxyUrl, input, MY_CATE} = this
        let d = [];
        let html = await requestHtml(`${rule.host}${tid}${pg}`, {
            headers: rule.headers
        });
        let list = pdfa(html, '.joe_archive__list joe_list&&li&&a');
        list.forEach(item => {
            const pic = pdfh(item, 'img&&onload').match(/'(.*?)'/)[1];
            const url = pdfh(item, 'a&&href');
            const title = pdfh(item, '.title&&Text').trim().replace('\n', '');
            if (pic.indexOf('.gif') < 0) {
                d.push({
                    title: title,
                    url: url,
                    desc: "",
                    pic_url: getProxyUrl() + '&url=' + pic,
                });
            }
        });
        return setResult(d);
    },
    二级: async function (ids) {
        let {input} = this
        let _url = ids[0] && ids[0].startsWith('http') ? ids[0] : `${rule.host}${ids[0]}`;
        const html = await requestHtml(_url, {
            headers: rule.headers
        });
        const $ = pq(html)
        let vod = {
            vod_id: `${rule.host}${ids[0]}`,
            vod_name: $('title').text()
        }
        const play_url = JSON.parse($('.dplayer').attr('config')).video.url
        let playFroms = [];
        let playUrls = [];
        const temp = [];
        temp.push(vod.vod_name + '$' + play_url)
        playFroms.push('不知道倾情打造');
        playUrls.push(temp.join('#'));
        vod.vod_play_from = playFroms.join('$$$');
        vod.vod_play_url = playUrls.join('$$$');
        return vod
    },
    搜索: async function (wd, quick, pg) {
        let {input, getProxyUrl} = this;
        let d = [];
        let u = input.split("?");
        let h = await post(u[0], {
            body: u[1]
        });
        let list = JSON.parse(h).data.list;
        list.forEach(item => {
            let pic = item.thumb;
            let url = `${rule.host}/archives/${item.id}.html`
            d.push({
                title: item.title,
                desc: item.created_date,
                // img: pic,
                img: getProxyUrl() + '&url=' + pic,
                url: url
            });
        });
        return setResult(d);
    }
};

function Image_decrypt(key, iv, data) {
    // key = CryptoJS.enc.Utf8.parse("f5d965df75336270");
    key = CryptoJS.enc.Utf8.parse(key);
    // iv = CryptoJS.enc.Utf8.parse("97b60394abc2fbe1");
    iv = CryptoJS.enc.Utf8.parse(iv);
    return CryptoJS.AES.decrypt({
        ciphertext: CryptoJS.enc.Base64.parse(data)
    }, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString(CryptoJS.enc.Base64)
}

function Image_decrypt2(key, iv, data) {
    key = CryptoJSW.enc.Utf8.parse(key);
    iv = CryptoJSW.enc.Utf8.parse(iv);
    return CryptoJSW.AES.decrypt({
        ciphertext: CryptoJSW.enc.Base64.parse(data)
    }, key, {
        iv: iv,
        mode: CryptoJSW.mode.CBC,
        padding: CryptoJSW.pad.Pkcs7
    }).toString(CryptoJSW.enc.Base64)
}
