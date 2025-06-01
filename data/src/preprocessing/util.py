"""
Utility functions for preprocessing
"""


def remove_number(text):
    """
    Remove all "一、二、三、四、五、六、七、八、九、十" from the end of the text
    """
    if not text:
        return text
    text = text.strip()
    if text[-1] in ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']:
        text = text[:-1]
        text = remove_number(text)
    return text
