import json
import logging
from typing import Any
from django.db import IntegrityError
from manga.models import Manga, AgeRestriction, MangaType, Moderated, Team, Tag, Genre, Publisher, MangaStatus, ScanlateStatus, People


class MangaToDb:
    def __init__(self, manga_json:dict[Any, Any]) -> None:
        self.manga_json: dict = manga_json.get('data', {})

    @property
    def href(self):
        return f'https://test-front.mangalib.me/ru/manga/{self.manga_json.get("slug")}'
    
    def show(self):
        print(json.dumps(self.manga_json, indent=4, ensure_ascii=False))

    async def create_model(self):
        manga = Manga.objects.filter(id=self.manga_json.get('id'))
        if await manga.aexists():
            return await manga.afirst(), await manga.aexists()
        age_restriction, is_create = await AgeRestriction.objects.aget_or_create(**self.manga_json.get('ageRestriction', {}))
        #print(f'{age_restriction=}')
        type, is_create = await MangaType.objects.aget_or_create(**self.manga_json.get('type', {}))
        #print(f'{type=}')
        moderated, is_create = await Moderated.objects.aget_or_create(**self.manga_json.get('moderated', {}))
        #print(f'{moderated=}')
        status, is_create = await MangaStatus.objects.aget_or_create(**self.manga_json.get('status', {}))
        #print(f'{status=}')
        scanlate_status, is_create = await ScanlateStatus.objects.aget_or_create(**self.manga_json.get('scanlateStatus', {}))
        #print(f'{scanlate_status=}')
        teams = []
        for team in self.manga_json.get('teams', []):
            team_json = team
            try:
                team, is_create = await Team.objects.aget_or_create(
                                                                    id=team.get('id'), 
                                                                    slug=team.get('slug'), 
                                                                    slug_url=team.get('slug_url'), 
                                                                    name=team.get('name'), 
                                                                    cover=team.get('cover'), 
                                                                    details=team.get('details')
                                                                    )
            except IntegrityError as e:
                logging.error(f'{team_json.get("name")=}\t{team_json.get("id")=}\t{e=}')
                team = await Team.objects.aget(id=team_json.get('id'))
            finally:
                teams.append(team)
        #print(f'{teams=}')
        genres = []
        for genre in self.manga_json.get('genres', []):
            genre_json = genre
            obj = None
            try:
                genre, is_create = await Genre.objects.aget_or_create(**genre)
            except IntegrityError as e:
                logging.error(f'{genre_json.get("name")=}\t{genre_json.get("id")=}\t{e=}')
                genre = await Genre.objects.aget(id=genre_json.get('id'))
            finally:
                genres.append(genre)
        #print(f'{genres=}')
        tags = []
        for tag in self.manga_json.get('tags', []):
            json_data = tag
            obj = None
            try:
                obj, is_create = await Tag.objects.aget_or_create(**tag)
            except IntegrityError as e:
                logging.error(f'{json_data.get("name")=}\t{json_data.get("id")=}\t{e=}')
                obj = await Tag.objects.aget(id=json_data.get('id'))
            finally:
                tags.append(obj)
        #print(f'{tags=}')
        publishers = []
        for publisher in self.manga_json.get('publisher', []):
            json_data = publisher
            obj = None
            try:
                obj, is_create = await Publisher.objects.aget_or_create(**publisher)
            except IntegrityError as e:
                logging.error(f'{json_data.get("name")=}\t{json_data.get("id")=}\t{e=}')
                obj = await Publisher.objects.aget(id=json_data.get('id'))
            finally:
                publishers.append(obj)

        artists = []
        for artist in self.manga_json.get('artists', []):
            json_data = artist
            obj = None
            try:
                obj, is_create = await People.objects.aget_or_create(**artist)
            except IntegrityError as e:
                logging.error(f'{json_data.get("name")=}\t{json_data.get("id")=}\t{e=}')
                obj = await People.objects.aget(id=json_data.get('id'))
            finally:
                artists.append(obj)
        #print(f'{artists=}')
        authors = []
        for author in self.manga_json.get('authors', []):
            json_data = author
            obj = None
            try:
                obj, is_create = await People.objects.aget_or_create(**author)
            except IntegrityError as e:
                logging.error(f'{json_data.get("name")=}\t{json_data.get("id")=}\t{e=}')
                obj = await People.objects.aget(id=json_data.get('id'))
            finally:
                authors.append(obj)
        #print(f'{authors=}')
        #print(f'{self.manga_json.get("id")=}')
        manga, is_create = await Manga.objects.aget_or_create(
            id = self.manga_json.get('id'),
            name = self.manga_json.get('name'),
            rus_name = self.manga_json.get('rus_name'),
            eng_name = self.manga_json.get('eng_name'),
            other_names = self.manga_json.get('otherNames'),
            slug = self.manga_json.get('slug'),
            slug_url = self.manga_json.get('slug_url'),
            cover = self.manga_json.get('cover'),
            background = self.manga_json.get('background'),
            site = self.manga_json.get('site'),
            summary = self.manga_json.get('summary'),
            close_view = self.manga_json.get('close_view'),
            release_date = self.manga_json.get('releaseDate') if self.manga_json.get('releaseDate') != '' else 0,
            views = self.manga_json.get('views'),
            rating = self.manga_json.get('rating'),
            is_licensed = self.manga_json.get('is_licensed'),
            metadata = self.manga_json.get('metadata'),
            model = self.manga_json.get('model'),
            items_count = self.manga_json.get('items_count'),
            format = self.manga_json.get('format'),
            release_date_string = self.manga_json.get('releaseDateString'),
            status = status,
            scanlate_status = scanlate_status,
            age_restriction = age_restriction,
            type = type,
            moderated = moderated,
        )   
        await manga.artists.aadd(*artists)
        await manga.authors.aadd(*authors)
        await manga.genres.aadd(*genres)
        await manga.teams.aadd(*teams)
        await manga.tags.aadd(*tags)
        await manga.publishers.aadd(*publishers)
        await manga.asave()
        #print(f'Готво - {manga}')
        return manga, is_create

class ChaptersToDb:
    def __init__(self, manga:Manga) -> None:
        self.manga:Manga = manga
    
    def __show(self):
        print(json.dumps(None, indent=4, ensure_ascii=False))

























