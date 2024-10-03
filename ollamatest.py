import ollama
prompt = "Hello, this is Santiago."
response = ollama.generate(model='gemma2:2b', prompt=prompt)
