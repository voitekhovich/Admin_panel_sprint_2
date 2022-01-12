import uuid
from dataclasses import dataclass, field
from datetime import datetime as dt


@dataclass
class FilmWork:
    title: str
    description: str
    creation_date: dt.date
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: dt.timestamp
    updated_at: dt.timestamp
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def get_list(self):
        return (self.id, self.title, self.description, self.creation_date, self.certificate, self.file_path,
                self.rating, self.type, self.created_at, self.updated_at)


@dataclass
class Genre:
    name: str
    description: str
    created_at: dt.timestamp
    updated_at: dt.timestamp
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def get_list(self):
        return (self.id, self.name, self.description, self.created_at, self.updated_at)


@dataclass
class GenreFilmWork:
    created_at: dt.timestamp
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def get_list(self):
        return (self.id, self.film_work_id, self.genre_id, self.created_at)


@dataclass
class Person:
    full_name: str
    birth_date: dt.date
    created_at: dt.timestamp
    updated_at: dt.timestamp
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def get_list(self):
        return (self.id, self.full_name, self.birth_date, self.created_at, self.updated_at)


@dataclass
class PersonFilmWork:
    role: str
    created_at: dt.timestamp
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def get_list(self):
        return (self.id, self.film_work_id, self.person_id, self.role, self.created_at)
