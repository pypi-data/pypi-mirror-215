from typing import List

class BaseParse:
    def _search(self, text) -> List:
        return [(num, string) for num, string in enumerate(self.code_strings) if text in string]
