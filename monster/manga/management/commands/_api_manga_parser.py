import json
import logging
from typing import Any
from django.db import IntegrityError
from manga.models import Chapter, MangaUser, Manga, AgeRestriction, MangaType, Moderated, Team, Tag, Genre, Publisher, MangaStatus, ScanlateStatus, People, Branch
import asyncio

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
        logging.debug(f'{self.manga_json.get("slug")=}')
        age_restriction, is_create = await AgeRestriction.objects.aget_or_create(**self.manga_json.get('ageRestriction', {}))
        logging.debug(f'{age_restriction=}')
        type, is_create = await MangaType.objects.aget_or_create(**self.manga_json.get('type', {}))
        logging.debug(f'{type=}')
        moderated, is_create = await Moderated.objects.aget_or_create(**self.manga_json.get('moderated', {}))
        logging.debug(f'{moderated=}')
        status, is_create = await MangaStatus.objects.aget_or_create(**self.manga_json.get('status', {}))
        logging.debug(f'{status=}')
        scanlate_status, is_create = await ScanlateStatus.objects.aget_or_create(**self.manga_json.get('scanlateStatus', {}))
        logging.debug(f'{scanlate_status=}')
        teams = []
        for team in self.manga_json.get('teams', []):
            data_json = team
            obj, is_create = await Team.objects.aget_or_create(id=team.get('id'), defaults=data_json)
            teams.append(obj)
        logging.debug(f'{teams=}')
        genres = []
        for genre in self.manga_json.get('genres', []):
            data_json = genre
            obj, is_create = await Genre.objects.aget_or_create(id=genre.get('id'), defaults=data_json)
            genres.append(obj)
        logging.debug(f'{genres=}')
        tags = []
        for tag in self.manga_json.get('tags', []):
            data_json = tag
            obj, is_create = await Tag.objects.aget_or_create(id=tag.get('id'), defaults=data_json)
            tags.append(obj)
        logging.debug(f'{tags=}')
        publishers = []
        for publisher in self.manga_json.get('publisher', []):
            data_json = publisher
            obj, is_create = await Publisher.objects.aget_or_create(id=publisher.get('id'), defaults=data_json)
            publishers.append(obj)
        logging.debug(f'{publishers=}')
        artists = []
        for artist in self.manga_json.get('artists', []):
            data_json = artist
            obj, is_create = await People.objects.aget_or_create(id=artist.get('id'), slug_url=artist.get('slug_url'), defaults=data_json)
            artists.append(obj)            
        logging.debug(f'{artists=}')
        authors = []
        for author in self.manga_json.get('authors', []):
            data_json = author
            obj, is_create = await People.objects.aget_or_create(id=author.get('id'), slug_url=author.get('slug_url'), defaults=data_json)
            authors.append(obj)
        logging.debug(f'{authors=}')
        manga, is_create = await Manga.objects.aupdate_or_create(
            id = self.manga_json.get('id'),
            defaults={
            'name':self.manga_json.get('name'),
            'rus_name': self.manga_json.get('rus_name'),
            'eng_name': self.manga_json.get('eng_name'),
            'other_names': self.manga_json.get('otherNames'),
            'slug': self.manga_json.get('slug'),
            'slug_url': self.manga_json.get('slug_url'),
            'cover': self.manga_json.get('cover'),
            'background': self.manga_json.get('background'),
            'site': self.manga_json.get('site'),
            'summary': self.manga_json.get('summary'),
            'close_view': self.manga_json.get('close_view'),
            'release_date': self.manga_json.get('releaseDate') if self.manga_json.get('releaseDate') != '' else 0,
            'views': self.manga_json.get('views'),
            'rating': self.manga_json.get('rating'),
            'is_licensed': self.manga_json.get('is_licensed'),
            'metadata': self.manga_json.get('metadata'),
            'model': self.manga_json.get('model'),
            'items_count': self.manga_json.get('items_count'),
            'format': self.manga_json.get('format'),
            'release_date_string': self.manga_json.get('releaseDateString'),
            'status': status,
            'scanlate_status': scanlate_status,
            'age_restriction': age_restriction,
            'type': type,
            'moderated': moderated,
            }
        )   
        logging.debug(f'Первичное создание {manga}')
        await manga.artists.aadd(*artists)
        await manga.authors.aadd(*authors)
        await manga.genres.aadd(*genres)
        await manga.teams.aadd(*teams)
        await manga.tags.aadd(*tags)
        await manga.publishers.aadd(*publishers)
        await manga.asave()
        logging.debug(f'Готво - {manga}')
        return manga, is_create

class BranchToDB:
    def __init__(self, branchs_json:dict[Any, Any]) -> None:
        self.branchs_json: dict = branchs_json

    def show(self):
        print(json.dumps(self.branchs_json, indent=4, ensure_ascii=False))
        
    async def create_model(self):
        teams = []
        for team in self.branchs_json.get('teams', []):
            team, is_create = await Team.objects.aget_or_create(id=team.get('id'), defaults=team)
            teams.append(team)
        logging.debug(f'branch {teams=}')
        user, is_create = await MangaUser.objects.aget_or_create(id=self.branchs_json.get('user', {}).get('id'), defaults=self.branchs_json.get('user'))
        logging.debug(f'branch {user=}')
        data = self.branchs_json
        branch, is_create = await Branch.objects.aget_or_create(id=data.get('id'), defaults={'branch_id':data.get('branch_id'), 'created_at':data.get('created_at'), 'user':user})
        logging.debug(f'{branch=}')
        return branch
    
class ChaptersToDb:
    def __init__(self, chapters_json:dict[Any, Any], manga:Manga) -> None:
        self.chapters_json: dict = chapters_json.get('data', [])
        self.manga = manga
    
    def show(self):
        print(json.dumps(self.chapters_json, indent=4, ensure_ascii=False))
        return json.dumps(self.chapters_json, indent=4, ensure_ascii=False)

    async def create_model(self, data:dict[Any, Any]):
        branches = []
        for branche in data.get('branches', []):
            b = BranchToDB(branche)
            branche = await b.create_model()
            assert isinstance(branche, Branch)
            branches.append(branche)
        logging.debug(f'chapter {branches=}')
        del data['branches']
        data['manga_id'] = self.manga
        chapter, is_create = await Chapter.objects.aget_or_create(id=data.get('id'), defaults=data)
        logging.debug(f'{chapter=}')
        return chapter
    
    async def create_models(self):
        tasks = []
        for chapter in self.chapters_json:
            task = asyncio.create_task(self.create_model(chapter))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        logging.debug(f'ChaptersToDb create_models {results=}')
        return results























