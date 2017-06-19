import scrapy

NEW_POSITIONS ="http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=198&typeid=653&orderby=dateline&sortid=192&typeid=653&orderby=dateline&sortid=192&filter=typeid"
INTERVIEW_REPORTS="http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=145&orderby=dateline&sortid=311&orderby=dateline&sortid=311&filter=author&page=1"
SCHOOL_APPLYS="http://www.1point3acres.com/bbs/forum-27-1.html"
TOFEL_EXAM="http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=125&filter=typeid&typeid=472&sortid=313"
PAGE_1 = TOFEL_EXAM

# response.css("span[title^='共']::text").extract_first()
# ' / 28 页'
# response.css("em[id^='authorposton']::text").extract_first()

# rsp.css("a[class='s xst']").extract()
# detail page url

# rsp.css("a[class='s xst']::attr(href)").extract_first()
# get url 
class PostTime(scrapy.Spider):
    name = 'post-time'

    def start_requests(self):
        yield scrapy.Request(url = PAGE_1, callback=self.parse_total_page)

    def parse_total_page(self, rsp):
        total_page_text = rsp.css("span[title^='共']::text").extract_first()
        if(total_page_text):
            total_page = int(total_page_text[3:-1])
            for p in range(1, total_page + 1):
                next_url = PAGE_1 + '&page=' +  str(p)
                #next_url = PAGE_1[:-6] + str(p) + ".html"
                #print('**************')
                #print(next_url)
                yield scrapy.Request(url = next_url, callback=self.parse_list)

    def parse_list(self, rsp):
        post_urls = rsp.css("a[class='s xst']::attr(href)").extract()
        for u in post_urls:
            yield scrapy.Request(url = u, callback = self.parse_date)

    def parse_date(self, rsp):  
        post_on = rsp.css("em[id^='authorposton']::text").extract_first()[3:]
        date, time= post_on.split()
        yield {'date': date, 'time':time}

