"""
Language Complexity Analyzer for HumAIne-chatbot

This module provides language complexity analysis functionality for user input.
"""

import re
from typing import Tuple


class LanguageComplexityAnalyzer:
    """Language complexity analyzer for user messages"""
    
    def __init__(self, asl_weight: float = 0.5, ttr_weight: float = 0.5):
        """
        Initialize the language complexity analyzer
        
        Args:
            asl_weight: Weight for average sentence length (0.0 to 1.0)
            ttr_weight: Weight for type-token ratio (0.0 to 1.0)
        """
        self.asl_weight = asl_weight
        self.ttr_weight = ttr_weight
        
        # Validate weights
        if abs(asl_weight + ttr_weight - 1.0) > 0.01:
            raise ValueError("Weights must sum to 1.0")
    
    def calculate_average_sentence_length(self, text: str) -> int:
        """
        Calculate average sentence length
        
        Args:
            text: The text to analyze
            
        Returns:
            Average sentence length in words
        """
        if not text:
            return 0
        
        # Split into sentences (simple approach)
        sentences = re.split(r'[.!?]+', text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0
        
        # Calculate total words
        total_words = 0
        for sentence in sentences:
            words = sentence.split()
            total_words += len(words)
        
        # Calculate average
        return total_words // len(sentences)
    
    def calculate_type_token_ratio(self, text: str) -> float:
        """
        Calculate type-token ratio (vocabulary diversity)
        
        Args:
            text: The text to analyze
            
        Returns:
            Type-token ratio (0.0 to 1.0)
        """
        if not text:
            return 0.0
        
        # Convert to lowercase and split into words
        words = text.lower().split()
        
        if not words:
            return 0.0
        
        # Count unique words (types)
        unique_words = set(words)
        
        # Calculate ratio
        ttr = len(unique_words) / len(words)
        
        return min(1.0, ttr)  # Ensure it's not greater than 1.0
    
    def analyze_complexity(self, text: str) -> Tuple[int, float, float]:
        """
        Analyze language complexity of text
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (average_sentence_length, type_token_ratio, complexity_score)
        """
        if not text:
            return 0, 0.0, 0.0
        
        # Calculate metrics
        asl = self.calculate_average_sentence_length(text)
        ttr = self.calculate_type_token_ratio(text)
        
        # Normalize ASL to 0-1 scale (assuming typical range is 5-25 words)
        normalized_asl = max(0.0, min(1.0, (asl - 5) / 20))
        
        # Calculate weighted complexity score
        complexity = (self.asl_weight * normalized_asl) + (self.ttr_weight * ttr)
        
        return asl, ttr, complexity 