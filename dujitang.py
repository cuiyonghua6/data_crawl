import requests
	import random
	from lxml import etree
    # 安装：pip install fake_useragent
	from fake_useragent import UserAgent
	
	
	def get_random_ua(): #随机UA
	    ua = UserAgent()
	    return ua.random
	
	headers = {
	    'User-Agent': get_random_ua()
	}
	
	url = 'https://www.nihaowua.com/home.html'
	
	
	def main():  #写入txt文本程序
	    count = 0
	    while True:
	        try:
	            with open("soup.txt", "a", encoding='utf-8') as f:
	                res = requests.get(url=url, headers=headers, timeout=10)
	                selector = etree.HTML(res.text)
	                content = selector.xpath('//section/div/*/text()')[0]
	                text = str(count) + str(content)
	                f.write(text + '\n')
	                count += 1
	                print('*****正在爬取中，这是第{}次爬取，内容为：{}'.format(count, content))
	        except Exception as e:
	            print('exception:', e)
	            continue
	
	
	if __name__ == '__main__':
	    main()