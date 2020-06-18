# -*- encoding: utf-8 -*-
import time
import requests
from fake_useragent import UserAgent
from scrapy import Selector

from raokouling.db import session, YoududuanziItem


class YoududuanziSpider(object):

    def __init__(self):
        self.count = 0
        self.headers = {
            'User-Agent': self.get_random_ua()
        }
        self.url = 'https://m.51test.net/raokouling/'

    def get_random_ua(self):  # 随机UA
        ua = UserAgent()
        return ua.random

    def get_content(self):
        response = requests.get(url=self.url, headers=self.headers, timeout=10)
        selector = Selector(text=response.content.decode('gb2312'))
        # selector = etree.HTML(response.content.decode('gb2312'))
        key_info = selector.xpath('//ul[@class="m_kc_con"]/li')
        for key in key_info:
            key_word = key.xpath('./a/text()').extract_first()
            key_href = key.xpath('./a/@href').extract_first()

            # 构造标题请求并访问
            key_url = 'https://m.51test.net' + key_href
            title_response = requests.get(url=key_url, headers=self.headers, timeout=10)
            title_selector = Selector(text=title_response.content.decode('gb2312'))
            # title_selector = etree.HTML(title_response.content.decode('gb2312'))
            title_info = title_selector.xpath('//div[@class="ui-mod-picsummary ui-border-bottom-gray"]/a')
            print(key_word)
            for title in title_info:
                title_name = title.xpath('./h3/text()').extract_first()
                title_href = title.xpath('./@href').extract_first()

                # 构造绕口令详情页请求并访问
                try:
                    detail_url = 'https://m.51test.net' + title_href
                    detail_response = requests.get(url=detail_url, headers=self.headers, timeout=10)
                    detail_selector = Selector(text=detail_response.content.decode('gbk'))
                    # detail_selector = etree.HTML(detail_response.content.decode('gbk'))
                    content_html_list = detail_selector.xpath('//div[@class="content"]').extract()
                    content_html = ''.join(content_html_list) if len(content_html_list) > 0 else None
                    content_list = detail_selector.xpath('//div[@class="content"]/p/text()').extract()
                    content = ''.join(content_list) if len(content_list) > 0 else None
                    if content is None or not content:
                        continue
                except Exception as e:
                    print('出现异常：', e, detail_url)
                    continue
                time.sleep(1)
                table.insert(key_word=key_word,
                             detail_title=title_name,
                             detail_url=detail_url,
                             content_html=content_html,
                             content=content)

    def run(self):
        self.get_content()


if __name__ == '__main__':
    duanzi = YoududuanziSpider()
    table = YoududuanziItem()
    table.creat_table()
    duanzi.run()