"""
Sentiment Analyzer for HumAIne-chatbot

This module provides sentiment analysis functionality for user input.
"""

import re
from typing import Tuple


class SentimentAnalyzer:
    """Sentiment analyzer for user messages"""
    
    def __init__(self):
        """Initialize the sentiment analyzer"""
        # Pre-rated sentiment tokens
        self.sentiment_tokens = {
            # Positive words (score: 1-5)
            'excellent': 5, 'amazing': 5, 'outstanding': 5, 'fantastic': 5, 'brilliant': 5,
            'wonderful': 4, 'great': 4, 'awesome': 4, 'perfect': 4, 'superb': 4,
            'good': 3, 'nice': 3, 'fine': 3, 'okay': 2, 'alright': 2,
            'love': 5, 'adore': 5, 'enjoy': 4, 'like': 3, 'appreciate': 4,
            'helpful': 4, 'useful': 4, 'beneficial': 4, 'valuable': 4,
            'excited': 4, 'happy': 4, 'pleased': 4, 'satisfied': 3,
            'impressed': 4, 'surprised': 3, 'interested': 3,
            
            # Negative words (score: -1 to -5)
            'terrible': -5, 'awful': -5, 'horrible': -5, 'dreadful': -5, 'atrocious': -5,
            'bad': -3, 'poor': -3, 'worse': -4, 'worst': -5,
            'hate': -5, 'despise': -5, 'loathe': -5, 'dislike': -3, 'disappointed': -3,
            'frustrated': -3, 'angry': -4, 'annoyed': -3, 'irritated': -3,
            'confused': -2, 'lost': -2, 'unsure': -2, 'uncertain': -2,
            'useless': -4, 'pointless': -4, 'worthless': -4, 'meaningless': -4,
            'boring': -3, 'tedious': -3, 'monotonous': -3, 'repetitive': -2,
            'difficult': -2, 'hard': -2, 'challenging': -1, 'complex': -1,
            
            # Neutral words (score: 0)
            'maybe': 0, 'perhaps': 0, 'possibly': 0, 'might': 0, 'could': 0,
            'think': 0, 'believe': 0, 'suppose': 0, 'guess': 0,
            'question': 0, 'ask': 0, 'wonder': 0, 'curious': 0,
            'explain': 0, 'describe': 0, 'tell': 0, 'show': 0,
            'understand': 0, 'learn': 0, 'know': 0, 'see': 0,
        }
        
        # Emoji sentiment mapping
        self.emoji_sentiment = {
            '😀': 4, '😃': 4, '😄': 4, '😁': 4, '😆': 4, '😅': 3, '😂': 4, '🤣': 4,
            '😊': 4, '😇': 4, '🙂': 3, '🙃': 2, '😉': 3, '😌': 3, '😍': 5, '🥰': 5,
            '😘': 4, '😗': 3, '😙': 3, '😚': 4, '😋': 3, '😛': 2, '😝': 2, '😜': 2,
            '🤪': 2, '🤨': 0, '🧐': 0, '🤓': 1, '😎': 3, '🤩': 4, '🥳': 4, '😏': 1,
            '😒': -2, '😞': -3, '😔': -3, '😟': -2, '😕': -2, '🙁': -2, '☹️': -3,
            '😣': -3, '😖': -3, '😫': -3, '😩': -3, '🥺': -1, '😢': -3, '😭': -4,
            '😤': -2, '😠': -3, '😡': -4, '🤬': -5, '🤯': -2, '😳': -1, '🥵': -2,
            '🥶': -2, '😱': -3, '😨': -3, '😰': -3, '😥': -2, '😓': -2, '🤗': 3,
            '🤔': 0, '🤭': 1, '🤫': 0, '🤥': -3, '😶': 0, '😐': 0, '😑': 0, '😯': 0,
            '😦': -1, '😧': -2, '😮': 0, '😲': 0, '😴': -1, '🤤': -1, '😪': -1, '😵': -2,
            '🤐': 0, '🥴': -1, '🤢': -4, '🤮': -5, '🤧': -2, '😷': -1, '🤒': -2, '🤕': -2,
            '🤑': -2, '🤠': 2, '😈': -1, '👿': -3, '👹': -3, '👺': -3, '💀': -2, '👻': 1,
            '👽': 0, '🤖': 0, '😺': 4, '😸': 4, '😹': 4, '😻': 5, '😼': 1, '😽': 3,
            '🙀': -2, '😿': -3, '😾': -3, '🙈': 1, '🙉': 0, '🙊': 0, '💌': 3, '💘': 4,
            '💝': 4, '💖': 4, '💗': 3, '💙': 2, '💚': 2, '🧡': 2, '💛': 2, '💜': 2,
            '🖤': -1, '💔': -4, '❣️': 3, '💕': 4, '💞': 4, '💓': 3, '💗': 3, '💖': 4,
            '💘': 4, '💝': 4, '💟': 3, '☮️': 2, '✝️': 0, '☪️': 0, '🕉️': 0, '☸️': 0,
            '✡️': 0, '🔯': 0, '🕎': 0, '☯️': 0, '☦️': 0, '🛐': 0, '⛎': 0, '♈': 0,
            '♉': 0, '♊': 0, '♋': 0, '♌': 0, '♍': 0, '♎': 0, '♏': 0, '♐': 0, '♑': 0,
            '♒': 0, '♓': 0, '🆔': 0, '⚛️': 0, '🉑': 0, '☢️': -3, '☣️': -2, '📴': -1,
            '📳': 0, '🈶': 0, '🈚': 0, '🈸': 0, '🈺': 0, '🈷️': 0, '✴️': 0, '🆚': 0,
            '💮': 0, '🉐': 0, '㊙️': 0, '㊗️': 0, '🈴': 0, '🈵': 0, '🈹': 0, '🈲': 0,
            '🅰️': 0, '🅱️': 0, '🆎': 0, '🆑': 0, '🅾️': 0, '🆘': -3, '❌': -3, '⭕': 0,
            '🛑': -2, '🛡️': 0, '🈯': 0, '💯': 3, '💢': -3, '♨️': 0, '💠': 0, '🔰': 0,
            '🔱': 0, '⭕': 0, '✅': 3, '☑️': 2, '🔘': 0, '🔴': -1, '🟠': 0, '🟡': 0,
            '🟢': 1, '🔵': 0, '🟣': 0, '⚫': -1, '⚪': 0, '🟤': 0, '🔺': 0, '🔻': 0,
            '💠': 0, '🔘': 0, '🔶': 0, '🔷': 0, '🔸': 0, '🔹': 0, '🔺': 0, '🔻': 0,
            '💎': 3, '🔶': 0, '🔷': 0, '🔸': 0, '🔹': 0, '🔺': 0, '🔻': 0, '💎': 3,
            '🔶': 0, '🔷': 0, '🔸': 0, '🔹': 0, '🔺': 0, '🔻': 0, '💎': 3, '🔶': 0,
        }
    
    def analyze_sentiment(self, text: str) -> Tuple[int, int]:
        """
        Analyze sentiment of text
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (sentiment_score, normalized_sentiment_score)
        """
        if not text:
            return 0, 0
        
        # Convert to lowercase for analysis
        text_lower = text.lower()
        
        # Calculate sentiment score
        total_score = 0
        word_count = 0
        
        # Analyze words
        words = text_lower.split()
        for word in words:
            # Clean word (remove punctuation)
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word:
                word_count += 1
                if clean_word in self.sentiment_tokens:
                    total_score += self.sentiment_tokens[clean_word]
        
        # Analyze emojis
        for emoji, score in self.emoji_sentiment.items():
            if emoji in text:
                total_score += score
                word_count += 1
        
        # Calculate average sentiment score
        if word_count > 0:
            sentiment_score = total_score / word_count
        else:
            sentiment_score = 0
        
        # Normalize to -5 to 5 scale
        normalized_score = max(-5, min(5, sentiment_score))
        
        return int(sentiment_score), int(normalized_score) 