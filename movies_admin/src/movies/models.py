import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = 'content\".\"genre'
        indexes = (
            models.Index(fields=('name',), name='genre_name_idx'),
        )

    def __str__(self) -> str:
        return f'{self.name}'


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        constraints = (
            UniqueConstraint(
                fields=('film_work', 'genre'),
                name='genre_film_work_idx'
            ),
        )

    def __str__(self) -> str:
        return f'{self.film_work} - {self.genre}'


class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_('full_name'), max_length=255)
    birth_date = models.DateField(_('birth_date'), null=True, blank=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        db_table = 'content\".\"person'
        indexes = (
            models.Index(fields=('full_name',), name='person_full_name_idx'),
        )

    def __str__(self) -> str:
        return f'{self.full_name}'


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('актёр')
    WRITER = 'writer', _('сценрист')
    DIRECTOR = 'director', _('режиссёр')


class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(_('role'), max_length=50, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        db_table = 'content\".\"person_film_work'
        constraints = (
            UniqueConstraint(
                fields=('film_work', 'person'),
                name='person_film_work_idx'
            ),
        )

    def __str__(self) -> str:
        return f'{self.person} {self.role} {self.film_work}'


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Filmwork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('sandwich'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)
    creation_date = models.DateField(_('creation date'), null=True, blank=True)
    certificate = models.TextField(_('certificate'), null=True, blank=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', null=True, blank=True)
    rating = models.FloatField(_('rating'), validators=(MinValueValidator(0), MaxValueValidator(10),),
                               null=True, blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = 'content\".\"film_work'
        indexes = (
            models.Index(fields=('creation_date',), name='film_work_creation_date_idx'),
            models.Index(fields=('rating',), name='film_work_rating_idx'),
        )

    def __str__(self) -> str:
        return f'{self.title}'
