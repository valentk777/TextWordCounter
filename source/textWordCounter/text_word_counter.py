import operator
from collections import Counter
from pathlib import Path
from typing import List, Dict

from source.services.excel_service import ExcelService
from source.services.file_service import FileService
from source.services.pdf_service import PdfService
from source.services.text_cleaning_service import TextCleaningService
from source.services.txt_service import TxtService


class TextWordCounter:
    def get_words_count_and_save_to_excel(self,
                                          file_path: str,
                                          excel_file_path: str,
                                          language: str = "en",
                                          words_to_remove_file_path: str = None) -> None:
        print("get_words_count_and_save_to_excel - started")

        data = self.get_words_count(file_path, language, words_to_remove_file_path)
        sheet_name = file_path.split("/")[-1]

        ExcelService.write(data, excel_file_path, sheet_name)

    def get_words_count(self,
                        file_path: str,
                        language: str = "en",
                        words_to_remove_file_path: str = None) -> Dict[str, int]:
        print("get_words_count - started")

        file_service = self._get_file_service(file_path)
        data = file_service.read(file_path)
        data = TextCleaningService.remove_punctuations(data)
        data = TextCleaningService.remove_digits(data)
        data = TextCleaningService.remove_single_letters(data)
        data = self._get_list_of_words_from_string(data)
        data = TextCleaningService.clean_stopword(data, language)
        data = self._get_count_of_words(data)
        data = TextCleaningService.clean_custom_word(data, words_to_remove_file_path)

        return data

    def _get_file_service(self, file_path: str) -> FileService or Exception:
        print("get_file_reader - started")
        suffix = Path(file_path).suffix

        if suffix == ".pdf":
            return PdfService

        if suffix == ".txt":
            return TxtService

        raise Exception(f"File extension {suffix} is not supported")

    def _get_list_of_words_from_string(self, text: str) -> List[str]:
        print("get_list_of_word_from_string - started")

        list_of_words = text.lower().split()

        print(f"number of words in a book: {len(list_of_words)}")

        return text.lower().split()

    def _get_count_of_words(self, text: List[str]) -> Dict[str, int]:
        print("get_count_of_words - started")

        words_by_count = Counter(text)
        words_by_count = dict(sorted(words_by_count.items(), key=operator.itemgetter(1), reverse=True))

        return words_by_count