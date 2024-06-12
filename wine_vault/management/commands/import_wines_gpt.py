import os
import json
import random
import re
import requests
from django.core.management import BaseCommand
from wine_vault.models import Wine, Winery, Location, Rating, WineType
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Import wines from API'
    state_file = "import_state.json"

    def save_state(self, state):
        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"vine_index": 0, "wine_index": 0}

    def handle(self, *args, **kwargs):
        random_preferences_list = [
            "Steak", "Roasted meat", "Pasta with tomato sauce", "Baked chicken", "Lamb",
            "Medium-aged cheeses", "Salmon", "Duck", "Mushrooms", "Grilled chicken",
            "Crab cakes", "Fried salmon", "Caesar salad", "Light fish (e.g., cod)", "Goat cheese",
            "Spicy dishes (e.g., Asian cuisine)", "Sushi", "Pork", "Oysters", "Foie gras",
            "Bruschetta", "Fruits", "Light salads", "Tapas", "Fried fish", "Olives",
            "Blue cheeses", "Chocolate desserts", "Nuts", "Fruit pies", "Baklava",
            "Fruit salads", "Light cakes and pies", "Ice cream"
        ]

        vine_list_api = ["reds", "whites", "sparkling", "rose", "dessert", "port"]
        state = self.load_state()
        max_attempts = 3
        timeout = 10  # seconds

        for vine_index in range(state["vine_index"], len(vine_list_api)):
            num = vine_list_api[vine_index]
            url = f"https://api.sampleapis.com/wines/{num}"
            response = requests.get(url)
            response_json = response.json()
            api_key = os.environ.get("OPENAI_API_KEY")
            client = OpenAI(api_key=api_key)

            # Разбить данные на батчи
            batch_size = 1000  # Измените на размер батча, подходящий для вашего случая
            total_wines = len(response_json)
            for start_index in range(state["wine_index"], total_wines, batch_size):
                end_index = min(start_index + batch_size, total_wines)
                wine_batch = response_json[start_index:end_index]

                # Подготовка батча для отправки в GPT
                wine_prompts = [
                    f"""Tell me about the wine {wine["wine"]}
                    make me a json with out '```json' and add format with the following data and delete all space and /n ,\,\,and other
                    1. name: The wine I specify.
                    2. price : price of the wine in dollars, price analysis must be accurate compared to online stores.
                    3. description: description of the wine in 200 characters.
                    4. preferences: what it goes best with, choose one or more from the list [
                        "Steak", "Roasted meat", "Pasta with tomato sauce", "Baked chicken", "Lamb",
                        "Medium-aged cheeses", "Salmon", "Duck", "Mushrooms", "Grilled chicken",
                        "Crab cakes", "Fried salmon", "Caesar salad", "Light fish (e.g., cod)", "Goat cheese",
                        "Spicy dishes (e.g., Asian cuisine)", "Sushi", "Pork", "Oysters", "Foie gras",
                        "Bruschetta", "Fruits", "Light salads", "Tapas", "Fried fish", "Olives",
                        "Blue cheeses", "Chocolate desserts", "Nuts", "Fruit pies", "Baklava",
                        "Fruit salads", "Light cakes and pies", "Ice cream"
                    ]
                    5. year: year of release""" for wine in wine_batch
                ]
                full_prompt = "\n".join(wine_prompts)

                attempts = 0
                while attempts < max_attempts:
                    try:
                        completion = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "Provide output in valid JSON format."},
                                {"role": "user", "content": full_prompt}
                            ],
                            timeout=timeout
                        )
                        data = completion.choices[0].message.content
                        responses = data.split("}")  # Разделяем ответы на отдельные JSON объекты
                        responses = [r + "}" for r in responses if r.strip()]

                        for response in responses:
                            try:
                                data_js = json.loads(response)
                            except json.JSONDecodeError:
                                continue

                            wine_name = data_js.get("wine", {}).get("name", "")
                            try:
                                print(f"Response from OpenAI for wine {wine_name}")  # Log response
                            except KeyError:
                                print(f"Response from OpenAI for bad but add")

                            wine_type, _ = WineType.objects.get_or_create(type=num[:-1] if num.endswith('s') else num)

                            rating_data = wine.get("rating", {})
                            winery, _ = Winery.objects.get_or_create(name=wine.get("winery"))
                            location = wine.get("location")
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

                            try:
                                year_of_release = data_js["wine"]["year"]
                            except KeyError:
                                year_of_release = random.randint(1990, 2024)

                            try:
                                description = data_js["wine"]["description"]
                            except KeyError:
                                description = "-"

                            try:
                                preferences = data_js["wine"]["preferences"]
                            except KeyError:
                                preferences = random.sample(random_preferences_list, 3)

                            try:
                                price = data_js["wine"]["price"]
                            except KeyError:
                                price = random.randint(30, 2000)

                            wine, created = Wine.objects.get_or_create(
                                name=wine_name,
                                location=location,
                                winery=winery,
                                rating=rating,
                                image_url=wine.get("image"),
                                image_upload=None,
                                wine_type=wine_type,
                                year_of_release=year_of_release,
                                price=price,
                                description=description,
                                preferences=preferences
                            )

                            print(f"Added wine: {wine_name}") if created else print(f"Wine already exists: {wine_name}")

                        break  # Successfully received response, exit the loop
                    except (json.JSONDecodeError, requests.exceptions.RequestException, KeyError) as e:
                        attempts += 1
                        if attempts >= max_attempts:
                            print(f"Failed to get a valid response for batch starting at index {start_index} after {max_attempts} attempts")
                            continue  # Skip this batch and move on to the next

                # Update state after each batch
                state["vine_index"] = vine_index
                state["wine_index"] = end_index
                self.save_state(state)

        # Reset state after completing all categories
        state["wine_index"] = 0
        state["vine_index"] = 0
        self.save_state(state)
