import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Advertisement, User, Location
from django.core.exceptions import ObjectDoesNotExist

from ads.serializers import UserCreateSerializer, LocationSetSerializer, UserGetSerializer, UserUpdateSerializer
from myavito import settings


def index(request):
    return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, args, kwargs)
        object_list = self.object_list.order_by('name')
        result = []
        for category in object_list:
            result.append({
                'id': category.id,
                'name': category.name,
            })
        return JsonResponse(result, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        quer_object = self.get_object()
        return JsonResponse({
            'id': quer_object.id,
            'name': quer_object.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        result = json.loads(request.body)
        Category.objects.create(**result)

        return JsonResponse(result, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, args, kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementsListView(ListView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        texts = request.GET.getlist('text')
        locations = request.GET.getlist('location')
        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        filter_params = Q()
        if categories:
            filter_params = Q(category__in=categories)

        if texts:
            for text in texts:
                filter_params |= Q(name__icontains=text)

        if locations:
            for location in locations:
                filter_params |= Q(author__locations__name__icontains=location)

        if price_from:
            filter_params &= Q(price__gte=price_from)
        if price_to:
            filter_params &= Q(price__lte=price_to)

        object_list = self.get_queryset(). \
            select_related('author', 'category'). \
            filter(filter_params). \
            order_by('-price')


        page = request.GET.get('page', 1)
        paginator = Paginator(object_list, settings.TOTAL_ON_PAGE)
        result = []
        for ad in paginator.get_page(page):
            result.append({
                'id': ad.id,
                'name': ad.name,
                'author': f'{ad.author.first_name} {ad.author.last_name}',
                'price': ad.price,
                'image': str(ad.image),
                'description': ad.description,
                'is_published': ad.is_published,
                'category': ad.category.name,
            })
        return JsonResponse({
            'items': result,
            'total': paginator.count,
            'num_pages': paginator.num_pages,
        },
            status=200,
            safe=False
        )

@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementCreateView(CreateView):
    model = Advertisement
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        if request.FILES.get('image', ''):
            result = request.POST
            Advertisement.objects.create(
                name=result['name'],
                author=User.objects.get(pk=result['author']),
                price=result['price'],
                description=result['description'],
                is_published=True if result['is_published'] else False,
                image=request.FILES.get('image', ''),
                category=Category.objects.get(pk=result['category']),
            )
        else:
            result = json.loads(request.body)
            Advertisement.objects.create(
                name=result['name'],
                author=User.objects.get(pk=result['author']),
                price=result['price'],
                description=result['description'],
                is_published=True if result['is_published'] else False,
                category=Category.objects.get(pk=result['category']),
            )

        return JsonResponse(result, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementDetailView(DetailView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        query_object = self.get_object()
        return JsonResponse({
            'id': query_object.id,
            'name': query_object.name,
            'author': f'{query_object.author.first_name} {query_object.author.last_name}',
            'price': query_object.price,
            'image': query_object.image.url,
            'description': query_object.description,
            'is_published': query_object.is_published,
            'category': query_object.category.name,
            }
        )

@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementUpdateView(UpdateView):
    model = Advertisement
    fields = ['name', 'author', 'price', 'description', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, args, kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.author = User.objects.get(pk=data['author_id'])
        self.object.price = data['price']
        self.object.description = data['description']
        self.object.category = Category.objects.get(pk=data['category_id'])
        self.object.save()
        return JsonResponse({
                "id": self.object.id,
                "name": self.object.name,
                "author_id": self.object.author.id,
                "author": self.object.author.first_name,
                "price": self.object.price,
                "description": self.object.description,
                "is_published": self.object.is_published,
                "category_id": self.object.category.id,
                "image": str(self.object.image)
            },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementImageUpdateView(UpdateView):
    model = Advertisement
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        file = request.FILES['image']
        self.object.image = file
        self.object.save()
        return JsonResponse({
                "id": self.object.id,
                "name": self.object.name,
                "author_id": self.object.author.id,
                "author": self.object.author.first_name,
                "price": self.object.price,
                "description": self.object.description,
                "is_published": self.object.is_published,
                "category_id": self.object.category.id,
                "image": str(self.object.image)
            }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, args, kwargs)
        return JsonResponse({"status": "ok"}, status=200)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer



class UserUpdateView(UpdateAPIView):
     queryset = User.objects.all()
     serializer_class = UserUpdateSerializer



class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    # model = User
    # success_url = '/'
    #
    # def get(self, request, *args, **kwargs):
    #     super().delete(request, args, kwargs)
    #     return JsonResponse({'status': 'ok'}, status=200)
    #
    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, args, kwargs)
    #     return JsonResponse({'status': 'ok'}, status=200)


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSetSerializer
