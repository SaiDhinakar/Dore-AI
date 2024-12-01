import settings
from datetime import datetime
import re


user_settings = settings.User()
data = user_settings.load_data()
username = data['username']

def check_predefined_responses(user_message):
    responses = {
        # Common Greetings
        ("hello", "hi","hii" ,"hey", "greetings", "what's up", "howdy"): "Hello! How can I assist you today?",
        ("good morning", "morning", "morning sunshine", "rise and shine"): "Good morning! Hope you have a great day ahead.",
        ("good evening", "evening", "good night", "night", "nighty night"): "Good evening! How's your day going?",
        ("good night", "night", "sleep well", "sweet dreams"): "Good night! Sleep well.",
        
        # Asking about the bot
        ("who are you", "what are you", "tell me about yourself", "introduce yourself"): "I'm Dore, your friendly AI assistant. How can I help you?",
        ("what's your name", "what is your name", "who should I call you"): "My name is Dore. I'm here to assist you!",
        
        ("who am i", "what am i", "tell me who I am", "can you identify me"): f"You're {username}, and user of Dore, the AI assistant.",

        # Asking about developers
        ("who developed you", "who are the developers", "who made you", "who created you", "who's behind you"): 
            "I was developed by Spidey and Drackko, two passionate developers who built me to help you.",
        ("who are the developers", "tell me about the developers", "who's your creator"): 
            "Spidey and Drackko are the amazing developers behind Dore.",
        ("are you open-source", "is this open source", "can I see your code"): 
            "Yes! The project is open-source. You can find the code on GitHub. Feel free to contribute!",
        ("where can I find the source code", "source code location", "where's your code hosted"): 
            "You can find the source code on GitHub. Just search for 'Dore AI' and you'll find the repository.",
        
        # Date and Time
        ("what time is it", "what's the time", "current time", "what is the time now", "tell me the time"): f"The current time is: {datetime.now().strftime('%I %M %p')}",
        ("what's the date", "what is the date", "current date", "today's date", "can you tell me the date"): f'Today is: {datetime.now().strftime("%B %d %A")}',
        
        # Help
        ("can you help me", "i need help", "I require assistance", "help me out"): "Of course! What do you need help with?",
        ("how do you work", "how do you do that", "explain your process"): "I use artificial intelligence to understand and respond to your messages.",
        
        # Farewells
        ("goodbye", "bye", "see you", "later", "take care"): "Goodbye! Have a wonderful day!",
        
        # Asking for AI capabilities
        ("can you do something", "what can you do", "tell me your capabilities", "what are your features"): 
            "I can chat with you, answer questions, tell jokes, and more. Just ask me anything!",
        
        # Weather (You can expand with actual API integration for weather)
        ("what's the weather", "how's the weather", "tell me about the weather", "is it raining"): "I don't know the weather right now, but I can help you check it online!",
        
        # Miscellaneous
        ("thank you", "thanks", "appreciate it", "thank you very much"): "You're welcome! Let me know if you need anything else.",
        ("sorry", "apologies", "my bad", "excuse me"): "No worries at all! How can I assist you further?",
        ("yes", "no", "affirmative", "negative"): "Okay, noted!",
        
        # Asking about AI and tech
        ("what is AI", "what is artificial intelligence", "define AI", "explain artificial intelligence"): 
            "AI stands for Artificial Intelligence, a field of computer science that aims to create machines capable of intelligent behavior.",
        ("who invented AI", "who created artificial intelligence", "who are the pioneers of AI"): 
            "Artificial Intelligence was pioneered by many great minds, including Alan Turing, John McCarthy, and others in the 1950s.",
        
        # Tech and Science
        ("what is machine learning", "define machine learning", "explain machine learning", "tell me about machine learning"): 
            "Machine Learning is a subset of AI that enables computers to learn and make decisions from data, without being explicitly programmed.",
        ("what is deep learning", "define deep learning", "explain deep learning", "tell me about deep learning"): 
            "Deep learning is a subset of machine learning that uses neural networks with many layers to analyze and learn from large amounts of data.",
        
        # Software Development
        ("who are Spidey and Drackko", "tell me about Spidey and Drackko", "who created this AI"): 
            "Spidey and Drackko are the developers behind this AI chatbot.",
        ("what technologies do you use", "what tech is behind you", "what's your tech stack"): 
            "I use technologies like Python, PyQt, NLP, and machine learning models to understand and respond to you.",
        
        # AI knowledge and limitations
        ("are you perfect", "do you make mistakes", "can you be wrong"): 
            "I'm not perfect, but I’m always learning and improving. If I make a mistake, feel free to correct me!",
        ("can you learn new things", "do you keep improving", "are you adaptable"): 
            "Yes! I continuously learn and adapt to become better at assisting you with your questions and tasks.",
    }

    # Normalize the input message to handle case insensitivity and punctuation variations
    user_message_lower = user_message.strip().lower()

    # Check if any predefined response matches the normalized input
    for keys, response in responses.items():
        if any(re.search(r'\b' + re.escape(key.lower()) + r'\b', user_message_lower) for key in keys):
            return response

    return None  # If no match, return None so the message will be sent to the AI model
