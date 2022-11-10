import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ads.models import Category, Advertisement


def index(request):
    return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = []
        for category in categories:
            result.append({
                'id': category.id,
                'name': category.name,
            })
        return JsonResponse(result, status=200, safe=False)

    def post(self, request):
        result = json.loads(request.body)
        category = Category()
        category.name = result['name']

        category.save()
        return JsonResponse(result, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementsView(View):
    def get(self, request):
        ads = Advertisement.objects.all()
        result = []
        for ad in ads:
            result.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.address,
                'is_published': ad.is_published
            })
        return JsonResponse(result, status=200, safe=False)

    def post(self, request):
        result = json.loads(request.body)
        ad = Advertisement()
        ad.name = result['name']
        ad.author = result['author']
        ad.price = result['price']
        ad.description = result['description']
        ad.address = result['address']
        ad.is_published = result['is_published']

        ad.save()
        return JsonResponse(result, status=200)


class AdvertisementView(View):
    def get(self, request, aid):
        ad = Advertisement.objects.get(id=aid)
        print(ad.name)
        result = {
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.address,
                'is_published': ad.is_published
            }
        return JsonResponse(result, status=200)


class CategoryView(View):
    def get(self, request, cid):
        category = Category.objects.get(id=cid)
        result = {
                'id': category.id,
                'name': category.name,
            }
        return JsonResponse(result, status=200)