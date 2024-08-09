import base64
from io import BytesIO
from PIL import Image
from python_rucaptcha.image_captcha import ImageCaptcha

from .dataclasses import CaptchaAnswer

class RuCaptcha:
    @staticmethod
    def save_image(file_name: str, src_base64: str):
        image_data = base64.b64decode(src_base64.split(',')[1])
        img = Image.open(BytesIO(image_data))
        img.save(file_name)
    @staticmethod
    def solve_captcha(TOKEN: str, file_name: str):
        return CaptchaAnswer(**ImageCaptcha(rucaptcha_key=TOKEN) \
            .captcha_handler(captcha_file=file_name))