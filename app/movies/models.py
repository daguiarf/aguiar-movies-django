from django.db import models


class ContentReference(models.Model):

    MEDIA_MOVIE = "movie"
    MEDIA_TV = "tv"
    MEDIA_PERSON = "person"

    MEDIA_TYPE_CHOICES = [
        (MEDIA_MOVIE, "Movie"),
        (MEDIA_TV, "TV Show"),
        (MEDIA_PERSON, "Person"),
    ]

    tmdb_id = models.IntegerField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    title = models.CharField(max_length=500)
    poster_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ("tmdb_id", "media_type")
        verbose_name = "Content Reference"
        verbose_name_plural = "Content References"

    def __str__(self):
        return f"{self.title} [{self.media_type}] (tmdb:{self.tmdb_id})"
