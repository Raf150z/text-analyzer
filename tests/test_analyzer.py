import unittest
import tempfile
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_analyzer import TextAnalyzer, AdvancedTextAnalyzer


class TestTextAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.sample_text = """
        This is a sample text. This text contains sample words.
        The sample text is used for testing the text analyzer.
        Multiple words appear multiple times in this sample text.
        """
        self.analyzer = TextAnalyzer(text=self.sample_text)
    
    def test_initialization(self):
        """Test analyzer initialization."""
        self.assertIsNotNone(self.analyzer)
        self.assertGreater(self.analyzer.total_words, 0)
        self.assertIsInstance(self.analyzer.word_frequency, dict)
    
    def test_word_frequency(self):
        """Test word frequency counting."""
        freq = self.analyzer.word_frequency
        self.assertIn('sample', freq)
        self.assertIn('text', freq)
        self.assertGreater(freq['sample'], 1)
    
    def test_unique_words(self):
        """Test unique words extraction."""
        unique = self.analyzer.unique_words
        self.assertIsInstance(unique, set)
        self.assertGreater(len(unique), 0)
        self.assertLess(len(unique), self.analyzer.total_words)
    
    def test_most_common(self):
        """Test most common words extraction."""
        top_3 = self.analyzer.get_most_common(3)
        self.assertEqual(len(top_3), 3)
        self.assertIsInstance(top_3, list)
        self.assertIsInstance(top_3[0], tuple)
    
    def test_search_word(self):
        """Test word search functionality."""
        self.assertEqual(self.analyzer.search_word('sample'), 4)
        self.assertEqual(self.analyzer.search_word('nonexistent'), 0)
        self.assertIsNone(self.analyzer.search_word(''))
    
    def test_statistics(self):
        """Test statistical calculations."""
        stats = self.analyzer.statistics
        self.assertIn('total_words', stats)
        self.assertIn('unique_words', stats)
        self.assertIn('lexical_diversity', stats)
        self.assertIn('average_word_length', stats)
    
    def test_compare_analyzers(self):
        """Test analyzer comparison."""
        text2 = "Different text with other words for comparison."
        analyzer2 = TextAnalyzer(text=text2)
        
        comparison = self.analyzer.compare_with(analyzer2)
        self.assertIn('common_words', comparison)
        self.assertIn('jaccard_similarity', comparison)
        self.assertGreater(comparison['jaccard_similarity'], 0)
    
    def test_generate_report(self):
        """Test report generation."""
        report = self.analyzer.generate_report('text')
        self.assertIsInstance(report, str)
        self.assertIn('TEXT ANALYSIS REPORT', report)
        self.assertIn('Total Words', report)
    
    def test_file_loading(self):
        """Test file loading functionality."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test file content for loading test.")
            temp_path = f.name
        
        try:
            analyzer = TextAnalyzer(file_path=temp_path)
            self.assertGreater(analyzer.total_words, 0)
        finally:
            os.unlink(temp_path)
    
    def test_exception_handling(self):
        """Test exception handling."""
        with self.assertRaises(ValueError):
            TextAnalyzer()
        
        with self.assertRaises(ValueError):
            TextAnalyzer(text="text", file_path="file.txt")
        
        with self.assertRaises(FileNotFoundError):
            TextAnalyzer(file_path="nonexistent_file.txt")


class TestAdvancedTextAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.sample_text = """
        This is a great and wonderful text. 
        It contains amazing words and wonderful phrases.
        Some parts are terrible and awful.
        """
        self.analyzer = AdvancedTextAnalyzer(text=self.sample_text)
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis."""
        sentiment = self.analyzer.sentiment_analysis()
        self.assertIn('positive', sentiment)
        self.assertIn('negative', sentiment)
        self.assertIn('sentiment_score', sentiment)
        self.assertGreater(sentiment['positive'], sentiment['negative'])
    
    def test_ngrams(self):
        """Test n-gram extraction."""
        bigrams = self.analyzer.get_ngrams(2)
        self.assertIsInstance(bigrams, dict)
        self.assertGreater(len(bigrams), 0)
    
    def test_inheritance_polymorphism(self):
        """Test inheritance and method overriding."""
        report = self.analyzer.generate_report('text')
        self.assertIn('SENTIMENT ANALYSIS', report)


if __name__ == '__main__':
    unittest.main()