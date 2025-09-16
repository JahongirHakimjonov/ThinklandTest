import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.shop.models.category import ProductCategory
from apps.shop.models.product import Product
from apps.users.models.users import User, RoleChoices


class Command(BaseCommand):
    help = "Generate fake products and categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories", type=int, default=5, help="Number of categories to create"
        )
        parser.add_argument(
            "--products", type=int, default=50, help="Number of products to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        user = User.objects.filter(email="jahongirhakimjonov@gmail.com").first()
        if not user:
            User.objects.create_superuser(
                email="jahongirhakimjonov@gmail.com",
                password="1253",
                role=RoleChoices.ADMIN,
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully!"))

            # Create categories
            categories = []
            for _ in range(options["categories"]):
                category = ProductCategory.objects.create(
                    title=fake.word().capitalize(),
                    description=fake.text(max_nb_chars=200),
                )
                categories.append(category)
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category.title}")
                )

            # Create products
            for _ in range(options["products"]):
                product = Product.objects.create(
                    title=fake.sentence(nb_words=3),
                    price=round(random.uniform(10.0, 500.0), 2),
                    description=fake.text(max_nb_chars=500),
                    category=random.choice(categories),
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Created product: {product.title}")
                )

            self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))
        else:
            self.stdout.write(
                self.style.WARNING("Superuser already exists. No data generated.")
            )
