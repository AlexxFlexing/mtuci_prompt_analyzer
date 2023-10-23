def format_the_output(string):
    string = string.split("[/INST]")[1]
    string = string[:-4]
    words = string.split()  # сплитим
    new_string = ""
    count = 0
    for word in words:
        if count + len(word) > 60:
            new_string += '\n'  #новый лайн
            count = 0
        new_string += word + ' '
        count += len(word) + 1
    return new_string.strip()
