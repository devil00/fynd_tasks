from django.db import models


class Director(models.Model):
    """
    Director model.
    """
    name = models.CharField(max_length=150)

    def __str__(self):
        return "Director: {}".format(self.name)


class Genre(models.Model):
    """
    Genre model.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return "Genere: {}".format(self.name)


class Movie(models.Model):
    """
    A django model responsible for storing a movie.
    The structure of this model comprises many to one relationship with Director
    model and many to many relationship with Genre model.
    """
    name = models.CharField(max_length=150)
    imdb_score = models.DecimalField(max_digits=5, decimal_places=2)
    popularity = models.DecimalField(max_digits=5, decimal_places=2)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return "Movie: {} has imdb score={}".format(self.name, self.score)
