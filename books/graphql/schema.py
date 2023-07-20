import graphene
from graphene import Node
from graphene import ID
from graphene_django import DjangoObjectType, DjangoListField

import books.models as models


class BookType(DjangoObjectType):

    class Meta:
        model = models.Book
        fields = (
            "uuid", "title", "title_ru", "description",
            "description_source", "date", "authors",
            "translators", "slug", "cover_image", "cover_image_source",
            "tag", "promoted", "status", "preview_url", "narrations"
        )


class PersonType(DjangoObjectType):

    class Meta:
        model = models.Person
        fields = (
            "uuid", "name", "name_ru", "description",
            "description_source", "photo", "photo_source",
            "slug", "gender", "date_of_birth", "books_authored",
            "books_translated", "narrations"
        )


class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag
        fields = (
            "name", "slug", "description", "description", "books",
        )


class PublisherType(DjangoObjectType):
    class Meta:
        model = models.Publisher
        fields = (
            "uuid", "name", "slug", "url", "logo", "description", "narrations"
        )


class NarrationType(DjangoObjectType):
    class Meta:
        model = models.Narration
        fields = ("uuid", "narrators", "book", "paid", "language", "duration", "publishers", "links")

class LinkTypeType(DjangoObjectType):

    class Meta:
        model = models.LinkType
        fields = ("name", "caption", "icon", "availability", "weight", "link_type")



class LinkType(DjangoObjectType):

    class Meta:
        model = models.Link
        fields = ("uuid", "url", "url_type", "narration")

class Query(graphene.ObjectType):
    persons = DjangoListField(PersonType, slug=graphene.String(required=False, default_value=""))
    tags = DjangoListField(TagType, slug=graphene.String(required=False, default_value=""))

    def resolve_tags(root, info, slug):
        if slug:
            print(slug)
            data = models.Tag.objects.prefetch_related('books').filter(slug=slug)
            return data
        else:
            data = models.Tag.objects.prefetch_related('books').all()
            return data

    def resolve_persons(root, info, slug):
        if slug:
            print(slug)
            data = models.Person.objects.prefetch_related('books_authored', 'books_translated', 'narrations').filter(slug=slug)
            return data
        else:
            print("22---")
            data = models.Person.objects.prefetch_related('books_authored', 'books_translated', 'narrations').all()
            return data


schema = graphene.Schema(query=Query)
