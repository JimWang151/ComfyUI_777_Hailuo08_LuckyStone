import os
import xml.etree.ElementTree as ET
import random
from typing import List
from PIL import Image
import shutil
import subprocess
from torchvision.transforms.functional import to_tensor

class XMLReader:
    def __init__(self, file_path):
        # 解析 XML 文件
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

        self.supported_font_extensions = [".ttf"]
        self.destination_font_dir = "/usr/share/fonts/"  # 硬编码字体安装目标目录

        # 获取当前目录下的 font 文件夹路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.fonts_dir = os.path.join(current_dir, "font")

        self.install_font_batch()  # 自动安装字体

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
        "Joy and happiness": "Joy_Happiness"
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
                        "Joy and happiness"
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
        # menu = random.choice(['浅色', '深色'])
        menu = '浅色'
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

            return lucky_stone_img, border_img, luckystone['name'], f"{luckystone['meaning']}{luckystone['motivation']}"
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
    def validate_font_file(self, font_path):
        """
        验证字体文件路径和文件类型
        """
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"字体文件 {font_path} 不存在！")

        file_extension = os.path.splitext(font_path)[1]
        if file_extension.lower() not in self.supported_font_extensions:
            raise ValueError(
                f"支持的字体类型为：{'、'.join(self.supported_font_extensions)}，当前文件为 '{file_extension}'！")

    def check_font_installed(self, font_path):
        """
        检查字体文件是否已安装
        """
        self.validate_font_file(font_path)  # 先验证字体文件

        font_file_name = os.path.basename(font_path)
        font_dirs = [self.destination_font_dir, os.path.expanduser("~/.fonts/")]  # 常见的字体目录
        for directory in font_dirs:
            if directory and os.path.exists(directory):
                if font_file_name in os.listdir(directory):
                    return True
        return False

    def install_font(self, font_path):
        """
        将字体文件安装到目标目录
        """
        self.validate_font_file(font_path)  # 验证字体文件

        destination_path = os.path.join(self.destination_font_dir, os.path.basename(font_path))

        # 检查目标目录是否存在，不存在则创建
        if not os.path.exists(self.destination_font_dir):
            os.makedirs(self.destination_font_dir)

        # 复制字体文件到目标目录
        shutil.copy2(font_path, destination_path)

        return destination_path

    @staticmethod
    def refresh_font_cache():
        """
        刷新字体缓存
        """
        try:
            subprocess.run(["fc-cache", "-f"], capture_output=True, check=True)
            print("字体缓存刷新完成！")
        except subprocess.CalledProcessError:
            print("刷新字体缓存失败，请确保系统支持 fc-cache 工具！")

    def install_font_batch(self):
        """
        批量安装字体
        """
        if not os.path.exists(self.fonts_dir):
            raise FileNotFoundError(f"字体文件夹不存在：{self.fonts_dir}！")

        for font_file in os.listdir(self.fonts_dir):
            font_path = os.path.join(self.fonts_dir, font_file)
            if os.path.isfile(font_path) and font_path.lower().endswith(".ttf"):
                try:
                    # 检查字体是否已安装
                    if self.check_font_installed(font_path):
                        print(f"字体 {font_file} 已经安装，跳过安装过程！")
                    else:
                        print(f"正在安装字体 {font_file} 到 {self.destination_font_dir} ...")
                        self.install_font(font_path)
                        print(f"字体 {font_file} 安装成功！")
                except Exception as e:
                    print(f"字体 {font_file} 安装失败：{e}")

        self.refresh_font_cache()
# 使用示例
