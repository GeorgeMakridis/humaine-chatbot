"""
Grammar Checker for HumAIne-chatbot

This module provides grammar analysis functionality for user input.
"""

import re
from typing import Tuple


class GrammarChecker:
    """Grammar checker for analyzing user input"""
    
    def __init__(self):
        """Initialize the grammar checker"""
        # Simple patterns for common grammar mistakes
        self.informal_patterns = [
            r'\b(u|ur|u\'re|u\'ve|u\'ll|u\'d)\b',  # Informal you
            r'\b(pls|plz)\b',  # Please
            r'\b(thx|tnx)\b',  # Thanks
            r'\b(omg|wtf|lol|rofl)\b',  # Internet slang
            r'\b(btw|imo|tbh|fyi)\b',  # Abbreviations
            r'\b(2|4|b4|gr8)\b',  # Number substitutions
        ]
        
        # Common spelling mistakes
        self.spelling_mistakes = [
            (r'\bteh\b', 'the'),
            (r'\brecieve\b', 'receive'),
            (r'\bseperate\b', 'separate'),
            (r'\boccured\b', 'occurred'),
            (r'\bdefinately\b', 'definitely'),
            (r'\bneccessary\b', 'necessary'),
            (r'\baccomodate\b', 'accommodate'),
            (r'\bbegining\b', 'beginning'),
            (r'\bbeleive\b', 'believe'),
            (r'\bcalender\b', 'calendar'),
        ]
    
    def count_words(self, text: str) -> int:
        """Count words in text"""
        if not text:
            return 0
        return len(text.split())
    
    def count_grammatical_mistakes(self, text: str) -> int:
        """Count grammatical mistakes in text"""
        if not text:
            return 0
        
        mistakes = 0
        
        # Check for informal patterns
        for pattern in self.informal_patterns:
            matches = re.findall(pattern, text.lower())
            mistakes += len(matches)
        
        # Check for common spelling mistakes
        for wrong, correct in self.spelling_mistakes:
            matches = re.findall(wrong, text.lower())
            mistakes += len(matches)
        
        # Check for basic grammar issues
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Check for sentence starting with lowercase
                if sentence and sentence[0].islower():
                    mistakes += 1
                
                # Check for missing spaces after punctuation
                if re.search(r'[.!?][a-zA-Z]', sentence):
                    mistakes += 1
        
        return mistakes
    
    def analyze_grammar(self, text: str) -> Tuple[int, int, float]:
        """
        Analyze grammar of text
        
        Returns:
            Tuple of (total_words, mistakes_count, grammatical_mistakes_frequency)
        """
        if not text:
            return 0, 0, 0.0
        
        total_words = self.count_words(text)
        mistakes = self.count_grammatical_mistakes(text)
        
        # Calculate frequency
        frequency = mistakes / max(total_words, 1)
        
        return total_words, mistakes, frequency 