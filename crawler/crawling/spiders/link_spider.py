import scrapy

from scrapy.log import INFO

from scrapy.http import Request
from lxmlhtml import LxmlLinkExtractor as LinkExtractor
from scrapy.conf import settings
import chardet
from crawling.items import RawResponseItem
from redis_spider import RedisSpider
from pattern.web import plaintext
import json
import uuid
import datetime
class LinkSpider(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "link"

    def __init__(self, *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        self.log("crawled url {}".format(response.request.url), level=INFO)

        cur_depth = 0
        if 'curdepth' in response.meta:
            cur_depth = response.meta['curdepth']

        # capture raw response
        item = RawResponseItem()

        # populated from response.meta
        item['appid'] = response.meta['appid']
        item['crawlid'] = response.meta['crawlid']
        item['attrs'] = response.meta['attrs']

        # populated from raw HTTP response
        item["url"] = response.request.url
        item["response_url"] = response.url
        item["status_code"] = response.status
        item["status_msg"] = "OK"
	html_data = response.body
        item["headers"] = self.reconstruct_headers(response)
	try:
                charset = chardet.detect(html_data)['encoding'].lower()
                if charset != 'utf-8':
                        html_data = html_data.decode(charset,'ignore').encode('utf-8')
                tetxt = plaintext(html_data,keep=[],replace='',linebreaks=1, indentation=False)
        except:
                self.log("No content in %s" % (response.url), level=INFO)
                tetxt = ''
	#item["body"] = response.body
	item["links"] = []
	try:
		item['title'] = tetxt.split('\n')[0]
	except:
		item['title'] = ''
	try:
		split_symbal = '\n'
		item['content'] = split_symbal.join(tetxt.split('\n')[1:])
	except:
		item['content'] = ''
	item['domain_name'] = 'http://'+response.request.url.split('/')[2]+'/'
	nowtime = datetime.datetime.now()
	item['create_time'] = nowtime.strftime('%Y-%m-%d %H:%M:%S')
        # determine whether to continue spidering
        if cur_depth >= response.meta['maxdepth']:
            self.log("Not spidering links in '{}' because" \
                " cur_depth={} >= maxdepth={}".format(
                response.url,
                cur_depth,
                response.meta['maxdepth']), level=INFO)
        else:
            # we are spidering -- yield Request for each discovered link
            link_extractor = LinkExtractor(
                            allow_domains=response.meta['allowed_domains'],
                            allow=response.meta['allow_regex'],
                            deny=response.meta['deny_regex'],
                            deny_extensions=response.meta['deny_extensions'])
            for link in link_extractor.extract_links(response):
                # link that was discovered
                item["links"].append({"url": link.url,"text": link.text, })
		#print response.meta['appid']
                req = Request(link.url,
                        callback=self.parse,
                        meta={
                            "allowed_domains": response.meta['allowed_domains'],
                            "allow_regex": response.meta['allow_regex'],
                            "deny_regex": response.meta['deny_regex'],
                            "deny_extensions": response.meta['deny_extensions'],
                            "maxdepth": response.meta['maxdepth'],
                            "curdepth": cur_depth + 1,
                            "appid": response.meta['appid'],
                            "crawlid": response.meta['crawlid'],
                            "attrs": response.meta['attrs'],
                            "spiderid": self.name,
                            "expires": response.meta['expires'],
                            "priority": response.meta['priority'] - 10,
                            "proxy": response.meta['proxy'],
			},
                        )

                self.log("Trying to follow link '{}'".format(req.url),
                        level=INFO)
                yield req

        # raw response has been processed, yield to item pipeline
        yield item
