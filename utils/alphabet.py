import os
import unicodedata

def translate_char(c):
    mapping = {
        "⸗": "-",
        "|": "|",
        "§": "§",
        "/": "",
        chr(768): "",
        "&": "&",
        "¬": "-",
        "ו": "@",
        "פ": "@",
        "נ": "@",
        "ק": "@",
        "ס": "@",
        "ב": "@",
        "א": "@",
        "ר": "@",
        "מ": "@",
        "י": "@",
        "ש": "@",
        "כ": "@",
        "ה": "@",
        "ז": "@",
        "ἐ": "@",
        "ν": "@",
        "ώ": "@",
        "ῶ": "@",
        "ι": "@",
        "ο": "@",
        "τ": "@",
        "ȣ": "@",
        chr(771): "",
        "π": "@",
        "α": "@",
        "ρ": "@",
        "ὸ": "@",
        "ς": "@",
        "ꝛ": "@",
        "ῤ": "@",
        "ῥ": "@",
        "η": "@",
        "σ": "@",
        "κ": "@",
        chr(11850): "",
        "æ": "@",
        "ό": "@",
        "ת": "@",
        "ח": "@",
        "ẽ": "@",
        "à": "@",
        "é": "e",
        "è": "e",
        "ꝫ": "@",
        "ò": "o",
        "ú": "u",
        chr(834): "",
        chr(769): "",
        "ę": "e",
        chr(361): "ü",
        chr(245): "ö",
        chr(182): chr(182),
        chr(227): "ä",
        chr(42841): "@",
        "⁊": "@",
        "’": "'",
        chr(367): "",
        chr(92): chr(92),
        chr(241): "n",
        chr(870): chr(776),
        "œ": "ö",
        "γ": "@",
        "γ": "@",
        "θ": "@",
        "ε": "@",
        "υ": "@",
        "Γ": "@",
        "Σ": "@",
        "ό": "@",
        "♂": "@",
        "♀": "@",
        "♃": "@",
        "♄": "@",
        "☽": "@",
        "☿": "@",
        "☉": "@",
        "▽": "@",
        "_": "@",
        "℞": "@",
        "Æ": "@",
        chr(59583): "@",
        "ꝰ": "@",
        "ꝓ": "@",
        "ꝑ": "@",
        "ē": "e",
        "ū": "u",
        "ë": "e",
        "ϧ": "@",
        "έ": "@",
        chr(772): "",
        chr(808): "",
        "ŋ": "@",
        chr(776): chr(776),
        chr(519): "e",
        "”": '"',
        "∙": "@",
        "∘": "@",
        chr(8218): ",",
        "°": "°",
        "«": "„",
        "»": "“",
        chr(946): "@",
        chr(8211): "-",
        "ê": "e",
        chr(8223): '"',
        chr(8216): "'",
        chr(236): "i",
        "Ä": "Ä",
        "Ü": "Ü",
        "Ö": "Ö",
        "½": "@",
        "⅙": "@",
        "⅔": "@",
        "¾": "@",
        "¼": "@",
        chr(244): "o",
        "=": "-",
        "⏑": "@",
        "⏓": "@",
        "û": "u",
        chr(8219): "'",
        "â": "a",
        "ἑ": "@",
        "ω": "@",
        chr(837): "",
        "ϱ": "@",
        "ῆ": "@",
        "Ἀ": "A",
        "φ": "@",
        "δ": "@",
        "ί": "i",
        "ï": "i",
        "î": "i",
        "ἀ": "@",
        "μ": "@",
        "ϰ": "@",
        "№": "@",
        "λ": "@",
        "ὀ": "o",
        chr(8125): "'",
        "ϑ": "@",
        chr(855): "",
        "χ": "@",
        "ἰ": "i",
        "ù": "u",
        "†": "@",
        "É": "E",
        "[": "[",
        "]": "]",
        "á": "a",
        "ř": "r",
        "Ἰ": "I",
        "ά": "@",
        "Β": "B",
        "έ": "@",
        "ἄ": "@",
        "є": "@",
        "ó": "o",
        "ξ": "@",
        "ὐ": "@",
        chr(932): "T",
        "ϋ": "@",
        "ℳ": "M",
        "Ç": "Ç"
    }
    return mapping[c] if c in mapping else c