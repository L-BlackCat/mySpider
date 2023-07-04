# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
import os.path
import sys
import time
from threading import Lock

# useful for handling different item types with a single interface

import pandas as pd
from scrapy import signals


class MyspiderPipeline:


    @classmethod
    def from_crawler(cls, crawler):
        spider = crawler.spider
        start_urls = getattr(spider, 'start_urls', None)
        return cls(start_urls=start_urls)


    def __init__(self,start_urls):
        self.count = 0
        self.lock = Lock()
        self.stage_path = 'battlecats_stages.csv'
        self.layer_path = 'battlecats_layer.csv'
        self.collected_items = []
        self.max_count = len(start_urls)

    def open_spider(self, spider):
        #   创建文件并写入表头
        if os.path.exists(self.stage_path):
            os.remove(self.stage_path)

        if os.path.exists(self.layer_path):
            os.remove(self.layer_path)

    def process_item(self, bigItem, spider):
        print("pipline item start")
        print("self.max_count %d " % self.max_count)
        # stage_path = 'battlecats_stages.csv'
        # layer_path = 'battlecats_layer.csv'
        # stage_data = [
        #     [item['id'], item['bg_image_id'], item['energy'], item['exp_reward'], item['base_hp'], item['stage_width'],
        #      item['max_enemies'], item['layer_id_list']]
        # ]
        # stage_columns = ['id', 'bg_image_id', 'energy', 'exp_reward', 'base_hp', 'stage_width', 'max_enemies',
        #                  'layer_id_list']
        # stage_df = pd.DataFrame(stage_data, columns=stage_columns)
        # stage_df.to_csv(stage_path, mode='a+' if os.path.isfile(stage_path) else 'w', header=not os.path.isfile(stage_path), index=False)
        #
        # print("two")
        #
        # all_layer_data = []
        # layer_columns = ['id', 'enemy_name', 'strength', 'number', 'base_hp_per',
        #                  'appear_time', 'reappear_time_sec']
        # layer_data_list = item['layer_data_list']
        # for layer_data in layer_data_list:
        #     # print(layer_data)
        #     layer = [
        #         layer_data['id'], layer_data['enemy_name'], layer_data['strength'],
        #         layer_data['number'], layer_data['base_hp_per'], layer_data['appear_time'],
        #         layer_data['reappear_time_sec']
        #     ]
        #     all_layer_data.append(layer)
        #
        # layer_df = pd.DataFrame(all_layer_data, columns=layer_columns)
        # layer_df.to_csv(layer_path, mode='a+' if os.path.isfile(layer_path) else 'w', header=not os.path.isfile(layer_path), index=False)
        with self.lock:
            self.collected_items.append(bigItem)
            self.count = self.count + 1

        print("pipline item end")
        return bigItem

    def close_spider(self, reason):
        while self.count < self.max_count:
            print("self.count %d self.max_count %d" % (self.count,self.max_count))
            time.sleep(3)
            break
        print("closed and write")
        sorted_data = sorted(self.collected_items, key=lambda x: x['index'])
        for data in sorted_data:
            item = data['stage']
            index = data['index']
            stage_data = [
                [item['id'], item['bg_image_id'], item['energy'], item['exp_reward'], item['base_hp'],
                 item['stage_width'],
                 item['max_enemies'], item['layer_id_list']]
            ]
            stage_columns = ['id', 'bg_image_id', 'energy', 'exp_reward', 'base_hp', 'stage_width', 'max_enemies',
                             'layer_id_list']
            stage_df = pd.DataFrame(stage_data, columns=stage_columns)
            stage_df.to_csv(self.stage_path, mode='a+' if os.path.isfile(self.stage_path) else 'w',
                            header=not os.path.isfile(self.stage_path), index=False)


            all_layer_data = []
            layer_columns = ['id', 'enemy_name', 'strength', 'number', 'base_hp_per',
                             'appear_time', 'reappear_time_sec']
            layer_data_list = item['layer_data_list']
            for layer_data in layer_data_list:
                # print(layer_data)
                layer = [
                    layer_data['id'], layer_data['enemy_name'], layer_data['strength'],
                    layer_data['number'], layer_data['base_hp_per'], layer_data['appear_time'],
                    layer_data['reappear_time_sec']
                ]
                all_layer_data.append(layer)

            layer_df = pd.DataFrame(all_layer_data, columns=layer_columns)
            layer_df.to_csv(self.layer_path, mode='a+' if os.path.isfile(self.layer_path) else 'w',
                            header=not os.path.isfile(self.layer_path), index=False)

        print("all write is ok")

    # def process_item(self, item, spider):
    #     columns = ['ap_cost', 'get_exp', 'tower_hp', 'stage_wide', 'enemy_max_cnt']
    #     data = [[item['ap_cost'], item['get_exp'], item['tower_hp'], item['stage_wide'], item['enemy_max_cnt']]]
    #     df = pd.DataFrame(data, columns=columns)
    #     df.to_csv('stage.csv')
    #     print(df)
    #
    #     enemy_columns = ['enemy_id', 'level_power', 'apper_type', 'apper_tower_left_hp', 'apper_sec', 'respawn_sec']
    #     all_enemy_data = []
    #     enemyStructList = item['enemy_struct_list']
    #     for enemyStruct in enemyStructList:
    #         enemy_data = [enemyStruct['enemy_id'], enemyStruct['level_power'], enemyStruct['apper_type'],
    #                       enemyStruct['apper_tower_left_hp'], enemyStruct['apper_sec'], enemyStruct['respawn_sec']]
    #         all_enemy_data.append(enemy_data)
    #     enemy_df = pd.DataFrame(all_enemy_data, columns=enemy_columns)
    #     enemy_df.to_csv('enemy_struct.csv')
    #     print(enemy_df)
    # # 读取json的内嵌完整数据
    # # jsonPath = os.path.dirname(os.path.dirname(os.getcwd())) + "\\douban.json"
    # # print(jsonPath)
    # # with open(jsonPath, 'r', encoding="utf-8") as f:
    # #     jsonData = json.loads(f.read())
    # #
    # # df_list = pd.json_normalize(jsonData, record_path=['enemy_struct_list'])
    # # print(df_list)
    #
    # with pd.ExcelWriter("output.csv") as writer:
    #     # df.to_excel(writer, index=False, sheet_name='chapter')
    #     df.to_csv(writer, index=False)
    #     enemy_df.to_csv(writer, index=False)
    #
    # return item

    # def open_spider(self, spider):
    #     self.fiele = open('battlecats_stage.csv', 'w', newline='')
    #     self.writer = csv.writer(self.fiele)
    #     self.writer.writerow(['id', 'bg_image_id', 'energy', 'exp_reward', 'base_hp', 'stage_width', 'max_enemies',
    #                           'layer_id_list'])  # 写表头
    #
    # def close_spider(self, spider):
    #     self.fiele.close()
    #
