from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Match(models.Model):
    swiper = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="swiped")
    swiped = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="swiper")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['swiper', 'swiped'],
                name='unique_match',
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_match",
                check=~models.Q(swiped=models.F("swiper"))
            ),
        ]
