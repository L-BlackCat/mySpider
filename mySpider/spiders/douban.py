import scrapy
from scrapy import Selector

from mySpider.items import EnemyStruct


class DoubanSpider(scrapy.Spider):
    name = "douban"
    # allowed_domains = ["movie.douban.com"]
    # start_urls = ["https://movie.douban.com/top250"]
    allowed_domains = ["battlecats-db.com"]
    start_urls = ["https://battlecats-db.com/stage/s03000-07.html"]

    # def parse(self, response):
    #     sel = Selector(response)
    #     list_items = sel.css('#content > div > div.article > ol > li')
    #     for list_item in list_items:
    #         movie_item = MovieItem()
    #         movie_item['title'] = list_item.css('span.title::text').extract_first()
    #         movie_item['rank'] = list_item.css('span.rating_num::text').extract_first()
    #         movie_item['subject'] = list_item.css('span.inq::text').extract_first()
    #         yield movie_item
    #     pass
    def parse(self, response):
        sel = Selector(response)
        list_items = sel.xpath('//*[@id="List"]/tbody[2]/tr')
        count = 1
        for list_item in list_items:
            enemyStruct = EnemyStruct()
            enemyStruct['enemy_id'] = list_item.xpath('.//td[@class="R"]/text()').get()

            count = count + 1
            yield enemyStruct
        pass
