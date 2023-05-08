# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class MovieItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     title = scrapy.Field()
#     rank = scrapy.Field()
#     subject = scrapy.Field()
#     pass
class EnemyStruct(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    enemy_id = scrapy.Field()
    level_power = scrapy.Field()  # 强度倍率
    apper_type = scrapy.Field()  # 出现数
    apper_tower_left_hp = scrapy.Field()  # 城联动
    apper_sec = scrapy.Field()  # 初登场秒数
    respawn_sec = scrapy.Field()  # 再登场
    pass


class Chapter(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ap_cost = scrapy.Field()  # 消费统御力
    get_exp = scrapy.Field()  # 经验值
    tower_hp = scrapy.Field()  # 城体力
    stage_wide = scrapy.Field()  # 舞台宽度
    enemy_max_cnt = scrapy.Field()  # 出击最大数
    enemy_struct_list = scrapy.Field()  # 敌人数据组
    pass