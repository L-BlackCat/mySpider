# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os.path
import sys

# useful for handling different item types with a single interface

import pandas as pd

from mySpider.items import Chapter


class MyspiderPipeline:
    def process_item(self, item, spider):
        columns = ['ap_cost', 'get_exp', 'tower_hp', 'stage_wide', 'enemy_max_cnt']
        data = [[item['ap_cost'], item['get_exp'], item['tower_hp'], item['stage_wide'], item['enemy_max_cnt']]]
        df = pd.DataFrame(data, columns=columns)
        print(df)

        enemy_columns = ['enemy_id', 'level_power', 'apper_type', 'apper_tower_left_hp', 'apper_sec', 'respawn_sec']
        all_enemy_data = []
        enemyStructList = item['enemy_struct_list']
        for enemyStruct in enemyStructList:
            enemy_data = [enemyStruct['enemy_id'], enemyStruct['level_power'], enemyStruct['apper_type'],
                          enemyStruct['apper_tower_left_hp'], enemyStruct['apper_sec'], enemyStruct['respawn_sec']]
            all_enemy_data.append(enemy_data)
        enemy_df = pd.DataFrame(all_enemy_data, columns=enemy_columns)
        enemy_df.to_csv('enemy_struct.csv')
        print(enemy_df)
        # 读取json的内嵌完整数据
        # jsonPath = os.path.dirname(os.path.dirname(os.getcwd())) + "\\douban.json"
        # print(jsonPath)
        # with open(jsonPath, 'r', encoding="utf-8") as f:
        #     jsonData = json.loads(f.read())
        #
        # df_list = pd.json_normalize(jsonData, record_path=['enemy_struct_list'])
        # print(df_list)

        with pd.ExcelWriter("output.xlsx") as writer:
            df.to_excel(writer, index=False, sheet_name='chapter')
            enemy_df.to_excel(writer, index=False, sheet_name="enemy_struct")

        return item
