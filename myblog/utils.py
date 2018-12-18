import random, string
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from django.core.cache import cache

def get_random_char(count=4):
    ran = string.ascii_lowercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


def get_random_color():
    return random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (120, 30), (255, 255, 255))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('ARLRDBD.TTF', 25)
    code = get_random_char()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30 * t + 5, 0), code[t], get_random_color(), font)
    # 生成干扰点
    for _ in range(random.randint(0, 50)):
        draw.point((random.randint(0, 120),
                    random.randint(0, 30)), fill=get_random_color())
    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.BLUR)
    # 保存
    # img.save(''.join(code)+'.jpg','jpeg')
    return img, code

