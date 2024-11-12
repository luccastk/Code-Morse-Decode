from pydub import AudioSegment
from pydub.silence import detect_nonsilent

MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '/': ' ',
}

def process_audio_to_morse(audio_file):
    audio = AudioSegment.from_file(audio_file, format="wav")
    
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=50, silence_thresh=-30)
    
    morse_code = []
    for i, (start, end) in enumerate(nonsilent_ranges):
        duration = end - start
        
        if duration < 100:
            morse_code.append('.')
        else:
            morse_code.append('-')
        
        if i < len(nonsilent_ranges) - 1:
            silence_duration = nonsilent_ranges[i + 1][0] - end
            if silence_duration > 400:
                morse_code.append('/')
            elif silence_duration > 100:
                morse_code.append(' ')
    
    return ''.join(morse_code)

def decode_morse_to_text(morse_code):
    words = morse_code.split('/')
    
    decoded_message = []
    
    for word in words:
        decoded_word = ''.join(MORSE_CODE_DICT.get(symbol, '?') for symbol in word.split())
        decoded_message.append(decoded_word)
    
    return ' '.join(decoded_message)


audio_path = 'musica.wav'
morse = process_audio_to_morse(audio_path)

decoded_text = decode_morse_to_text(morse)
print("Texto Decodificado:", decoded_text)
