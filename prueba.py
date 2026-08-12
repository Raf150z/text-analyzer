from src.text_analyzer import TextAnalyzer, AdvancedTextAnalyzer

analyzer = TextAnalyzer(text="Hola mundo, este es un texto de prueba")

print(f"Total words: {analyzer.total_words}")
print(f"Unique words: {len(analyzer.unique_words)}")
print(analyzer.get_most_common(5))