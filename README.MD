# 📊 Text Analyzer - Professional Python Text Analysis Tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Overview

Text Analyzer is a professional Python library for comprehensive text analysis. It provides advanced statistical analysis, word frequency counting, lexical diversity metrics, and comparative analysis of multiple texts.

### 🎯 Key Features

- **📊 Statistical Analysis**: Total words, unique words, lexical diversity
- **🔍 Word Frequency**: Count and track word occurrences
- **📈 Reports**: Generate professional text and JSON reports
- **💭 Sentiment Analysis**: Basic sentiment detection (Advanced version)
- **📏 Word Length Analysis**: Distribution and statistics
- **🔄 Text Comparison**: Compare multiple texts with Jaccard similarity
- **💾 Multiple Formats**: Export to TXT, JSON, CSV
- **⚡ Batch Processing**: Analyze multiple files efficiently
- **🧪 Fully Tested**: Comprehensive unit tests

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Raf150z/text-analyzer.git
cd text-analyzer
pip install -r requirements.txt
```

### Basic Usage
'''bash
from src.text_analyzer import TextAnalyzer

# Analyze text
text = "Your text to analyze goes here."
analyzer = TextAnalyzer(text=text)

# Get statistics
print(f"Total words: {analyzer.total_words}")
print(f"Unique words: {len(analyzer.unique_words)}")

# Get most common words
top_words = analyzer.get_most_common(10)
for word, count in top_words:
    print(f"{word}: {count}")
'''

### Advanced Usage
'''bash
from src.text_analyzer import AdvancedTextAnalyzer
from src.file_handler import FileHandler

# Analyze file
analyzer = AdvancedTextAnalyzer(file_path="document.txt")

# Generate and save report
report = analyzer.generate_report()
handler = FileHandler("output")
handler.save_report(report, "analysis_report", "txt")
'''

