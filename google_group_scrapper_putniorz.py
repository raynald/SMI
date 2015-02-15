import time
import xml.etree.ElementTree
from selenium import webdriver

group_url = 'https://groups.google.com/forum/#!topic/light-table-discussion/5YscXFxTLRE'

def thread_to_dict(thread):
    parsed = {'name': thread.xpath('.//a')[0].text}
    parsed['url'] = thread.xpath('.//a')[0].attrib['href']
    raw_last_change = thread.xpath('.//span[@title]')[0].attrib['title']
    last_change = date_parse(raw_last_change)
    parsed['month'] = last_change.month
    info = thread.xpath('.//div[contains(@style,"right")]')[0]
    parsed['seen'] = int(info.xpath('.//span[@class]')[3].text.split()[0])
    parsed['posts'] = int(info.xpath('.//span[@class]')[4].text.split()[0])
    return parsed

if __name__ == '__main__':
    browser = webdriver.PhantomJS()
    browser.set_window_size(1024, 768)
    browser.get(group_url)
    time.sleep(5)
    frontpage = fromstring(browser.page_source)
    browser.quit()
    frontpage.make_links_absolute(GOOGLE_GROUP_BASE)
    html_threads = frontpage.xpath('//div[@role="listitem"]')
    threads = (thread_to_dict(thread) for thread in html_threads)
