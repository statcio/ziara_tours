# Create your views here.
import random

from django.http import Http404, HttpResponseNotFound
from django.http import HttpResponseServerError
from django.views.generic.base import TemplateView

from tours import data
from tours.data import departures, tours


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['title'] = data.title
        context['subtitle'] = data.subtitle
        context['description'] = data.description
        context['departures'] = data.departures
        context['tours'] = data.tours
        context['tours'] = random.sample(data.tours.items(), 6)
        return context


class TourView(TemplateView):
    template_name = 'tour.html'

    def get_context_data(self, id, **kwargs):
        context = super(TourView, self).get_context_data(**kwargs)
        context['title'] = data.title
        context['departures'] = data.departures
        context['tours'] = tours[id]
        return context


class DepartureView(TemplateView):
    template_name = 'departure.html'

    def get_context_data(self, departure, **kwargs):
        context = super().get_context_data(**kwargs)
        tours_departure = [[tour_id, tour] for tour_id, tour in tours.items()
                           if tour['departure'] == departure]
        min_price = min([t[1]['price'] for t in tours_departure])
        max_price = max([t[1]['price'] for t in tours_departure])
        min_nights = min([t[1]['nights'] for t in tours_departure])
        max_nights = max([t[1]['nights'] for t in tours_departure])
        context['min_price'] = min_price
        context['max_price'] = max_price
        context['min_nights'] = min_nights
        context['max_nights'] = max_nights
        context['title'] = data.title
        context['departures'] = data.departures
        if departure not in data.departures:
            raise Http404
        context['tours'] = dict((key, value) for (key, value) in data.tours.items() if value['departure'] == departure)
        context['departure'] = departures[departure]
        return context


def custom_handler500(request):
    return HttpResponseServerError('Внутреняя ошибка сервера')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')
