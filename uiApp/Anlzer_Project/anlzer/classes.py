from .mixins import *
from django.views.generic import *


class JSONListView(JSONResponseMixin, ListView):

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)