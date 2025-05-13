from transformers import pipeline
import pandas as pd

class ModelPipeline:
    def __init__(self):
        self.zero_shot = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        self.absa = pipeline(
            "text-classification",
            model="yangheng/deberta-v3-base-absa-v1.1"
        )
        self.sentiment = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-sentiment"
        )
        self.emotion = pipeline(
            "text-classification",
            model="SamLowe/roberta-base-go_emotions"
        )
        self.aspect_candidates = [
            "driver", "app", "price", "payment",
            "customer support", "service",
            "waiting time", "safety", "accuracy"
        ]
        
        self.churn_keywords = [
            "cancel", "switch", "stop", "uninstall",
            "delete", "quit", "won't use", "avoid"
        ]
        
        self.sentiment_map = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral',
            'LABEL_2': 'positive'
        }

    def detect_aspects(self, text, threshold=0.85):
        """Detect relevant aspects using zero-shot classification"""
        result = self.zero_shot(text, self.aspect_candidates, multi_label=True)
        return [
            aspect for aspect, score 
            in zip(result["labels"], result["scores"]) 
            if score > threshold
        ]

    def get_aspect_sentiment(self, text, aspect):
        """Get sentiment for a specific aspect using ABSA"""
        try:
            result = self.absa(f"{text} [ASP] {aspect}")[0]
            return result["label"].lower() 
        except:
            return "neutral"  

    def build(self, text):
        aspects = self.detect_aspects(text)
        aspect_sentiments = {
            aspect: self.get_aspect_sentiment(text, aspect) 
            for aspect in aspects
        }
        
        sentiment_result = self.sentiment(text)[0]
        overall_sentiment = self.sentiment_map.get(
            sentiment_result["label"], 
            sentiment_result["label"]
        )
        
        emotion_result = self.emotion(text)[0]
        EMOTION_MAPPING = {
            'disappointment': 'disappointment',
            'annoyance': 'annoyance',
            'neutral': 'neutral',
            'curiosity': 'curiosity',
            'anger': 'anger',
            'gratitude': 'gratitude',
            'confusion': 'confusion',
            # Negative spectrum
            'disapproval': 'disapproval',
            'disgust': 'anger',
            'fear': 'anger',
            'grief': 'disappointment',
            'sadness': 'disappointment',
            'remorse': 'annoyance',
            'embarrassment': 'annoyance',
            'joy': 'gratitude',
            'love': 'love',
            'admiration': 'gratitude',
            'amusement': 'gratitude',
            'approval': 'approval',
            'caring': 'gratitude',
            'optimism': 'gratitude',
            'pride': 'gratitude',
            'relief': 'gratitude',
            'excitement': 'gratitude',  
            # Cognitive states
            'desire': 'curiosity',
            'surprise': 'confusion',  
            'realization': 'confusion',
            'nervousness': 'confusion'
        }

        def simplify_emotion(raw_emotion):
            return EMOTION_MAPPING.get(raw_emotion.lower(), 'neutral')
        
        text_lower = text.lower()
        churn_risk = any(
            keyword in text_lower 
            for keyword in self.churn_keywords
        )
        
        return {
            "overall_sentiment": overall_sentiment,
            "overall_emotion": simplify_emotion(emotion_result["label"]),
            "aspect_analysis": aspect_sentiments,
            "churn_risk": "high" if churn_risk else "low"
        }

if __name__ == "__main__":
    analyzer = ModelPipeline()
    
    test_texts = [
        "The driver was late but very polite",
        "App crashed 3 times during my ride",
        "Estimated fare was $10 but charged $15",
        "I'm switching to Uber after this terrible experience"
    ]
    
    results = []
    for text in test_texts:
        analysis = analyzer.build(text)
        results.append(analysis)
    

    df = pd.DataFrame(results)
    #df.to_csv("hee.csv")
    print(df)