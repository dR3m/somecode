from django.http import HttpResponse
from jsonschema import validate, exceptions
from json import loads, decoder
from .models import ImageObj, TaskObj
from django.views import View
from django.shortcuts import render


def verify_json(b):
    try:
        b = loads(b.decode())
    except decoder.JSONDecodeError:
        return None
    schema = {
        "type": "array",
        "properties":{
            "img": {
                "type": "object",
                "required": ["url", "param"],
                "properties": {
                        "url": {
                            "type": "string"
                        },
                        "param": {
                            "type": "number"
                        }

                }
            }
        }
    }

    try:
        validate(b, schema)
    except exceptions.ValidationError:
        b = None
    return b


class IndexView(View):
    def post(self, req):
        resp = HttpResponse()
        resp['Content-Type'] = 'application/json'
        resp.content = 'ok\n'

        b = req.body
        if b:
            urls = verify_json(b)
            if urls:
                t = TaskObj()
                t.set_guid()
                t.save()
                for data in urls:
                    url = data['img']['url']
                    param = data['img']['param']
                    img = ImageObj(task=t)
                    if not img.transform(url, param):
                        img.save()
                        resp.content = t.guid + '\n'
            else:
                resp.content = 'JSON is not valid\n'
        else:
            resp.content = 'body required\n'
        return resp

    def get(self, req):
        guid = req.GET.get('guid')
        if guid:
            imgs = [i.image_path.split('/')[-1] for i in TaskObj.get_task_imgs(guid)]
            return render(req, 'images.html', {"imgs_list": imgs})
        return HttpResponse('param required')


