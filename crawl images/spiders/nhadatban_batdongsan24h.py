import scrapy
from datetime import datetime

class NhadatbanSpider(scrapy.Spider):
    name = "nhadatban_batdongsan24h"
    allowed_domains = ["batdongsan24h.com.vn"]
    start_urls = ["https://batdongsan24h.com.vn/bat-dong-san-ban-tai-viet-nam-s32113/-1/-1/-1?page={}".format(page) for page in range(1, 100)]

    def parse(self, response):
        list_nha = response.xpath('//ul[@class="s-list"]/li/a')

        # with open("page.html", 'w', encoding="utf-8") as html_file:
        #     html_file.write(response.text)

        for nha in list_nha: 
            title = nha.xpath(".//@title").get().strip()
            link = nha.xpath(".//@href").get()
            absolute_url = response.urljoin(link)
            ngay_dang = nha.xpath(".//h3/span/text()").get().replace("(", "").replace(")", "")
            gia = nha.xpath(".//div/span[contains(strong, 'Giá:')]/strong[2]/text()").get().replace("\r\n", "").strip()
            dien_tich = nha.xpath(".//div/span[contains(strong, 'Diện tích:')]/span/text()").get().replace("\r\n", "").strip()
            dia_chi = nha.xpath(".//div/span[contains(strong, 'Địa chỉ:')]/em/text()").get().replace("\r\n", "").strip()
            link_img = nha.xpath(".//div/div[@class='sr-image']/img//@src").get()
            
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            yield {
                "title" : title, 
                "link": absolute_url, 
                "ngay_dang": ngay_dang, 
                "gia": gia, 
                "dien_tich": dien_tich, 
                "khu_vuc": dia_chi, 
                "link_img": link_img, 
                "crawl_time": dt_string
            }

            # yield response.follow(url=link, callback=self.parse_nha, meta={'title': title})

    # def parse_nha(self, response):
    #     title = response.request.meta['title']

    #     yield {
    #         "title": title, 
    #         'gia': response.xpath("(//div[@class='o-i-field'])[1]/span[2]/text()").get().replace("\r\n", "").strip()
    #     }
