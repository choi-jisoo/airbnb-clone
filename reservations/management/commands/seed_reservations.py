from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations.models import Reservation
from users import models as user_models
from rooms import models as room_models
from random import choice, randint

NAME = "reservations"


class Command(BaseCommand):
    help = f"This command creates the {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        if number <= 0:
            self.stdout.write(self.style.ERROR("Please enter a valid number."))
            return

        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        seeder.add_entity(
            Reservation,
            number,
            {
                "guest": lambda x: choice(all_users),
                "room": lambda x: choice(all_rooms),
                "check_in": lambda x: datetime.now() - timedelta(days=randint(0, 5)),
                "check_out": lambda x: datetime.now() + timedelta(days=randint(1, 5)),
            },
        )
        seeder.execute()

        if number != 1:
            self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
        else:
            self.stdout.write(self.style.SUCCESS("1 reservation created!"))
