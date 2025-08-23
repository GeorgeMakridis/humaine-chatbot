"""
Enhanced Language Analysis for HumAIne-chatbot

This module provides sophisticated language analysis for user profiling,
including complexity assessment, sentiment analysis, and grammar evaluation.
"""

import re
from typing import Dict, Any, Tuple
from textstat import textstat
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('stopwords', quiet=True)
    except:
        pass

class EnhancedLanguageAnalyzer:
    """Advanced language analysis for user profiling"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english')) if 'stopwords' in nltk.data.find('corpora') else set()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Comprehensive text analysis"""
        if not text or not text.strip():
            return self._empty_analysis()
        
        # Basic metrics
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = len(sent_tokenize(text))
        
        # Advanced metrics
        complexity_score = self._calculate_complexity_score(text)
        sentiment_score = self._analyze_sentiment(text)
        grammar_score = self._analyze_grammar(text)
        vocabulary_richness = self._calculate_vocabulary_richness(text)
        
        return {
            "basic_metrics": {
                "word_count": word_count,
                "char_count": char_count,
                "sentence_count": sentence_count,
                "avg_sentence_length": word_count / max(sentence_count, 1),
                "avg_word_length": char_count / max(word_count, 1)
            },
            "complexity_analysis": complexity_score,
            "sentiment_analysis": sentiment_score,
            "grammar_analysis": grammar_score,
            "vocabulary_analysis": vocabulary_richness,
            "overall_score": self._calculate_overall_score(complexity_score, sentiment_score, grammar_score, vocabulary_richness)
        }
    
    def _calculate_complexity_score(self, text: str) -> Dict[str, Any]:
        """Calculate language complexity score"""
        try:
            # Flesch Reading Ease
            flesch_ease = textstat.flesch_reading_ease(text)
            
            # Flesch-Kincaid Grade Level
            flesch_grade = textstat.flesch_kincaid_grade(text)
            
            # Gunning Fog Index
            gunning_fog = textstat.gunning_fog(text)
            
            # SMOG Index
            smog_index = textstat.smog_index(text)
            
            # Automated Readability Index
            ari = textstat.automated_readability_index(text)
            
            # Coleman-Liau Index
            coleman_liau = textstat.coleman_liau_index(text)
            
            # Linsear Write Formula
            linsear_write = textstat.linsear_write_formula(text)
            
            # Dale-Chall Readability Score
            dale_chall = textstat.dale_chall_readability_score(text)
            
            # Syllable count
            syllable_count = textstat.syllable_count(text)
            
            # Lexicon count
            lexicon_count = textstat.lexicon_count(text)
            
            return {
                "flesch_reading_ease": flesch_ease,
                "flesch_kincaid_grade": flesch_grade,
                "gunning_fog": gunning_fog,
                "smog_index": smog_index,
                "automated_readability_index": ari,
                "coleman_liau_index": coleman_liau,
                "linsear_write": linsear_write,
                "dale_chall_score": dale_chall,
                "syllable_count": syllable_count,
                "lexicon_count": lexicon_count,
                "complexity_level": self._classify_complexity(flesch_ease, flesch_grade)
            }
        except Exception as e:
            return {
                "error": str(e),
                "complexity_level": "medium"
            }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment"""
        try:
            # Basic sentiment indicators
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'joy']
            negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'disappointed']
            
            words = text.lower().split()
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            
            # Exclamation and question analysis
            exclamation_count = text.count('!')
            question_count = text.count('?')
            
            # Capitalization analysis (enthusiasm indicator)
            caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
            
            # Sentiment score calculation
            sentiment_score = (positive_count - negative_count) / max(len(words), 1)
            normalized_score = max(-1, min(1, sentiment_score * 10))  # Scale to -1 to 1
            
            return {
                "positive_words": positive_count,
                "negative_words": negative_count,
                "exclamation_count": exclamation_count,
                "question_count": question_count,
                "capitalization_ratio": caps_ratio,
                "sentiment_score": normalized_score,
                "sentiment_label": self._classify_sentiment(normalized_score),
                "enthusiasm_level": self._classify_enthusiasm(exclamation_count, caps_ratio)
            }
        except Exception as e:
            return {
                "error": str(e),
                "sentiment_score": 0,
                "sentiment_label": "neutral"
            }
    
    def _analyze_grammar(self, text: str) -> Dict[str, Any]:
        """Analyze grammar and writing quality"""
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            # Basic grammar checks
            proper_sentence_start = sum(1 for s in sentences if s[0].isupper())
            proper_sentence_end = sum(1 for s in sentences if s.rstrip()[-1] in '.!?')
            
            # Word-level analysis
            pos_tags = pos_tag(words) if words else []
            nouns = sum(1 for word, tag in pos_tags if tag.startswith('NN'))
            verbs = sum(1 for word, tag in pos_tags if tag.startswith('VB'))
            adjectives = sum(1 for word, tag in pos_tags if tag.startswith('JJ'))
            
            # Punctuation analysis
            punctuation_count = sum(1 for c in text if c in '.,;:!?')
            comma_count = text.count(',')
            period_count = text.count('.')
            
            # Grammar score calculation
            grammar_score = 0
            if sentences:
                grammar_score += (proper_sentence_start / len(sentences)) * 0.3
                grammar_score += (proper_sentence_end / len(sentences)) * 0.3
            
            if words:
                grammar_score += min(1.0, punctuation_count / len(words)) * 0.2
                grammar_score += min(1.0, (nouns + verbs + adjectives) / len(words)) * 0.2
            
            return {
                "proper_sentence_start": proper_sentence_start,
                "proper_sentence_end": proper_sentence_end,
                "noun_count": nouns,
                "verb_count": verbs,
                "adjective_count": adjectives,
                "punctuation_count": punctuation_count,
                "comma_count": comma_count,
                "period_count": period_count,
                "grammar_score": grammar_score,
                "grammar_quality": self._classify_grammar_quality(grammar_score)
            }
        except Exception as e:
            return {
                "error": str(e),
                "grammar_score": 0.5,
                "grammar_quality": "medium"
            }
    
    def _calculate_vocabulary_richness(self, text: str) -> Dict[str, Any]:
        """Calculate vocabulary richness metrics"""
        try:
            words = word_tokenize(text.lower())
            unique_words = set(words)
            
            # Type-token ratio
            type_token_ratio = len(unique_words) / max(len(words), 1)
            
            # Hapax legomena (words appearing only once)
            word_freq = {}
            for word in words:
                if word.isalpha():  # Only alphabetic words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            hapax_count = sum(1 for freq in word_freq.values() if freq == 1)
            hapax_ratio = hapax_count / max(len(word_freq), 1)
            
            # Stop word ratio (common words)
            stop_word_count = sum(1 for word in words if word in self.stop_words)
            stop_word_ratio = stop_word_count / max(len(words), 1)
            
            # Vocabulary diversity score
            vocab_diversity = (type_token_ratio * 0.4 + hapax_ratio * 0.3 + (1 - stop_word_ratio) * 0.3)
            
            return {
                "type_token_ratio": type_token_ratio,
                "unique_words": len(unique_words),
                "total_words": len(words),
                "hapax_legomena": hapax_count,
                "hapax_ratio": hapax_ratio,
                "stop_word_count": stop_word_count,
                "stop_word_ratio": stop_word_ratio,
                "vocabulary_diversity": vocab_diversity,
                "vocabulary_level": self._classify_vocabulary_level(vocab_diversity)
            }
        except Exception as e:
            return {
                "error": str(e),
                "vocabulary_diversity": 0.5,
                "vocabulary_level": "medium"
            }
    
    def _calculate_overall_score(self, complexity: Dict, sentiment: Dict, grammar: Dict, vocabulary: Dict) -> float:
        """Calculate overall language quality score"""
        try:
            # Normalize scores
            complexity_score = min(1.0, max(0.0, complexity.get('flesch_reading_ease', 50) / 100))
            sentiment_score = (sentiment.get('sentiment_score', 0) + 1) / 2  # Convert -1,1 to 0,1
            grammar_score = grammar.get('grammar_score', 0.5)
            vocab_score = vocabulary.get('vocabulary_diversity', 0.5)
            
            # Weighted average
            overall_score = (
                complexity_score * 0.25 +
                sentiment_score * 0.25 +
                grammar_score * 0.25 +
                vocab_score * 0.25
            )
            
            return round(overall_score, 3)
        except:
            return 0.5
    
    def _classify_complexity(self, flesch_ease: float, flesch_grade: float) -> str:
        """Classify text complexity level"""
        if flesch_ease >= 90:
            return "very_easy"
        elif flesch_ease >= 80:
            return "easy"
        elif flesch_ease >= 70:
            return "fairly_easy"
        elif flesch_ease >= 60:
            return "standard"
        elif flesch_ease >= 50:
            return "fairly_difficult"
        elif flesch_ease >= 30:
            return "difficult"
        else:
            return "very_difficult"
    
    def _classify_sentiment(self, score: float) -> str:
        """Classify sentiment based on score"""
        if score > 0.3:
            return "positive"
        elif score < -0.3:
            return "negative"
        else:
            return "neutral"
    
    def _classify_enthusiasm(self, exclamation_count: int, caps_ratio: float) -> str:
        """Classify enthusiasm level"""
        if exclamation_count > 2 or caps_ratio > 0.1:
            return "high"
        elif exclamation_count > 0 or caps_ratio > 0.05:
            return "medium"
        else:
            return "low"
    
    def _classify_grammar_quality(self, score: float) -> str:
        """Classify grammar quality"""
        if score > 0.8:
            return "excellent"
        elif score > 0.6:
            return "good"
        elif score > 0.4:
            return "fair"
        else:
            return "poor"
    
    def _classify_vocabulary_level(self, diversity: float) -> str:
        """Classify vocabulary level"""
        if diversity > 0.8:
            return "advanced"
        elif diversity > 0.6:
            return "intermediate"
        elif diversity > 0.4:
            return "basic"
        else:
            return "limited"
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure"""
        return {
            "basic_metrics": {
                "word_count": 0,
                "char_count": 0,
                "sentence_count": 0,
                "avg_sentence_length": 0,
                "avg_word_length": 0
            },
            "complexity_analysis": {"complexity_level": "medium"},
            "sentiment_analysis": {"sentiment_score": 0, "sentiment_label": "neutral"},
            "grammar_analysis": {"grammar_score": 0.5, "grammar_quality": "medium"},
            "vocabulary_analysis": {"vocabulary_diversity": 0.5, "vocabulary_level": "medium"},
            "overall_score": 0.5
        }
