import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated


from ads.models import Category, Advertisement, Selection
from ads.serializers import CategorySerializer, AdvertisementSerializer, SelectionCreateSerializer, \
    SelectionListSerializer, SelectionRetrieveSerializer
from authentication.models import User
from authentication.permissions import IsAuthor, IsAuthorOrModerator

from myavito import settings


def index(request):
    return JsonResponse({'status': 'ok'}, status=200)


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdvertisementsListView(ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

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

        self.queryset = self.get_queryset(). \
            select_related('author', 'category'). \
            filter(filter_params). \
            order_by('-price')

        return super().get(request, args, kwargs)


class AdvertisementCreateView(CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


class AdvertisementRetrieveView(RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]


class AdvertisementUpdateView(UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrModerator]



@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementImageUpdateView(UpdateView):
    model = Advertisement
    fields = ['image']
    permission_classes = [IsAuthenticated, IsAuthorOrModerator]

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


class AdvertisementDestroyView(DestroyAPIView):
    queryset = Advertisement.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrModerator]


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionRetrieveView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionRetrieveSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.queryset

        return super().post(request, *args, **kwargs)


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class SelectionDestroyView(DestroyAPIView):
    queryset = Selection.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]
