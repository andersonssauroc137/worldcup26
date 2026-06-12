import uuid
from django.db import models


class Player(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nickname = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nickname"]

    def __str__(self):
        return self.nickname