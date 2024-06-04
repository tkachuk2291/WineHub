import requests
import random
import re
from django.core.management import BaseCommand
from wine_vault.models import Wine, Winery, Location, Rating, WineType


class Command(BaseCommand):
    help = 'Import wines from API'

    def handle(self, *args, **kwargs):
        vine_list_api = ["reds", "whites", "sparkling", "rose", "dessert", "port"]

        for num in vine_list_api:
            url = f"https://api.sampleapis.com/wines/{num}"
            response = requests.get(url)
            response_json = response.json()
            wine_type, _ = WineType.objects.get_or_create(type=num[:-1] if num.endswith('s') else num)
            for item in response_json:
                rating_data = item.get("rating", {})
                winery, _ = Winery.objects.get_or_create(name=item.get("winery"))
                location = item.get("location")
                if "·" in location:
                    country, region = location.split("\n·\n")
                    location, _ = Location.objects.get_or_create(country=country, region=region)
                else:
                    location, _ = Location.objects.get_or_create(country=country, region="-")
                    print("Invalid region or country")
                    continue
                rating, _ = Rating.objects.get_or_create(
                    average=rating_data.get("average", 0),
                    reviews=rating_data.get("reviews", 0)
                )
                wine_name = item.get("wine", "")
                vintage_match = re.match(r'.*\d{4}$', wine_name)
                vintage = int(wine_name[-4:]) if vintage_match else random.randint(1990, 2024)
                print(winery)
                wine, created = Wine.objects.get_or_create(
                    name=wine_name,
                    location=location,
                    winery=winery,
                    rating=rating,
                    image_url=item.get("image"),
                    image_upload=None,
                    wine_type=wine_type,
                    vintage=vintage,
                )
                print(f"Added wine: {wine_name}") if created else print(f"Wine already exists: {wine_name}")
