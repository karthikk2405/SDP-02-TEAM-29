def english_to_telugu(text):
    # Define a basic mapping for demonstration
    mapping = {
        'a': 'ఎ',
        'b': 'బి',
        'c': 'సి',
        'd': 'డి',
        'e': 'ఇ',
        'f': 'ఎఫ్',
        'g': 'జి',
        'h': 'హేచ్',
        'i': 'ఐ',
        'j': 'జే',
        'k': 'కే',
        'l': 'ఎల్',
        'm': 'ఎం',
        'n': 'ఎన్',
        'o': 'ఓ',
        'p': 'పి',
        'q': 'క్యూ',
        'r': 'ఆర్',
        's': 'ఎస్',
        't': 'టి',
        'u': 'యూ',
        'v': 'వి',
        'w': 'డబల్యూ',
        'x': 'ఎక్స్',
        'y': 'వై',
        'z': 'జెడ్'
    }

    telugu_text = ''.join(mapping.get(char.lower(), char) for char in text)

    return telugu_text

# Example usage
english_text = "Hello, how are you?"
telugu_result = english_to_telugu(english_text)
print(telugu_result)
