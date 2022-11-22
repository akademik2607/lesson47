import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Category, Advertisement, User, Location
from django.core.exceptions import ObjectDoesNotExist

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
        object_list = self.get_queryset().select_related('author', 'category').order_by('-price')
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


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().prefetch_related('location').order_by('username')


        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page = request.GET.get('page', 1)

        result = []
        for user in paginator.get_page(page):
            user.location.all()
            total_ads = Advertisement\
                .objects\
                .filter(is_published=True, author=user)\
                .aggregate(Count('author_id'))['author_id__count']
            result.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'password': user.password,
                'role': user.role,
                'age': user.age,
                'location': [i.name for i in user.location.all()],
                'total_ads': total_ads
            })
        return JsonResponse({
            'items': result,
            'total': paginator.count,
            'num_pages': paginator.num_pages,
        })

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, args, kwargs)

        return JsonResponse({
            'id': self.object.id,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'username': self.object.username,
            'password': self.object.password,
            'role': self.object.role,
            'age': self.object.age,
            'location': [i.name for i in self.object.location.all()],
        })

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        locations = Location.objects.filter(name__in=data.get('locations'))

        user = User.objects.create(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            age=data['age'],
        )
        if not locations:
            for loc in data.get('locations'):
                locations = Location.objects.create(name=loc)
                user.location.add(locations)
        user.save()
        return JsonResponse({
            'id': user.id,
            'username': data['username'],
            'password': data['password'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': data['role'],
            'age': data['age'],
            'locations': data['locations']
        })



@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        locations = Location.objects.filter(name__in=data.get('locations'))

        self.object = self.get_object()
        self.object.first_name = data.get('first_name')
        self.object.last_name = data.get('last_name')
        self.object.username = data.get('username')
        self.object.password = data.get('password')
        self.object.role = data.get('role', 'member')
        self.object.age = data.get('age')
        self.object.location.set(locations)
        self.object.save()

        return JsonResponse({
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'username': data.get('username'),
            'password': data.get('password'),
            'role': data.get('role'),
            'age': data.get('age'),
            'location': data.get('locations'),
        }, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def get(self, request, *args, **kwargs):
        super().delete(request, args, kwargs)
        return JsonResponse({'status': 'ok'}, status=200)

    def delete(self, request, *args, **kwargs):
        super().delete(request, args, kwargs)
        return JsonResponse({'status': 'ok'}, status=200)
