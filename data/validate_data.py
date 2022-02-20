'''
Script for validating data in DB.
'''
from os import path
from books.models import LinkType, Narration

from data.books import BooksData


def _verify_books_covers_valid(data: BooksData) -> None:
    for book in data.books:
        cover = book.cover_image
        if cover.name == '':
            print(f'Missing cover for book {book.title}')
        else:
            assert path.exists(
                cover.path
            ), f'For book {book.title} did not find image {cover.path}'


def _verify_link_type_icons_exist() -> None:
    for link_type in LinkType.objects.all():
        icon_path = link_type.icon.path
        assert path.exists(
            icon_path
        ), f'For link type {link_type.name} did not find icon {icon_path}'


def _verify_people_photos_valid(data: BooksData) -> None:
    for person in data.people:
        photo = person.photo
        if photo.name == '':
            print(f'Missing photo for person {person.name}')
        else:
            assert path.exists(
                photo.path
            ), f'For person {person.name} did not find image {photo.path}'


def _verify_russian_translations_present(data: BooksData) -> None:
    for person in data.people:
        if person.name_ru == '':
            print(f'Missing name_ru for {person.name}')
    for book in data.books:
        if book.title_ru == '':
            print(f'Missing title_ru for {book.title}')


def run(data: BooksData) -> None:
    'Validates data'
    _verify_books_covers_valid(data)
    _verify_link_type_icons_exist()
    _verify_people_photos_valid(data)
    _verify_russian_translations_present(data)


def cleanup_orphans(data: BooksData) -> None:
    'Removes models which do not belong to any book'
    for person in data.people:
        if person.books_authored.count(
        ) == 0 and person.books_translated.count(
        ) == 0 and person.narrations.count() == 0:
            print(f'Deleting person {person.name} because no books.')
            person.delete()
    for narration in Narration.objects.all():
        if narration.links.count() == 0:
            print(
                f'Deleting narration for book {narration.book.title} because no links.'
            )
            narration.delete()
    for book in data.books:
        if book.narrations.count() == 0:
            print(f'Deleting book {book.title} because no narrations.')
            book.delete()