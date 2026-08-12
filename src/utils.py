import re
import time
from functools import wraps
from typing import List, Dict, Set, Any
import logging

logger = logging.getLogger(__name__)


def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        logger.info(f"{func.__name__} executed in {elapsed:.4f} seconds")
        return result
    return wrapper


def validate_text(func):

    @wraps(func)
    def wrapper(text, *args, **kwargs):
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        return func(text, *args, **kwargs)
    return wrapper


def clean_text(text: str) -> str:

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove email addresses
    text = re.sub(r'\S+@\S+\.\S+', '', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\?\!]', '', text)
    return text.strip()


def batch_process_files(file_paths: List[str], analyzer_class) -> List[Dict[str, Any]]:

    results = []
    
    for file_path in file_paths:
        try:
            analyzer = analyzer_class(file_path=file_path)
            results.append({
                'file': file_path,
                'total_words': analyzer.total_words,
                'unique_words': len(analyzer.unique_words),
                'statistics': analyzer.statistics
            })
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            results.append({
                'file': file_path,
                'error': str(e)
            })
    
    return results


def create_word_cloud_data(word_freq: Dict[str, int], max_words: int = 100) -> List[Dict]:

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:max_words]
    
    # Create format for word cloud library
    word_cloud_data = [
        {'word': word, 'count': count, 'size': count * 10}
        for word, count in sorted_words
    ]
    
    return word_cloud_data


def find_anagrams(word: str, word_list: Set[str]) -> List[str]:

    if not word:
        return []
    
    # Sort characters for comparison
    sorted_word = ''.join(sorted(word.lower()))
    
    anagrams = []
    for w in word_list:
        if len(w) == len(word) and w.lower() != word.lower():
            if ''.join(sorted(w.lower())) == sorted_word:
                anagrams.append(w)
    
    return anagrams