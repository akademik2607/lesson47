from django.core.management.base import BaseCommand
import csv

from ads.models import Advertisement, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.csv_ads_reader()
        self.csv_categories_reader()

    def csv_ads_reader(self):
        results = []
        with open('ads.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            for row in rows:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
                results.append(Advertisement(
                    name=row['name'],
                    author=row['author'],
                    price=row['price'],
                    description=row['description'],
                    address=row['address'],
                    is_published=row['is_published']
                ))
            Advertisement.objects.bulk_create(results)

    def csv_categories_reader(self):
        with open('categories.csv', newline='', encoding='utf-8') as f:
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