from django.db import models
from requests import get as method_get
from PIL import Image, ImageOps
import uuid, os
from io import BytesIO


class TaskObj(models.Model):
    guid = models.CharField(max_length=32)

    def set_guid(self):
        self.guid = uuid.uuid1().hex

    @staticmethod
    def get_task_imgs(guid):
        return ImageObj.objects.filter(task__guid=guid)


class ImageObj(models.Model):
    task = models.ForeignKey(TaskObj, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=200)
    SAVE_PATH = os.path.join(os.path.dirname(__file__), '../images/')

    def get_uuid(self):
        return uuid.uuid1().hex

    def download(self, url):
        res = method_get(url)
        if res.ok:
            self.image_path = self.SAVE_PATH + 'img_' + self.get_uuid() + '.jpg'
            return res.content
        else:
            return None

    def transform(self, url, param):
        data = self.download(url)
        if data:
            img = Image.open(BytesIO(data)).convert('L')
            for i in range(img.width):
                for j in range(img.height):
                    if img.getpixel((i, j)) > param:
                        img.putpixel((i, j), 255)  # white
                    else:
                        img.putpixel((i, j), 0)  # black
            img.save(self.image_path)
            return 0
        return 1
