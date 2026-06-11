from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=5)
    flag = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return f"{self.flag} {self.name}"


class Game(models.Model):
    PLATFORM_CHOICES = [
        ("mobile", "Mobile Browser"),
        ("pc", "PC Browser"),
        ("both", "Both"),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="games",
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    short_description = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title