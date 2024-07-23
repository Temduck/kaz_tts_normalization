import re
from num2words import num2words
from kazakh_language_data import ORDINAL_DICT, ORDINAL_SUFFIX, GROUP_SUFFIX
from kazakh_language_data import MONTHS, ALPHABET

class KazakhNumeralConverter:
    def __init__(self):
        self.ordinal_num_suffixs = ORDINAL_SUFFIX.split("|")
        self.group_num_suffixs = GROUP_SUFFIX.split("|")

    def num2words_get_ordinal(self, num):
        # Convert number to ordinal form based on predefined mappings
        words = num2words(num, lang="kz").rsplit(" ", 1)
        words[-1] = ORDINAL_DICT.get(words[-1], words[-1])
        return " ".join(words)

    def replace_npw(self, match):
        # Replace number-word pairs like months or years with their word equivalents
        num, word = match.group().split()
        return "{} {}".format(self.num2words_get_ordinal(num), word)

    def replace_n(self, match):
        # Convert standalone numbers into words
        return num2words(match.group(), lang="kz")

    def remove_n(self, match):
        # Remove digits from concatenated digit-letter combinations
        return re.sub('\d', '', match.group())

    def replace_s(self, match):
        # Replace num with suffix match
        num, suffix = match.group().split("-")
        if suffix in self.ordinal_num_suffixs:
            return self.num2words_get_ordinal(num)
        if suffix in self.group_num_suffixs:
            return num2words(num, lang="kz") + suffix



if __name__=="__main__":
    # Example usage:
    converter = KazakhNumeralConverter()

    # Example regex matches to test the methods
    match_npw = re.match(r'\b(\d+)\s(\w+)', '3 наурыз')
    match_n = re.match(r'\b\d+\b', '5')
    match_remove_n = re.match(r'\w+\d+', 'example123')
    match_replace_s = re.match(r'\d+-\w+', '5-ші')

    print(converter.replace_npw(match_npw))   # Output: "үшінші наурыз"
    print(converter.replace_n(match_n))       # Output: "бес"
    print(converter.remove_n(match_remove_n)) # Output: "example"
    print(converter.replace_s(match_replace_s))  # Output: "бесінші"

    # List of compiled regex patterns and replacement functions
    _numerals = [
        (re.compile(rf"\b(3[01]|[12][0-9]|[1-9])\s({MONTHS})"), converter.replace_npw),
        (re.compile(r"\b\d{4}\sжыл"), converter.replace_npw),
        (re.compile(rf"\d+-({ORDINAL_SUFFIX})"), converter.replace_s),
        (re.compile(rf"\d+-({GROUP_SUFFIX})"), converter.replace_s),
        (re.compile(rf"[{ALPHABET}]+\d+"), converter.remove_n),
        (re.compile(rf"\d+[{ALPHABET}]+"), converter.remove_n),
        (re.compile(r"\b\d{1,3}\b"), converter.replace_n),
    ]

    def has_numbers(inputString):
        return bool(re.search(r'\d', inputString))

    def expand_numbers(text):
        for regex, replacement_func in _numerals:
            if not has_numbers(text): break
            text = regex.sub(replacement_func, text)
        return text

    example_text = "3 наурыз 2023 жыл 5-ші 30 қарашада"
    expanded_text = expand_numbers(example_text)
    print(expanded_text)