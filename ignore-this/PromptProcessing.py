import ollama


# noinspection PyShadowingNames
def classify_prompt(prompt):
    # List of keywords that indicate a command for the control center
    control_keywords = [
        "reduce", "increase", "decrease", "volume", "brightness", "turn on", "turn off", "find", "search",
        "open", "close", "start", "stop"
    ]

    prompt_lower = prompt.lower()

    for keyword in control_keywords:
        if keyword in prompt_lower:
            return "control_center"

    return "ai_chatbot"


# noinspection PyShadowingNames
def process_log_file(log_file_path):
    try:
        with open(log_file_path, 'r') as file:
            prompt = file.read().strip()

        classification = classify_prompt(prompt)

        if classification == "control_center":

            print(f"Control Center: {prompt}")
            # Tasks for command center code
            # understand the context around the identified keyword
            # parse the command
            # execute the command

        else:
            response = ollama.generate(model='gemma2:2b', prompt=prompt)
            # might have to separate the prompt into chunks

            print(f"AI Chatbot: \n{response['response']}")

        return prompt, classification

    except FileNotFoundError:
        print(f"Error: The file {log_file_path} was not found.")
    except IOError:
        print(f"Error: There was an issue reading the file {log_file_path}.")


# Example usage
log_file_path = "log.txt"
prompt, classification = process_log_file(log_file_path)
print(f"Prompt: {prompt}")
print(f"Classification: {classification}")
