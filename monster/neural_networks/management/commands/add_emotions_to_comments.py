from manga.models import Comment, Emotion, CommentEmotion
from neural_networks.management.commands.toxic import Processor
from icecream import ic
from django.core.management.base import BaseCommand
import asyncio
import time


class CommentProcessor(Processor):

    def __init__(self) -> None:
        super().__init__()
        self.emotions = {}
        for emotion in Emotion.objects.all():
            self.emotions[emotion.name] = emotion
        
    async def add_emotion_to_comment(self, comment:Comment) -> Comment:
        
        data = await self.text_to_res(comment.comment)
        ic(comment.comment, data)
        if comment.toxic is None:
            comment.toxic = data['toxic']
            await comment.asave()
        
        resultset = [key for key, value in data.items() if key != 'toxic'][0]
        if self.emotions.get(resultset, False):
            emotion = self.emotions.get(resultset)
        else:
            emotion = await Emotion.objects.acreate(name=resultset)
            self.emotions[resultset] = emotion
            
        comment_emotion = CommentEmotion(emotion=emotion, comment=comment, power=data.get(resultset))
        await comment_emotion.asave()
        return comment


def main():
    processor = CommentProcessor()
    comments = [Comment.objects.all()[i] for i in range(0, 10, 1)]
    
    for com in comments:
        asyncio.run(processor.add_emotion_to_comment(com))
    ic(comments)
    ic(len(comments))
    return comments

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    def handle(self, *args, **options):
        start = time.process_time()
        comments = main()
        end = time.process_time()
        ic(end-start)
        breakpoint()