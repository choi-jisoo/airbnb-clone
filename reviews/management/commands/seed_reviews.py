from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from users import models as user_models
from rooms import models as room_models
from random import randint, choice


class Command(BaseCommand):
    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help="How many reviews do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        if number <= 0:
            self.stdout.write(self.style.ERROR("Please enter a valid number."))
            return
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Review,
            number,
            {
                "accuracy": lambda x: randint(0, 5),
                "communication": lambda x: randint(0, 5),
                "cleanliness": lambda x: randint(0, 5),
                "location": lambda x: randint(0, 5),
                "check_in": lambda x: randint(0, 5),
                "value": lambda x: randint(0, 5),
                "user": lambda x: choice(all_users),
                "room": lambda x: choice(all_rooms),
            },
        )
        seeder.execute()

        if number != 1:
            self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))
        else:
            self.stdout.write(self.style.SUCCESS("1 review created!"))
