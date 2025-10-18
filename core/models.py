from django.db import models

# Create your models here.
from django.db import models

class Planet(models.Model):
    name = models.CharField(max_length=100)
    climate = models.CharField(max_length=100, blank=True, null=True)
    terrain = models.CharField(max_length=100, blank=True, null=True)
    population = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField()
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=200)
    release_date = models.DateField()
    desc = models.TextField(blank=True, null=True)
    planets = models.ManyToManyField(Planet, related_name="films")

    def __str__(self):
        return self.title


class Character(models.Model):
    name = models.CharField(max_length=100)
    height = models.CharField(max_length=10, blank=True, null=True)
    mass = models.CharField(max_length=10, blank=True, null=True)
    hair_color = models.CharField(max_length=50, blank=True, null=True)
    skin_color = models.CharField(max_length=50, blank=True, null=True)
    eye_color = models.CharField(max_length=50, blank=True, null=True)
    birth_year = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    homeworld = models.ForeignKey(
        Planet, on_delete=models.SET_NULL, null=True, related_name="residents"
    )
    films = models.ManyToManyField(Film, related_name="characters")
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
