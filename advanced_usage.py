from src.text_analyzer import AdvancedTextAnalyzer
from src.file_handler import FileHandler

analyzer = AdvancedTextAnalyzer(file_path="document.txt")

report = analyzer.generate_report()
handler = FileHandler("output")
handler.save_report(report, "analysis_report", "txt")