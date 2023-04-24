from rest_framework import renderers
import json

class UserRenderers(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        return (
            json.dumps({'errors': data})
            if 'ErrorDetail' in str(data)
            else json.dumps(data)
        )

class ProductRenderers(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        return (
            json.dumps({'errors': data})
            if 'ErrorDetail' in str(data)
            else json.dumps(data)
        )