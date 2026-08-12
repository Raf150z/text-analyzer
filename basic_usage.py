from src.text_analyzer import TextAnalyzer

text = "Python is a high-level, interpreted, general-purpose programming language designed with an emphasis on code readability and simplicity. Created by Guido van Rossum and released in 1991, its syntax allows developers to express concepts in fewer lines of code compared to languages like C++ or Java. It uses English-like keywords and relies on indentation instead of curly brackets to define blocks of code"
analyzer = TextAnalyzer(text=text)

print(f"Total words: {analyzer.total_words}")
print(f"Unique words: {len(analyzer.unique_words)}")

top_words = analyzer.get_most_common(10)
for word, count in top_words:
    print(f"{word}: {count}")