from django.core.management.base import BaseCommand
import csv

from ads.models import Advertisement, Category, Location, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.csv_categories_reader()
        self.csv_locations_reader()
        self.csv_user_reader()
        self.csv_ads_reader()


    def csv_ads_reader(self):
        results = []
        with open('ad.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            for row in rows:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
                results.append(Advertisement(
                    name=row['name'],
                    author_id=row['author_id'],
                    price=row['price'],
                    description=row['description'],
                    is_published=row['is_published'],
                    image=row['image'],
                    category_id=row['category_id'],
                ))
            Advertisement.objects.bulk_create(results)

    def csv_categories_reader(self):
        with open('category.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            results = []
            for row in rows:
                results.append(
                    Category(
                        name=row['name']
                    )
                )
            Category.objects.bulk_create(results)

    def csv_locations_reader(self):
        with open('location.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            results = []
            for row in rows:
                results.append(
                    Location(
                        id=row['id'],
                        name=row['name'],
                        lat=row['lat'],
                        lng=row['lng']
                    )
                )
            Location.objects.bulk_create(results)


    def csv_user_reader(self):
        with open('user.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            results = []
            for row in rows:
                user = User(
                    id=row['id'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    username=row['username'],
                    password=row['password'],
                    role=row['role'],
                    age=row['age'],
                )
                user.save()
                user.location.add(Location.objects.get(pk=row['location_id']))

                results.append(user)
            # User.objects.bulk_create(results)
