import scrapy
from scrapy import Selector

from mySpider.items import EnemyStruct, Chapter


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
        enemyStructList = []
        for list_item in list_items:
            enemyStruct = EnemyStruct()
            enemyStruct['enemy_id'] = count
            enemyStruct['level_power'] = list_item.xpath('.//td[@class="R"][1]/text()').get()
            enemyStruct['apper_type'] = list_item.xpath('.//td[@class="R"][2]/text()').get()
            if enemyStruct['apper_type'] is None:
                enemyStruct['apper_type'] = 0
            enemyStruct['apper_tower_left_hp'] = list_item.xpath('.//td[@class="R"][3]/text()').get()
            enemyStruct['apper_sec'] = list_item.xpath('.//td[@class="R"][4]/text()').get()
            enemyStruct['respawn_sec'] = list_item.xpath('.//td[@class="R"][5]/text()').get().replace("～", "|")
            if enemyStruct['respawn_sec'].startswith('-'):
                enemyStruct['respawn_sec'] = 0

            count = count + 1
            enemyStructList.append(enemyStruct)
            # yield enemyStruct

        chapter_item = sel.xpath('//*[@id="List"]/thead[1]')
        chapter = Chapter()
        chapter['ap_cost'] = chapter_item.xpath('./tr[1]/td[@class="R"]/font/text()').get()
        chapter['get_exp'] = chapter_item.xpath('./tr[2]//td[@class="R"]/text()').get()
        chapter['tower_hp'] = chapter_item.xpath('./tr[3]//td[@class="R"]/font/text()').get()
        chapter['stage_wide'] = chapter_item.xpath('./tr[4]//td[@class="R"]/text()').get()
        chapter['enemy_max_cnt'] = chapter_item.xpath('./tr[5]//td[@class="R"]/text()').get()
        chapter['enemy_struct_list'] = enemyStructList

        yield chapter
        pass
