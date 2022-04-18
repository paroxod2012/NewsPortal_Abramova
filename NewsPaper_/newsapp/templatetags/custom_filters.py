from django import template

register = template.Library()

incorrect_words = ['stupid', 'bastard', 'fool', 'idiot']

@register.filter()

def censor(value):

        low_value = value.lower()
        end_pos = len(value)
        for word in incorrect_words:
            start_pos = 0
            word_len = len(word)
            while start_pos < end_pos - word_len:
                position = low_value.find(word, start_pos, end_pos)
                if position == -1:
                    break
                else:
                    value = value.replace(word[1::], '*' * word_len)
                    start_pos += position + word_len
        return f'{value}'













