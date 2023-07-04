import os
import re

import pandas as pd
import scrapy
from scrapy import Selector, signals

from mySpider.items import Layer, Stage
from mySpider.pipelines import MyspiderPipeline


class BattlecatsSpider(scrapy.Spider):
    name = "battlecats"
    allowed_domains = ["battlecats-db.com"]
    start_urls = [
        "https://battlecats-db.com/stage/s03000-02.html",
        "https://battlecats-db.com/stage/s03000-03.html",
        "https://battlecats-db.com/stage/s03000-04.html",
        "https://battlecats-db.com/stage/s03000-05.html",
        "https://battlecats-db.com/stage/s03000-06.html",
        "https://battlecats-db.com/stage/s03000-07.html",
        "https://battlecats-db.com/stage/s03000-08.html",
        "https://battlecats-db.com/stage/s03000-09.html",
        "https://battlecats-db.com/stage/s03000-10.html",
        "https://battlecats-db.com/stage/s03000-11.html",
        "https://battlecats-db.com/stage/s03000-12.html",
        "https://battlecats-db.com/stage/s03000-13.html",
        "https://battlecats-db.com/stage/s03000-14.html",
        "https://battlecats-db.com/stage/s03000-15.html",
        "https://battlecats-db.com/stage/s03000-16.html",
        "https://battlecats-db.com/stage/s03000-17.html",
        "https://battlecats-db.com/stage/s03000-18.html",
        "https://battlecats-db.com/stage/s03000-19.html",
        "https://battlecats-db.com/stage/s03000-20.html",
        "https://battlecats-db.com/stage/s03000-21.html",
        "https://battlecats-db.com/stage/s03000-22.html",
        "https://battlecats-db.com/stage/s03000-23.html",
        "https://battlecats-db.com/stage/s03000-24.html",
        "https://battlecats-db.com/stage/s03000-25.html",
        "https://battlecats-db.com/stage/s03000-26.html",
        "https://battlecats-db.com/stage/s03000-27.html",
        "https://battlecats-db.com/stage/s03000-28.html",
        "https://battlecats-db.com/stage/s03000-29.html",
        "https://battlecats-db.com/stage/s03000-30.html",
        "https://battlecats-db.com/stage/s03000-31.html",
        "https://battlecats-db.com/stage/s03000-32.html",
        "https://battlecats-db.com/stage/s03000-33.html",
        "https://battlecats-db.com/stage/s03000-34.html",
        "https://battlecats-db.com/stage/s03000-35.html",
        "https://battlecats-db.com/stage/s03000-36.html",
        "https://battlecats-db.com/stage/s03000-37.html",
        "https://battlecats-db.com/stage/s03000-38.html",
        "https://battlecats-db.com/stage/s03000-39.html",
        "https://battlecats-db.com/stage/s03000-40.html",
        "https://battlecats-db.com/stage/s03000-41.html",
        "https://battlecats-db.com/stage/s03000-42.html",
        "https://battlecats-db.com/stage/s03000-43.html",
        "https://battlecats-db.com/stage/s03000-44.html",
        "https://battlecats-db.com/stage/s03000-45.html",
        "https://battlecats-db.com/stage/s03000-46.html",
        "https://battlecats-db.com/stage/s03000-47.html",
        "https://battlecats-db.com/stage/s03000-48.html",
    ]
    def start_requests(self):
        for index, url in enumerate(self.start_urls):
            yield scrapy.Request(url, callback=self.parse, meta={'index': index})

    def parse(self, response):
        print("enter parse")
        index = response.meta['index']
        global number
        sel = Selector(response)
        current_url = response.url
        match = re.search(r"s(\d+)-(\d+)\.html", current_url)
        if match:
            number = int(match.group(2))
            print(number)  # 输出 "3"
        else:
            print("未找到数字")
        list_items = sel.xpath('//*[@id="List"]/tbody[2]/tr')
        layerId = number * 1000 + 1
        layerList = []
        layerIdList = []
        for list_item in list_items:
            layer = Layer()
            layer['id'] = layerId
            layer['enemy_name'] = list_item.xpath('.//td[3]/text() | .//td[3]/a/text()').get()
            if layer['enemy_name'] == "カンバン娘":
                continue
            layer['strength'] = list_item.xpath(
                './/td[@class="R"][1]/text() | .//td[@class="R"][1]/font/text()').get().replace('％', '')
            layer['number'] = list_item.xpath('.//td[@class="R"][2]/text() | .//td[@class="R"][2]/font/text()').get()
            # //*[@id="List"]/tbody[2]/tr[1]/td[5]/font
            if layer['number'] == "無制限":
                layer['number'] = 999
            else:
                layer['number'] = int(layer['number'])
            layer['base_hp_per'] = list_item.xpath('.//td[@class="R"][3]/text()').get().replace('％', '')
            layer['appear_time'] = list_item.xpath('.//td[@class="R"][4]/text()').get()
            layer['reappear_time_sec'] = list_item.xpath('.//td[@class="R"][5]/text()').get().replace("～", "|")
            layerIdList.append(layerId)
            layerId = layerId + 1
            layerList.append(layer)

        print(layerIdList)

        stage_item = sel.xpath('//*[@id="List"]/thead[1]')
        stage = Stage()
        stage['id'] = number
        stage['bg_image_id'] = 1
        stage['energy'] = stage_item.xpath('./tr[1]/td[@class="R"]/font/text()').get()

        values = stage_item.xpath('./tr[2]//td[@class="R"]/text() | ./tr[2]//td[@class="R"]/font/text()').getall()
        self.updateValue('exp_reward', values, stage)
        #   过滤掉字符串中的非数字字符
        result = ''.join(filter(str.isdigit, stage['exp_reward']))
        stage['exp_reward'] = int(result)

        stage['base_hp'] = stage_item.xpath('./tr[3]//td[@class="R"]/font/text() | ./tr[3]//td[@class="R"]/text()').get()
        result = ''.join(filter(str.isdigit, stage['base_hp']))
        stage['base_hp'] = int(result)

        values = stage_item.xpath('./tr[4]//td[@class="R"]/font/text() | ./tr[4]//td[@class="R"]/text()').getall()
        self.updateValue('stage_width', values, stage)
        result = ''.join(filter(str.isdigit, stage['stage_width']))
        stage['stage_width'] = int(result)

        stage['max_enemies'] = stage_item.xpath(
            './tr[5]//td[@class="R"]/text() | ./tr[5]//td[@class="R"]/font/text()').get()
        result = "|".join(str(item) for item in layerIdList)
        stage['layer_id_list'] = result

        stage['layer_data_list'] = layerList

        # return stage
        yield {
            'index': index,
            'stage': stage
        }
        pass

    def updateValue(self, name, values, stage):
        for value in values:
            if value:
                stage[name] = value
                break