import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_analyzer import TextAnalyzer, AdvancedTextAnalyzer
from src.file_handler import FileHandler
from src.utils import create_word_cloud_data, batch_process_files


def example_basic_usage():
    """Example of basic text analysis."""
    print("\n" + "="*60)
    print("EXAMPLE 1: BASIC TEXT ANALYSIS")
    print("="*60)
    
    sample_text = """
    Artificial intelligence is transforming the world. 
    Machine learning and deep learning are key technologies.
    Python is the most popular language for AI development.
    The future of AI is exciting and full of possibilities.
    """
    
    # Create analyzer
    analyzer = TextAnalyzer(text=sample_text)
    
    # Print basic information
    print(f"\n📊 Analysis Results:")
    print(f"Total Words: {analyzer.total_words}")
    print(f"Unique Words: {len(analyzer.unique_words)}")
    print(f"Average Word Length: {analyzer.statistics['average_word_length']:.2f}")
    
    # Get most common words
    print(f"\n🔝 Top 5 Most Common Words:")
    for word, count in analyzer.get_most_common(5):
        print(f"  {word}: {count}")
    
    # Generate and save report
    report = analyzer.generate_report()
    print(f"\n📄 Report Preview:\n{report[:500]}...")
    
    return analyzer


def example_advanced_usage():
    """Example of advanced text analysis with file handling."""
    print("\n" + "="*60)
    print("EXAMPLE 2: ADVANCED ANALYSIS WITH FILE HANDLING")
    print("="*60)
    
    # Create sample file
    sample_path = Path("examples/sample_input.txt")
    sample_path.parent.mkdir(exist_ok=True)
    
    sample_text = """
    The beautiful sunset painted the sky in amazing colors.
    The wonderful view was truly breathtaking and spectacular.
    Some people say the sunset is the most beautiful moment of the day.
    """
    sample_path.write_text(sample_text, encoding='utf-8')
    
    # Analyze file
    analyzer = AdvancedTextAnalyzer(file_path=str(sample_path))
    
    # Get sentiment
    sentiment = analyzer.sentiment_analysis()
    print(f"\n💭 Sentiment Analysis:")
    print(f"  Positive: {sentiment['positive']}")
    print(f"  Negative: {sentiment['negative']}")
    print(f"  Overall: {sentiment['sentiment']}")
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save with file handler
    handler = FileHandler("examples/output")
    handler.save_report(report, "advanced_analysis_report", "txt")
    
    # Export to CSV
    handler.export_to_csv(analyzer.word_frequency, "word_frequency_export")
    
    print(f"\n✅ Results saved to 'examples/output/' directory")
    
    return analyzer


def example_comparison():
    """Example of comparing multiple texts."""
    print("\n" + "="*60)
    print("EXAMPLE 3: COMPARING MULTIPLE TEXTS")
    print("="*60)
    
    texts = [
        "Artificial intelligence and machine learning are transforming technology.",
        "Deep learning and neural networks are key components of modern AI systems.",
        "The future of artificial intelligence is full of exciting possibilities."
    ]
    
    analyzers = [TextAnalyzer(text=t) for t in texts]
    
    # Compare first two texts
    comparison = analyzers[0].compare_with(analyzers[1])
    
    print(f"\n📊 Comparison Results:")
    print(f"Common Words: {comparison['common_count']}")
    print(f"Jaccard Similarity: {comparison['jaccard_similarity']:.2%}")
    print(f"Words Unique to Text 1: {len(comparison['unique_to_self'])}")
    print(f"Words Unique to Text 2: {len(comparison['unique_to_other'])}")
    
    return analyzers


def example_batch_processing():
    """Example of batch processing multiple files."""
    print("\n" + "="*60)
    print("EXAMPLE 4: BATCH PROCESSING")
    print("="*60)
    
    # Create multiple sample files
    texts = [
        "First sample text for batch processing.",
        "Second sample text with different content.",
        "Third sample text for comprehensive analysis."
    ]
    
    file_paths = []
    for i, text in enumerate(texts, 1):
        path = Path(f"examples/batch/sample_{i}.txt")
        path.parent.mkdir(exist_ok=True)
        path.write_text(text, encoding='utf-8')
        file_paths.append(str(path))
    
    # Batch process
    results = batch_process_files(file_paths, TextAnalyzer)
    
    print(f"\n📊 Batch Processing Results:")
    for result in results:
        if 'error' in result:
            print(f"  ❌ {result['file']}: {result['error']}")
        else:
            print(f"  ✅ {result['file']}: {result['total_words']} words, {result['unique_words']} unique")
    
    return results


def main():
    """Main example execution."""
    print("🚀 TEXT ANALYZER - COMPREHENSIVE EXAMPLES\n")
    
    examples = [
        ("Basic Analysis", example_basic_usage),
        ("Advanced Analysis", example_advanced_usage),
        ("Text Comparison", example_comparison),
        ("Batch Processing", example_batch_processing)
    ]
    
    for name, func in examples:
        try:
            func()
            print(f"\n✅ {name} completed successfully!")
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")
    
    print("\n" + "="*60)
    print("🎉 All examples completed!")
    print("Check the generated files in the 'examples/' directory.")


if __name__ == "__main__":
    main()