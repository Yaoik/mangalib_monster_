from transformers import BertTokenizer, BertForSequenceClassification
import asyncio
from django.core.management.base import BaseCommand, CommandError
import time
from icecream import ic
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import asyncio

class ToxicityAnalyzer:
    tokenizer = BertTokenizer.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier')
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    model = BertForSequenceClassification.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier').to(device) # type: ignore 
        
    def __init__(self) -> None:
        pass

    def text_to_prob(self, text:str):
        # prepare the input
        batch = self.tokenizer.encode(text, return_tensors='pt').to(self.device) # type: ignore # type: ignore # type: ignore # type: ignore # type: ignore

        # inference
        with torch.no_grad():
            outputs = self.model(batch) # type: ignore
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # interpreting the output
        toxicity_prob = round(probs[0][1].item(), 3)
        neutral_prob = round(probs[0][0].item(), 3)

        res = {'neutral': neutral_prob, 'toxic': toxicity_prob}
        #breakpoint()
        return res

def show(neural_network, texts:list[str]):
    start = time.perf_counter()
    ic()
    ic(neural_network.text_to_prob('Данный фрагмент текста не содержит абсолютно никаких эмоций'))
    ic(neural_network.text_to_prob('Ты мне нравишься. Я тебя люблю'))
    ic(neural_network.text_to_prob('Минато, ты переступаешь черту...'))
    ic(neural_network.text_to_prob('Пхех приманочка XD'))
    ic(neural_network.text_to_prob('Спасибо.'))
    ic(neural_network.text_to_prob('Не пфыкай мне тут! 😠'))
    ic(neural_network.text_to_prob('Этот прицел просто имба'))
    ic(neural_network.text_to_prob('добро пожаловать в мир истинных мужчин'))
    ic(neural_network.text_to_prob('Ахахэахах<br>Это же гениально, берём уроки манипулировния сознанием человека от Джинни!'))
    ic()
    end = time.perf_counter()
    ic(end-start)

class EmotionAnalyzer:
    tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny2-cedr-emotion-detection')
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    model = BertForSequenceClassification.from_pretrained('cointegrated/rubert-tiny2-cedr-emotion-detection').to(device) # type: ignore 
    #if torch.cuda.is_available():
    #    model.to('cuda')
        
    def __init__(self) -> None:
        pass
    
    def text_to_prob(self, text:str):
        # prepare the input
        batch = self.tokenizer.encode(text, return_tensors='pt').to(self.device) # type: ignore # type: ignore # type: ignore # type: ignore # type: ignore

        # inference
        with torch.no_grad():
            outputs = self.model(batch) # type: ignore
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # interpreting the output
        no_emotion_prob = round(probs[0][0].item(), 3)
        sadness_prob = round(probs[0][1].item(), 3)
        surprise_prob = round(probs[0][2].item(), 3)
        anger_prob = round(probs[0][3].item(), 3)
        fear_prob = round(probs[0][4].item(), 3)
        joy_prob = round(probs[0][5].item(), 3)
        
        res = {'no_emotion':no_emotion_prob, 'sadness':sadness_prob, 'surprise':surprise_prob, 'anger':anger_prob, 'fear':fear_prob, 'joy':joy_prob}
        
        return res

class SmallToxicityAnalyzer:
    tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny-toxicity') # 11.8M 
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    device = 'cuda'
    model = BertForSequenceClassification.from_pretrained('cointegrated/rubert-tiny-toxicity').to(device)  # type: ignore 
    #if torch.cuda.is_available():
    #    model.to('cuda')
        
    def __init__(self) -> None:
        pass

    async def text_to_prob(self, text:str):
        
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(self.device) # type: ignore 
            proba = torch.sigmoid(self.model(**inputs).logits).cpu().numpy()[0]

        res = {'toxic': round(1 - proba.T[0] * (1 - proba.T[-1]), 3)}
        #breakpoint()
        return res

class SmallEmotionAnalyzer:
    # seara/rubert-tiny2-ru-go-emotions
    tokenizer = AutoTokenizer.from_pretrained('seara/rubert-tiny2-ru-go-emotions')
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    model = AutoModelForSequenceClassification.from_pretrained('seara/rubert-tiny2-ru-go-emotions')
    
    def __init__(self) -> None:
        self.types = {
            'admiration': 'восхищение',
            'amusement': 'веселье',
            'anger': 'злость',
            'annoyance': 'раздражение',
            'approval': 'одобрение',
            'caring': 'забота',
            'confusion': 'непонимание',
            'curiosity': 'любопытство',
            'desire': 'желание',
            'disappointment': 'разочарование',
            'disapproval': 'неодобрение',
            'disgust': 'отвращение',
            'embarrassment': 'смущение',
            'excitement': 'возбуждение',
            'fear': 'страх',
            'gratitude': 'признательность',
            'grief': 'горе',
            'joy': 'радость',
            'love': 'любовь',
            'nervousness': 'нервозность',
            'optimism': 'оптимизм',
            'pride': 'гордость',
            'realization': 'осознание',
            'relief': 'облегчение',
            'remorse': 'раскаяние',
            'sadness': 'грусть',
            'surprise': 'удивление',
            'neutral': 'нейтральность',
        }

    def text_to_prob(self, text:str):
        # prepare the input
        batch = self.tokenizer.encode(text, return_tensors='pt') # type: ignore # type: ignore # type: ignore # type: ignore # type: ignore

        # inference
        with torch.no_grad():
            outputs = self.model(batch) # type: ignore
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
        
        res = {}
        
        for t, prob in zip(self.types.values(), probs):
            res[t] = round(prob.item(), 3)
        
        return res

class EmotionAnalizerNew:
    LABELS = ['neutral', 'happiness', 'sadness', 'enthusiasm', 'fear', 'anger', 'disgust']
    tokenizer = AutoTokenizer.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection') # 29.2M 
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    device = 'cuda'
    model = BertForSequenceClassification.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection').to(device)  # type: ignore 
        
    def __init__(self) -> None:
        pass

    async def text_to_prob(self, text:str):
        
        with torch.no_grad():
            inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt').to(self.device)
            outputs = self.model(**inputs)
            
        predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
        max_index = predicted.argmax().item()
        max_emotion = self.LABELS[max_index] # type: ignore 
        max_prob = predicted[0, max_index].item()  # type: ignore 
        #breakpoint()
        return {max_emotion: round(max_prob, 3)}


class Processor:
    def __init__(self) -> None:
        self.t = SmallToxicityAnalyzer()
        self.e = EmotionAnalizerNew()

    async def text_to_res(self, text:str):
        res = {}
        res_e = asyncio.create_task(self.e.text_to_prob(text))
        res_t = asyncio.create_task(self.t.text_to_prob(text))
        res.update(await res_e)
        res.update(await res_t)
        return res
        
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    def handle(self, *args, **options):
        texts = [
            'Данный фрагмент текста не содержит абсолютно никаких эмоций', 
            'Ты мне нравишься. Я тебя люблю', 
            'Минато, ты переступаешь черту...', 
            'Пхех приманочка XD', 
            'Спасибо.', 
            'Не пфыкай мне тут! 😠',
            'Этот прицел просто имба',
            'добро пожаловать в мир истинных мужчин'
            'Ахахэахах<br>Это же гениально, берём уроки манипулировния сознанием человека от Джинни!'
            ] * 100
        p = Processor()
        start = time.perf_counter()
        for text in texts:
            print()
            ic(text, asyncio.run(p.text_to_res(text)))
            print()
        end = time.perf_counter()
        ic(end-start)
        ic((end-start)/len(texts)*100)
        breakpoint()
        
        
        
        
        





        