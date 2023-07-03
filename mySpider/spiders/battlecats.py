import re

import scrapy
from scrapy import Selector

from mySpider.items import Layer, Stage


class BattlecatsSpider(scrapy.Spider):
    name = "battlecats"
    allowed_domains = ["battlecats-db.com"]
    start_urls = [
        "https://battlecats-db.com/stage/s03000-02.html",
        "https://battlecats-db.com/stage/s03000-03.html",
        "https://battlecats-db.com/stage/s03000-04.html",
    ]

    def start_requests(self):
        for index, url in enumerate(self.start_urls):
            yield scrapy.Request(url, meta={'index': index})

    def parse(self, response):

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

        stage['base_hp'] = stage_item.xpath('./tr[3]//td[@class="R"]/font/text()').get()
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

        yield stage
        pass

    def updateValue(self, name, values, stage):
        for value in values:
            if value:
                stage[name] = value
                break
