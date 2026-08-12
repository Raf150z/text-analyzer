import json
import csv
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class FileHandler:

    SUPPORTED_FORMATS = ['.txt', '.json', '.csv']
    
    def __init__(self, base_path: Optional[str] = None):

        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.base_path.mkdir(exist_ok=True)
        logger.info(f"FileHandler initialized at {self.base_path}")
    
    def save_report(self, report: str, filename: str, format_type: str = 'txt') -> str:

        try:
            file_path = self.base_path / f"{filename}.{format_type}"
            
            # Validate extension
            if f'.{format_type}' not in self.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported format: {format_type}")
            
            # Write file based on format
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"Report saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            raise
    
    def save_analysis_results(self, results: Dict, filename: str) -> str:

        try:
            file_path = self.base_path / f"{filename}.json"
            
            # Convert sets to lists for JSON serialization
            serializable_results = self._make_serializable(results)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            raise
    
    def export_to_csv(self, word_freq: Dict[str, int], filename: str) -> str:

        try:
            file_path = self.base_path / f"{filename}.csv"
            
            # Sort by frequency descending
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Word', 'Frequency', 'Percentage'])
                
                total = sum(word_freq.values())
                for word, count in sorted_words:
                    percentage = (count / total) * 100 if total > 0 else 0
                    writer.writerow([word, count, f"{percentage:.2f}%"])
            
            logger.info(f"CSV exported: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error exporting CSV: {e}")
            raise
    
    @staticmethod
    def _make_serializable(obj):
        """Convert non-serializable objects to serializable format."""
        if isinstance(obj, (set, tuple)):
            return list(obj)
        if isinstance(obj, dict):
            return {k: FileHandler._make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [FileHandler._make_serializable(item) for item in obj]
        return obj
    
    def list_available_files(self, pattern: str = "*.txt") -> List[str]:

        return [str(f) for f in self.base_path.glob(pattern)]