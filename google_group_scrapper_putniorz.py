import time
from BeautifulSoup import BeautifulSoup
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
    source = browser.page_source
    source = source.encode('utf-8')
    frontpage = BeautifulSoup(source)
    index = 0
    user_poll = []
    combiner = {}
    for span in frontpage.findAll("span", "HPFAGND-wb-Q HPFAGND-b-Qb"):
        user_poll.append({'date': span.text.encode('utf-8')})
    index = 0
    for span in frontpage.findAll("span", "HPFAGND-P-a"):
        user_poll[index]['name'] = span.text.encode('utf-8')
        index += 1
    index = 0
    for span in frontpage.findAll("span", "HPFAGND-wb-fb"):
        user_poll[index]['comment'] = span.text.encode('utf-8').replace(",","~")
        index += 1
    browser.quit()
    for x in user_poll:
        if x['name'] in combiner:
            combiner[x['name']] += x['comment']
        else:
            combiner[x['name']] = x['comment']
    with open('yash/googleGroupList.csv', 'a') as f:
        for x in user_poll:
            f.write(x['name']+","+x['date']+","+x['comment']+"\n")
    with open('yash/googleGroupCombine.csv', 'a') as f:
        for x in combiner:
            f.write(x + "," + combiner[x] + "\n")
