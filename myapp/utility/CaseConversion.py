def to_pascal(string: str):
    string = string.replace("_", " ")
    string = ''.join(word[0].upper() + word[1:] for word in string.split())
    return string.replace(" ", "")

def to_snake(string: str):
    string = to_pascal(string)
    return ''.join(['_'+char.lower() if char.isupper() else char for char in string]).lstrip('_')