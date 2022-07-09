from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users import models as user_models
from rooms import models as room_models
from random import choice, randint

NAME = "lists"


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
        seeder.add_entity(
            List,
            number,
            {
                "user": lambda x: choice(all_users),
            },
        )
        created_lists = seeder.execute()
        created_clean = flatten(list(created_lists.values()))
        all_rooms = room_models.Room.objects.all()
        for pk_of_list in created_clean:
            each_list = List.objects.get(pk=pk_of_list)
            to_add = all_rooms[randint(0, 5) : randint(6, 30)]
            each_list.rooms.add(*to_add)

        if number != 1:
            self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
        else:
            self.stdout.write(self.style.SUCCESS("1 list created!"))
