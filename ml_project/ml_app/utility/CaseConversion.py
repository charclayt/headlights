def to_pascal(string: str):
    string = string.replace("_", " ")
    string = ''.join(word[0].upper() + word[1:] for word in string.split())
    return string.replace(" ", "")
    
