from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number", 2)
        if number <= 0:
            self.stdout.write(self.style.ERROR("Please enter a valid number."))
            return
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
            },
        )
        seeder.execute()
        if number != 1:
            self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
        else:
            self.stdout.write(self.style.SUCCESS("1 user created!"))
