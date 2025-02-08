import os
import xml.etree.ElementTree as ET
import random
from typing import List
from PIL import Image
from torchvision.transforms.functional import to_tensor

class XMLReader:
    def __init__(self, file_path):
        # 解析 XML 文件
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    constellation_map = {
        "白羊座": "Aries",
        "金牛座": "Taurus",
        "双子座": "Gemini",
        "巨蟹座": "Cancer",
        "狮子座": "Leo",
        "处女座": "Virgo",
        "天秤座": "Libra",
        "天蝎座": "Scorpio",
        "射手座": "Sagittarius",
        "摩羯座": "Capricorn",
        "水瓶座": "Aquarius",
        "双鱼座": "Pisces"
    }
    expectation_map = {
        "财富自由": "Financial freedom",
        "真爱降临": "True love arrives",
        "健康长寿": "Health and longevity",
        "职业成功": "Career success",
        "家庭和睦": "Family harmony",
        "内心平静": "Inner peace",
        "创意灵感": "Creative inspiration",
        "友情长存": "Enduring friendship",
        "自信提升": "Confidence boost",
        "冒险精神": "Spirit of adventure",
        "学业进步": "Academic progress",
        "快乐幸福": "Joy and Happiness"
    }

    expectation_en_map = {
        "Wealth freedom": "Wealth_Freedom",
        "True love arrives": "True_Love",
        "Health and longevity": "Health_Longevity",
        "Career success": "Career_Success",
        "Family harmony": "Family_Harmony",
        "Inner peace": "Inner_Peace",
        "Creative inspiration": "Creative_Inspiration",
        "Enduring friendship": "Lasting_Friendship",
        "Confidence boost": "Confidence_Boost",
        "Spirit of adventure": "Adventurous_Spirit",
        "Academic progress": "Academic_Progress",
        "Joy and happiness ": "Joy_Happiness"
    }

    reversed_constellation_map = {v: k for k, v in constellation_map.items()}
    reversed_expectation_map = {v: k for k, v in expectation_map.items()}

    # 从模板读取幸运石
    def read_xml(self, username: str, constellation: str, expectation: str):
        stones = []  # 用于存储遍历到的幸运石信息
        # constellation_ch = self.reversed_constellation_map.get(constellation)
        # print(constellation_ch)
        expectation_en = self.expectation_en_map.get(expectation)
        # print(expectation_ch)
        # 访问并获取数据
        for template in self.root.findall('template'):
            for constellations in template.findall('constellation'):
                constellation_id = constellations.get('id')
                # 星座
                if constellation_id == constellation:
                    for expectations in constellations.findall('expectation'):
                        # 期望
                        expectation_id = expectations.get('id')
                        if expectation_id == expectation_en:
                            # 幸运石
                            for stone in expectations.findall('stone'):
                                name = stone.find('name').text
                                meaning = stone.find('meaning').text
                                meaning = (meaning.replace('{name}',name)
                                           .replace('{constellation}',constellation_id)
                                           .replace('{userName}',username))

                                motivation = stone.find('motivation').text
                                prompt = stone.find("prompt")
                                prompt_txt = ''
                                if prompt:
                                    prompt_txt = prompt.text
                                # 将幸运石信息存储在列表中
                                stones.append({'name': name, 'meaning': meaning, 'motivation': motivation, 'prompt': prompt_txt})

        # 随机返回一个幸运石
        if stones:
            random_stone = random.choice(stones)
            return random_stone  # 返回随机选取的幸运石
        else:
            return None  # 如果没有找到幸运石则返回 None

class LuckyStone:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "username": ("STRING", {"default":''}),
                "constellation": ((
                        # "白羊座",
                        # "金牛座",
                        # "双子座",
                        # "巨蟹座",
                        # "狮子座",
                        # "处女座",
                        # "天秤座",
                        # "天蝎座",
                        # "射手座",
                        # "摩羯座",
                        # "水瓶座",
                        # "双鱼座",
                          "Aries",
                          "Taurus",
                          "Gemini",
                          "Cancer",
                          "Leo",
                          "Virgo",
                          "Libra",
                          "Scorpio",
                          "Sagittarius",
                          "Capricorn",
                          "Aquarius",
                          "Pisces"
                      ),
                        {"default": "Aries"}
                ),
                "expectation": ((
                        # "财富自由",
                        # "真爱降临",
                        # "健康长寿",
                        # "职业成功",
                        # "家庭和睦",
                        # "内心平静",
                        # "创意灵感",
                        # "友情长存",
                        # "自信提升",
                        # "冒险精神",
                        # "学业进步",
                        # "快乐幸福",
                        "Wealth freedom",
                        "True love arrives",
                        "Health and longevity",
                        "Career success",
                        "Family harmony",
                        "Inner peace",
                        "Creative inspiration",
                        "Enduring friendship",
                        "Confidence boost",
                        "Spirit of adventure",
                        "Academic progress",
                        "Joy and happiness",
                        ),
                        {"default": "Wealth freedom"}
                ),
            },
        }

    RETURN_TYPES = ("IMAGE","IMAGE","STRING","STRING")
    RETURN_NAMES = ("LogoImage","BorderImage","StoneName","StoneText")
    FUNCTION = "create_stone"
    OUTPUT_NODE = True
    CATEGORY = "HailuoLuckyStone"
    DESCRIPTION = "hailuo luck stone"



    def create_stone(self,username: str, constellation: str, expectation: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, 'data')
        file_path = os.path.join(data_dir, 'template_en.xml')
        xmlreader = XMLReader(file_path)

        luckystone = xmlreader.read_xml(username, constellation, expectation)
        menu = random.choice(['浅色', '深色'])
        if luckystone:
            #星座图片
            img = self.load_image(constellation,menu)
            lucky_stone_img = to_tensor(img)  # 直接转换为 Tensor
            lucky_stone_img = lucky_stone_img.permute(1, 2, 0)
            lucky_stone_img = lucky_stone_img.unsqueeze(0)  # 添加 batch 维度，变为 [1, H, W, 4]

            #边框图片
            img2 = self.load_image('背景底纹',menu)
            border_img = to_tensor(img2)  # 直接转换为 Tensor
            border_img = border_img.permute(1, 2, 0)
            border_img = border_img.unsqueeze(0)  # 添加 batch 维度，变为 [1, H, W, 4]

            return lucky_stone_img,border_img,luckystone['name'],f'{luckystone['meaning']}{luckystone['motivation']}'
        else:
            print("No lucky stone found.")

    # 读取星座模板图片
    def load_image(self,constellation: str, menu: str) -> Image:
        # 初始化一个空列表，用于存储找到的 PNG 文件
        image_list = []
        filename = f'{constellation}.png'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, 'img','constellation',menu)
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            img = Image.open(file_path).convert("RGBA")  # 确保
            image_list.append(img)  # 保存图像以防止被垃圾回收
            return img
        else:
            print(f"文件 {filename} 不存在于 img 文件夹中。")
            file_path = os.path.join(data_dir, 'default.png')
            img = Image.open(file_path).convert("RGBA")  # 确保
            image_list.append(img)  # 保存图像以防止被垃圾回收
            return img

        # return image_list

# 使用示例
if __name__ == "__main__":
    xml_reader = XMLReader('data/template_en.xml')
    userName = '琴海森林'
    constellation = 'Aries'
    expectation = 'Wealth freedom'
    lucky_stone = xml_reader.read_xml(userName, constellation,expectation)
    if lucky_stone:
        print("Randomly Selected Lucky Stone:")
        print(f"标题: {lucky_stone['name']}")
        print(f"姓名: {userName}")
        print(f"寓意: {lucky_stone['meaning']}\n{lucky_stone['motivation']}")
        # print(f"提示词: {lucky_stone['prompt']}")
    else:
        print("No lucky stone found.")