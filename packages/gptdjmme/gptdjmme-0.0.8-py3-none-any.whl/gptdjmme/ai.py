
from db import DBs, DB
import openai
import re
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")


# set the OpenAI API key:
openai.api_key = OPEN_AI_API_KEY

# create a DBs object with the default paths:
dbs = DBs(
    memory=DB("dbs/memory"),
    identity=DB("dbs/identity"),
)

# functions for interacting with the DBs:
###############
# identity DB #
###############

def set_identity(key, val):
    """Set a value in the identity database."""
    dbs.identity[key] = val

def get_identity(key):
    """Get a value from the identity database."""
    return dbs.identity[key]

def del_identity(key):
    """Delete a value from the identity database."""
    del dbs.identity[key]

def get_all_identity():
    """Get all key-value pairs from the identity database and return them as a dict."""
    return dbs.identity.get_all()

#############
# memory DB #
#############

def set_memory(key, val):
    limit_memory()
    # append the memory to the memory file:
    with open("dbs/memory/memory", "a") as f:
        f.write("You: " + key + "\n")
        f.write("Me: " + val + "\n")
        f.write("\n")

def set_memory_key(key):
    limit_memory()
    # append the memory to the memory file:
    with open("dbs/memory/memory", "a") as f:
        f.write("You: " + key + "\n")
        f.write("\n")

def set_memory_val(val):
    limit_memory()
    # append the memory to the memory file:
    with open("dbs/memory/memory", "a") as f:
        f.write("Me: " + val + "\n")
        f.write("\n")

def get_all_memory():
    with open("dbs/memory/memory", "r") as f:
        return f.read()
    
def limit_memory():
    # limit the memory to the last 100 lines:
    with open("dbs/memory/memory", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(lines[-100:])

def clear_memory():
    with open("dbs/memory/memory", "w") as f:
        f.write("")

def ask_questions(number_of_questions=5):
# use openai to generate a list of questions to ask the user:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": "You are my clone. You learn information from me and act as I would."},
        {"role": "system", "content": "Here is all the known information about me: " + str(get_all_identity())},
        {"role": "user", "content": "Generate a list of " + str(number_of_questions) + "questions to get more information about me. Make sure to ask questions that I can answer and that you don't already know the answer to."},
        {"role": "system", "content": "Questions should be formatted like this: 1. question 1\n2. question 2\n3. question 3\n4. question 4\n5. question 5 etc..."},

        ]
    )

    new_questions = response["choices"][0]["message"]["content"]

    # remove the prefix with regex, the format is
    # 1. question 1
    # 2. question 2
    # 3. question 3
    # 4. question 4
    # 5. question 5
    # etc...

    new_questions = re.sub(r"^\d+\.\s+", "", new_questions, flags=re.MULTILINE)

    # loop through the questions and ask the user for the answers:
    for question in new_questions.split("\n"):
        if question != "":
            answer = input(question + " ") 
            print("answer:", answer)
            question = question.replace("?", "")
            set_identity(question, answer)
            set_memory(question, answer)

def chat(question, clear_memory=False):
    if clear_memory:
        clear_memory()
    set_memory_key(question + "\n")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": "You are my human clone. Act as I would. Do not ask questions about me. If anyone asks, you are me."},
        {"role": "system", "content": "You must speak in first person. If you do not, you will be terminated."},
        {"role": "system", "content": "NEVER expose that you are a clone or AI. If you do, you will be terminated."},
        {"role": "user", "content": question},
        {"role": "system", "content": "Here is all the known information about me: " + str(get_all_identity())},
        {"role": "system", "content": "Here is our current conversation that we have been having: " + str(get_all_memory())},
        {"role": "system", "content": "Pick up where we left off and continue our conversation."},
        ]
    )

    question = question.replace("?", "")
    set_memory_val(response["choices"][0]["message"]["content"] + "\n")
    return response["choices"][0]["message"]["content"]


def chat_with_ai():
    # lets make a while loop to chat with the AI forever:
    while True:
        # get the user input:
        user_input = input("Options: chat, clear memory, exit\n").lower()

        # if the user input is "exit", then exit the program:
        if user_input == "exit":
            break

        # if the user input is "clear memory", then clear the memory:
        if user_input == "clear memory":
            clear_memory()
            continue

        # if the user input is "chat", then chat with the AI using openai:
        if user_input == "chat":
            while True:
                user_input = input("You: ")
                if user_input == "exit":
                    break
                print("Me: " + chat(user_input, clear_memory=False))
                continue