import re
from collections import Counter, defaultdict
from typing import List, Dict, Set, Tuple, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextAnalyzer:
    
    def __init__(self, text: str = "", file_path: Optional[str] = None):

        if text and file_path:
            raise ValueError("Provide either text string or file_path, not both")
        
        if not text and not file_path:
            raise ValueError("Must provide either text string or file_path")
        
        self._original_text = text
        self._file_path = file_path
        self._processed_words: List[str] = []
        self._word_frequency: Dict[str, int] = {}
        self._unique_words: Set[str] = set()
        self._word_stats = {}
        
        # Load and process text
        self._load_text()
        self._process_text()
        
        logger.info(f"TextAnalyzer initialized with {len(self._processed_words)} words")
    
    def _load_text(self) -> None:

        if self._file_path:
            try:
                with open(self._file_path, 'r', encoding='utf-8') as file:
                    self._original_text = file.read()
                logger.info(f"Loaded file: {self._file_path}")
            except FileNotFoundError:
                logger.error(f"File not found: {self._file_path}")
                raise
            except PermissionError:
                logger.error(f"Permission denied: {self._file_path}")
                raise
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                raise
    
    def _process_text(self) -> None:

        if not self._original_text:
            return
        
        # Clean text: remove punctuation, convert to lowercase
        clean_text = re.sub(r'[^\w\s]', ' ', self._original_text)
        clean_text = re.sub(r'\d+', '', clean_text)  # Remove numbers
        
        # Split into words
        words = clean_text.lower().split()
        
        # Filter empty strings and very short words (optional)
        self._processed_words = [word for word in words if len(word) > 1]
        
        # Build frequency dictionary
        self._word_frequency = Counter(self._processed_words)
        
        # Build unique words set
        self._unique_words = set(self._processed_words)
        
        # Calculate statistics
        self._calculate_statistics()
    
    def _calculate_statistics(self) -> None:

        total_words = len(self._processed_words)
        unique_count = len(self._unique_words)
        
        # Calculate lexical diversity
        lexical_diversity = unique_count / total_words if total_words > 0 else 0
        
        # Find most common words
        most_common = self._word_frequency.most_common(10)
        
        # Find words by length distribution
        length_distribution = defaultdict(int)
        for word in self._processed_words:
            length_distribution[len(word)] += 1
        
        # Average word length
        avg_length = sum(len(word) for word in self._processed_words) / total_words if total_words > 0 else 0
        
        self._word_stats = {
            'total_words': total_words,
            'unique_words': unique_count,
            'lexical_diversity': lexical_diversity,
            'most_common_words': most_common,
            'length_distribution': dict(length_distribution),
            'average_word_length': avg_length,
            'longest_word': max(self._processed_words, key=len) if self._processed_words else "",
            'shortest_word': min(self._processed_words, key=len) if self._processed_words else "",
        }
    
        
    @property
    def word_frequency(self) -> Dict[str, int]:
        """Get word frequency dictionary."""
        return self._word_frequency.copy()  # Return copy for encapsulation
    
    @property
    def unique_words(self) -> Set[str]:
        """Get set of unique words."""
        return self._unique_words.copy()
    
    @property
    def total_words(self) -> int:
        """Get total word count."""
        return self._word_stats.get('total_words', 0)
    
    @property
    def statistics(self) -> Dict:
        """Get all statistics."""
        return self._word_stats.copy()
    
    
    def get_most_common(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        Get n most common words.
        
        Implements:
        - Dictionary operations
        - List sorting algorithm (built-in Timsort)
        - Slicing for performance
        """
        if n <= 0:
            return []
        # Using Counter's most_common which uses heap algorithm
        return self._word_frequency.most_common(n)
    
    def search_word(self, word: str) -> Optional[int]:

        try:
            if not word:
                raise ValueError("Word cannot be empty")
            word = word.lower().strip()
            return self._word_frequency.get(word, 0)
        except Exception as e:
            logger.error(f"Error searching for word '{word}': {e}")
            return None
    
    def get_words_by_length(self, length: int) -> List[str]:

        if length <= 0:
            return []
        return [word for word in self._processed_words if len(word) == length]
    
    def compare_with(self, other_analyzer: 'TextAnalyzer') -> Dict:

        if not isinstance(other_analyzer, TextAnalyzer):
            raise TypeError("Must compare with another TextAnalyzer instance")
        
        # Find common and unique words using set operations
        common_words = self._unique_words & other_analyzer._unique_words
        unique_to_self = self._unique_words - other_analyzer._unique_words
        unique_to_other = other_analyzer._unique_words - self._unique_words
        
        # Calculate similarity (Jaccard similarity)
        union = self._unique_words | other_analyzer._unique_words
        jaccard = len(common_words) / len(union) if union else 0
        
        return {
            'common_words': common_words,
            'common_count': len(common_words),
            'unique_to_self': unique_to_self,
            'unique_to_other': unique_to_other,
            'jaccard_similarity': jaccard,
            'size_self': self.total_words,
            'size_other': other_analyzer.total_words
        }
    
    def generate_report(self, format_type: str = "text") -> str:

        if format_type.lower() == "text":
            return self._generate_text_report()
        elif format_type.lower() == "json":
            return self._generate_json_report()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_text_report(self) -> str:
        """Generate text format report."""
        stats = self._word_stats
        
        report = f"""
        ╔══════════════════════════════════════════════════════════════╗
        ║                   TEXT ANALYSIS REPORT                      ║
        ╚══════════════════════════════════════════════════════════════╝
        
        📊 BASIC STATISTICS
        ──────────────────────────────────────────────────────────────
        Total Words:        {stats['total_words']:,}
        Unique Words:       {stats['unique_words']:,}
        Lexical Diversity:  {stats['lexical_diversity']:.2%}
        Average Word Length:{stats['average_word_length']:.2f} characters
        
        📝 LONGEST AND SHORTEST WORDS
        ──────────────────────────────────────────────────────────────
        Longest:  "{stats['longest_word']}" ({len(stats['longest_word'])} chars)
        Shortest: "{stats['shortest_word']}" ({len(stats['shortest_word'])} chars)
        
        🔝 TOP 10 MOST FREQUENT WORDS
        ──────────────────────────────────────────────────────────────
        """
        
        for i, (word, count) in enumerate(stats['most_common_words'], 1):
            percentage = (count / stats['total_words']) * 100
            report += f"        {i:2d}. {word:15s} → {count:4d} times ({percentage:5.2f}%)\n"
        
        # Word length distribution
        report += f"""
        📏 WORD LENGTH DISTRIBUTION
        ──────────────────────────────────────────────────────────────
        """
        
        for length, count in sorted(stats['length_distribution'].items()):
            bar = "█" * min(count, 50)  # Limit bar length
            report += f"        {length:2d} chars: {bar} {count}\n"
        
        report += """
        ══════════════════════════════════════════════════════════════
        Report generated by TextAnalyzer v1.0.0
        """
        
        return report
    
    def _generate_json_report(self) -> str:
        """Generate JSON format report."""
        import json
        # Convert sets to lists for JSON serialization
        stats_copy = self._word_stats.copy()
        stats_copy['most_common_words'] = [
            {'word': word, 'count': count} 
            for word, count in stats_copy['most_common_words']
        ]
        return json.dumps(stats_copy, indent=2)
    
    def __str__(self) -> str:
        """String representation of the analyzer."""
        return f"TextAnalyzer(words={self.total_words}, unique={len(self._unique_words)})"
    
    def __len__(self) -> int:
        """Return total word count."""
        return self.total_words



class AdvancedTextAnalyzer(TextAnalyzer):

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sentiment_words = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'wonderful'],
            'negative': ['bad', 'terrible', 'awful', 'horrible', 'poor']
        }
    
    def sentiment_analysis(self) -> Dict[str, int]:

        positive_count = 0
        negative_count = 0
        
        for word in self._processed_words:
            if word in self._sentiment_words['positive']:
                positive_count += 1
            elif word in self._sentiment_words['negative']:
                negative_count += 1
        
        total = positive_count + negative_count
        sentiment_score = (positive_count - negative_count) / total if total > 0 else 0
        
        return {
            'positive': positive_count,
            'negative': negative_count,
            'sentiment_score': sentiment_score,
            'sentiment': 'Positive' if sentiment_score > 0.1 else 'Negative' if sentiment_score < -0.1 else 'Neutral'
        }
    
    def get_ngrams(self, n: int = 2) -> Dict[str, int]:

        if n < 1:
            raise ValueError("n must be at least 1")
        
        ngrams = []
        for i in range(len(self._processed_words) - n + 1):
            ngram = ' '.join(self._processed_words[i:i+n])
            ngrams.append(ngram)
        
        return dict(Counter(ngrams).most_common(20))
    
    def generate_report(self, format_type: str = "text") -> str:

        base_report = super().generate_report(format_type)
        
        if format_type.lower() == "text":
            sentiment = self.sentiment_analysis()
            return base_report + f"""
            
            💭 SENTIMENT ANALYSIS
            ──────────────────────────────────────────────────────────────
            Positive Words: {sentiment['positive']}
            Negative Words: {sentiment['negative']}
            Sentiment Score: {sentiment['sentiment_score']:.2f}
            Overall Sentiment: {sentiment['sentiment']}
            """
        
        return base_report