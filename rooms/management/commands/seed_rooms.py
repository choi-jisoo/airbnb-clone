from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users.models import User
from random import choice, randint


class Command(BaseCommand):

    help = "This command creates the rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many rooms do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        if number <= 0:
            self.stdout.write(self.style.ERROR("Please enter a valid number."))
            return

        seeder = Seed.seeder()
        all_users = User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: choice(all_users),
                "room_type": lambda x: choice(room_types),
                "price": lambda x: randint(20, 500),
                "guests": lambda x: randint(1, 8),
                "beds": lambda x: randint(1, 4),
                "bedrooms": lambda x: randint(1, 4),
                "baths": lambda x: randint(1, 4),
            },
        )
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(1, randint(2, 10)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"/room_photos/{randint(1,31)}.webp",
                    room=room,
                )

            for a in amenities:
                magic_number = randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in house_rules:
                magic_number = randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        if number != 1:
            self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
        else:
            self.stdout.write(self.style.SUCCESS("1 room created!"))
