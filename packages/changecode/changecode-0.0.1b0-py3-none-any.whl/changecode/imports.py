from typing import List

class ImportsParse:
    """ 
    Импорты всегда должны находиться в начале кода и должны быть разделены 
    по пакетам или по назначению 1 строкой
    """
    def __init__(self, code_strings: List[str]) -> None:
        self.code_strings = code_strings
