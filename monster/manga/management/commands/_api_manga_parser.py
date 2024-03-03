import copy
import json
import logging
import time
from typing import Any
from manga.models import Comment, Page, Chapter, MangaUser, Manga, AgeRestriction, MangaType, Moderated, Team, Tag, Genre, Publisher, MangaStatus, ScanlateStatus, People, Branch
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
    
    async def create_models(self) -> list[Chapter]:
        tasks = []
        for chapter in self.chapters_json:
            task = asyncio.create_task(self.create_model(chapter))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        logging.debug(f'ChaptersToDb create_models {results=}')
        return results

class PagesToDB:
    def __init__(self, pages_json:list[dict[Any, Any]], chapter:Chapter) -> None:
        self.pages_json = pages_json
        self.chapter = chapter

    def show(self):
        print(json.dumps(self.pages_json, indent=4, ensure_ascii=False))
        
    async def create_models(self):
        logging.debug(f'create_models start')
        pages_json = self.pages_json.copy()
        for page in pages_json:
            page['chapter_id'] = self.chapter
        for page in pages_json:
            logging.debug(f'create_models {page.get("created_at")=}')
            logging.debug(f'create_models {page.get("updated_at")=}')
            if page.get("updated_at", '').startswith('-'):
                page['updated_at'] = None
            try:
                float(page['ratio'])
            except ValueError:
                page['ratio'] = 0.0
                
        pages_data = [Page(**page) for page in self.pages_json]
        logging.debug(f'create_models {pages_data=}')
        pages = await Page.objects.abulk_create(pages_data, ignore_conflicts=True)
        logging.debug(f'create_models {pages=}')
        logging.debug(f'create_models {len(pages)=}')
        logging.debug(f'create_models end')
        return pages

class CommentToDB:
    def __init__(self, pages_json:dict[str, Any], page:Page) -> None:
        assert isinstance(page, Page)
        assert isinstance(pages_json, dict)
        self.pages_json = pages_json
        self.page = page
        self.last_count = None

    def show(self):
        r = json.dumps(self.pages_json, indent=4, ensure_ascii=False)
        print(r)
        with open('C:\\Users\\Shamrock\\Desktop\\mangalib_monster обход блокировки ботов\\monster\\manga\\management\\commands\\res.json', 'w+', encoding='utf-8') as f:
            f.write(r)
    
    async def json_to_model(self, root:dict):    
        data = copy.deepcopy(root)
        del data['votes']
        user, is_create = await MangaUser.objects.aget_or_create(id=root.get('user', {}).get('id'), defaults=root.get('user', {}))
        data['user'] = user
            
        data['votes_up'] = root.get('votes', {}).get('up', 0)
        data['votes_down'] = root.get('votes', {}).get('down', 0)
            
        data['post_page'] = self.page
        
        return Comment(**data)
    
    async def recursion_create(self, comments_exists: dict[int, Comment], comments:list):
        comments_obj = []
        i = 0
        while i<len(comments):
            com = comments[i]
            if comments_exists.get(com.get('parent_comment', 0), False):
                data = copy.deepcopy(com)
                data['parent_comment'] = comments_exists.get(data.get('parent_comment'))
                data['root_id'] = comments_exists.get(data.get('root_id'))
                c = await self.json_to_model(data)
                comments_obj.append(c)
                del comments[i]
            else:
                i+=1
                
        comments_obj = await Comment.objects.abulk_create(comments_obj, ignore_conflicts=True)
        new: dict[int, Comment] = {i.id:i for i in comments_obj}
        comments_exists.update(new)
        if len(comments)>0 and not len(comments) == self.last_count:
            self.last_count = len(comments)
            return await self.recursion_create(comments_exists, comments)
        val = tuple(comments_exists.values())
        return val
    
    async def create_models(self):
        roots_list = []
        for root in self.pages_json.get('root', []):
            root = await self.json_to_model(root)
            roots_list.append(root)
        try:
            del self.pages_json['root']
        except KeyError as e:
            logging.error(f'ERROR {self.pages_json=}')
            raise KeyError(e)
        
        roots = await Comment.objects.abulk_create(roots_list, ignore_conflicts=True)
        comments_exists = {i.id:i for i in roots}
        extend = await self.recursion_create(comments_exists, self.pages_json.get('replies', {}))
        return tuple(extend)



class OldCommentToDB:
        
    async def _json_to_model(self, comment:dict, page:Page):    
        data = {}
        data['id'] = comment.get('id')
        if comment.get('root_id'):
            data['root_id'] = await Comment.objects.aget(id=comment.get('root_id')) 
        else:
            data['root_id'] = None
        if comment.get('parent_comment'):
            data['parent_comment'] = await Comment.objects.aget(id=comment.get('parent_comment')) 
        else:
            data['parent_comment'] = None
        data['comment_level'] = comment.get('comment_level')
        data['post_page'] = page
        data['votes_up'] = comment.get('votes_up')
        data['votes_down'] = comment.get('votes_down')
        data['deleted'] = comment.get('deleted')
        data['comment'] = comment.get('comment')
        data['created_at'] = comment.get('created_at', '').replace(' ', 'T') + '.000000Z'
        data['updated_at'] = comment.get('updated_at', '').replace(' ', 'T') + '.000000Z'
        user = comment.get('user') 
        assert isinstance(user, dict)
        data['user'], is_created = await MangaUser.objects.aget_or_create(id=user.get('id'), defaults=user)
        return Comment(**data)
    
    async def create_models(self, data:dict[Page, dict[Any, list[dict]]]):
        comments_list = []
        for page, comments_data in data.items():
            for comment in comments_data.get('comments', []):
                comment = await self._json_to_model(comment, page)
                comments_list.append(comment)
            del comments_data['comments']
        #start = time.time()
        comments = await Comment.objects.abulk_create(comments_list, ignore_conflicts=True)
        #logging.info(f'comments time = {time.time()-start}s')
        
        comments_exists = {i.id:i for i in comments}
        #logging.info(f'create_models {len(comments)=}')
        for page, comments_data in data.items():
            replies = comments_data.get('replies', [])
            while len(replies)>0:
                l = len(replies)
                #logging.info(f'{replies=}')
                create = []
                i = 0
                while len(replies)>i:
                    replie = replies[i]
                    if comments_exists.get(replie.get('parent_comment', 0), False):
                        #logging.info(f'{replie=}')
                        create.append(await self._json_to_model(replie, page))
                        replies.pop(i)
                    else:
                        i+=1
                #start = time.time()
                new_comments = await Comment.objects.abulk_create(create, ignore_conflicts=True)
                #logging.info(f'new_comments time = {time.time()-start}s')
                for com in new_comments:
                    comments_exists[com.id] = com
                comments.extend(new_comments)
                if len(replies) == l:
                    break
        if len(comments)>0:
            logging.info(f'+{len(comments)} comments')
        return set(comments)
