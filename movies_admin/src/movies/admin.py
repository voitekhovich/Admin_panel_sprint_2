from django.contrib import admin

from .models import Filmwork, FilmworkGenre, Genre, Person, PersonFilmWork


class FilmworkGenreInline(admin.TabularInline):
    model = FilmworkGenre
    extra = 1


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating', 'created_at', 'updated_at',)
    list_filter = ('type',)
    search_fields = ('title', 'description', )
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating',
    )
    inlines = (FilmworkGenreInline, PersonFilmWorkInline,)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at',)
    list_filter = ('name',)
    search_fields = ('name', )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'created_at', 'updated_at',)
    list_filter = ('birth_date',)
    search_fields = ('full_name', )
