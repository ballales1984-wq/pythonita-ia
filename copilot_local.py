import ollama

def chiedi_a_llama3(frase):
    risposta = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': frase}
    ])
    return risposta['message']['content'].strip()
