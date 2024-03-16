from functools import partial
from django.db.models.manager import BaseManager
from manga.models import Comment, Emotion, CommentEmotion
from neural_networks.management.commands.toxic import Processor
from icecream import ic
from django.core.management.base import BaseCommand
import asyncio
import time
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db import transaction
import logging
import concurrent.futures



class CommentProcessor(Processor):

    def __init__(self) -> None:
        super().__init__()
        self.emotions = {}
        for emotion in Emotion.objects.all():
            self.emotions[emotion.name] = emotion
        
    async def add_emotion_to_comment(self, comment:Comment) -> Comment:
        if comment.toxic is not None and await sync_to_async(hasattr)(comment, 'comment_emotion'):
            return comment

        data = await self.text_to_res(comment.comment) # type: ignore
        
        if not comment.toxic is not None:
            comment.toxic = data['toxic']
            await comment.asave()

        if not await sync_to_async(hasattr)(comment, 'comment_emotion'):
            resultset = next(key for key, value in data.items() if key != 'toxic')
            if self.emotions.get(resultset, False):
                emotion = self.emotions.get(resultset)
            else:
                emotion = await Emotion.objects.acreate(name=resultset)
                self.emotions[resultset] = emotion
                
            comment_emotion = CommentEmotion(emotion=emotion, comment=comment, power=data.get(resultset))
            await comment_emotion.asave()

        return comment

    async def add_emotions_to_comments(self, comments:BaseManager[Comment]):
        tasks = []
        async for com in comments:
            tasks.append(asyncio.create_task(self.add_emotion_to_comment(com)))
        return await asyncio.gather(*tasks)



async def main(processor: CommentProcessor):

    chunk_size = 1000
    comment_queryset = Comment.objects.all()
    async def get_comment_queryset_chunk(chunk: int, chunk_size: int) -> BaseManager[Comment]:
        comments = comment_queryset[chunk:chunk + chunk_size]
        return comments
    
    comment_count = 92_547_673

    next_comments_chunk = False
    for chunk in range(2_548_000, comment_count, chunk_size):
        start = time.process_time()
        
        if next_comments_chunk is not False:
            comments_chunk: BaseManager[Comment] = next_comments_chunk
        else:
            comments_chunk: BaseManager[Comment] = await get_comment_queryset_chunk(chunk, chunk_size)
            
        next_comments_chunk = asyncio.create_task(get_comment_queryset_chunk(chunk+chunk_size, chunk_size))
        
        res = await processor.add_emotions_to_comments(comments_chunk)
        
        end = time.process_time()
        t = end-start
        chunk_now = '{:0>9}'.format(chunk)
        chunk_next = '{:0>9}'.format(chunk+chunk_size)
        chunk_now = '_'.join([chunk_now[i:i+3] for i in range(0, len(chunk_now), 3)])
        chunk_next = '_'.join([chunk_next[i:i+3] for i in range(0, len(chunk_next), 3)])
        ic(chunk_now, t)
        logging.debug(f'{chunk_now} - {chunk_next}   process_time = {t:.3}')
        
        next_comments_chunk = await next_comments_chunk

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    def handle(self, *args, **options):
        start = time.process_time()
        comments = asyncio.run(main(CommentProcessor()))
        end = time.process_time()
        ic(end-start)
        breakpoint()