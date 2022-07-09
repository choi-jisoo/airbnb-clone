from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        if self.status == self.STATUS_CONFIRMED:
            return now >= self.check_in and now < self.check_out
        else:
            return False

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        if self.status == self.STATUS_CANCELED:
            return True
        else:
            return now >= self.check_out

    is_finished.boolean = True


def get_now_date():
    now = timezone.now().date()
    return now
