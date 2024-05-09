import json
import random
import spacy.cli
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

nlp = spacy.load("en_core_web_sm")

labels = []
sentences = []

intentions_path = "data/intentions.json"
sentences_path = "data/sentences.txt"

# this has not been put into a seperate file as implementation would be more complex
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'today', 'tomorrow', 'week']
verbs = ['going', 'visit', 'travel', 'go', 'choose', 'get', 'goes']
loc_types = ['GPE', 'ORG', 'LOC', 'NORP', 'PERSON']

chosen_intention = None

# Opening JSON file and return JSON object as a dictionary

with open(intentions_path) as f:
    intentions = json.load(f)

final_chatbot = False

# this function checks to see if the word may is in the text supplied as in some cases may can be used to indicate a date
def may_check(phrase):
    lower = phrase.lower()
    if "may" in lower:
        return True#

def clean_date(date):
    date = nlp(date)
    out = ""
    for token in date:
        if token.pos_ == "DET":
            continue
        else:
            out += token.text + " "
    return out.rstrip()

def clean_ord(ord):
    if "st" in ord:
        ord = ord.replace("st", "")
        return ord
    if "nd" in ord:
        ord = ord.replace("nd", "")
        return ord
    if "rd" in ord:
        ord = ord.replace("rd", "")
        return ord
    if "th" in ord:
        ord = ord.replace("th", "")
        return ord

def date_conversion(date):
    if date.lower() in weekdays:

        date = date.lower()

        todayindex = datetime.today().weekday()

        if date == "today":
            return datetime.today().strftime("%Y-%m-%d")
        if date == "tomorrow":
            date_out = datetime.today() + timedelta(days=1)
            return date_out.strftime("%Y-%m-%d")
        if date == "a week":
            date_out = datetime.today() + timedelta(days=7)
            return date_out.strftime("%Y-%m-%d")

        index = weekdays.index(date)
        today = datetime.today()
        if todayindex == index:
            date_out = datetime.today() + timedelta(days=7)
            return date_out.strftime("%Y-%m-%d")
        else:
            if today.weekday() < index:
                date_out = datetime.today() + timedelta(days=(index - todayindex))
                return date_out.strftime("%Y-%m-%d")
            else:
                date_out = datetime.today() + timedelta(days=7 - today.weekday() + index)
                return date_out.strftime("%Y-%m-%d")
    else:
        words = date.split()
        if "st" in words[0]:
            words[0] = words[0].replace("st", "")
        if "nd" in words[0]:
            words[0] = words[0].replace("nd", "")
        if "rd" in words[0]:
            words[0] = words[0].replace("rd", "")
        if "th" in words[0]:
            words[0] = words[0].replace("th", "")

        month = words[0] + " " + words[1] + " " + str(datetime.today().year)
        date = datetime.strptime(month, "%d %B %Y").strftime("%Y-%m-%d")

        if date < datetime.today().strftime("%Y-%m-%d"):
            return datetime.strptime(month, "%d %B %Y").replace(year=datetime.today().year + 1).strftime("%Y-%m-%d")
        else:
            return date

def time_conversion(time):

    time = time.replace(" ", "")

    if "afternoon" in str(time).lower():
        return datetime.strptime("15:00", "%H:%M").strftime("%H:%M")
    if "midnight" in str(time).lower():
        return datetime.strptime("00:00", "%H:%M").strftime("%H:%M")
    if "noon" in str(time).lower():
        return datetime.strptime("12:00", "%H:%M").strftime("%H:%M")
    if "morning" in str(time).lower():
        return datetime.strptime("09:00", "%H:%M").strftime("%H:%M")
    if "evening" in str(time).lower():
        return datetime.strptime("18:00", "%H:%M").strftime("%H:%M")
    if "am" in str(time).lower() or "pm" in str(time).lower():
        return datetime.strptime(time, "%I%p").strftime("%H:%M")
    if str(time).isdigit():
        return datetime.strptime(time, "%H%M").strftime("%H:%M")
    if ":" in str(time):
        return datetime.strptime(time, "%H:%M").strftime("%H:%M")

def check_intention_by_keyword(sentence):
    global chosen_intention
    for word in sentence.split():
        for type_of_intention in intentions:
            if word.lower() in intentions[type_of_intention]["patterns"]:

                print("BOT: " + random.choice(intentions[type_of_intention]["responses"]))
                if type_of_intention == 'book':
                    print("BOT: note, if you would like to start over, just type 'reset' and I will start selection again.")
                # Do not change these lines
                if type_of_intention == 'greeting' and final_chatbot:
                    print("BOT: I am built for helping you with your travel plans. You can ask me about the time, date, and train tickets.\n(Hint: What time is it?)")
                return type_of_intention
    return chosen_intention

def check_intention_by_keyword_nr(sentence):
    global chosen_intention
    for word in sentence.split():
        for type_of_intention in intentions:
            if word.lower() in intentions[type_of_intention]["patterns"]:
                return type_of_intention
    return None
def lemmatize_and_clean(text):
    doc = nlp(text.lower())
    out = ""
    for token in doc:
        if not token.is_stop and not token.is_punct:
            out = out + token.lemma_ + " "
    return out.strip()

time_sentences = ''
date_sentences = ''
with open(sentences_path) as file:
    for line in file:
        parts = line.split(' | ')
        if parts[0] == 'time':
            time_sentences = time_sentences + ' ' + parts[1].strip()
        elif parts[0] == 'date':
            date_sentences = date_sentences + ' ' + parts[1].strip()

labels = []
sentences = []

doc = nlp(time_sentences)
for sentence in doc.sents:
    labels.append("time")
    sentences.append(sentence.text.lower().strip())

doc = nlp(date_sentences)
for sentence in doc.sents:
    labels.append("date")
    sentences.append(sentence.text.lower().strip())

def date_time_response(user_input):
    cleaned_user_input = lemmatize_and_clean(user_input)
    doc_1 = nlp(cleaned_user_input)
    similarities = {}
    for idx, sentence in enumerate(sentences):
        cleaned_sentence = lemmatize_and_clean(sentence)
        doc_2 = nlp(cleaned_sentence)
        similarity = doc_1.similarity(doc_2)
        similarities[idx] = similarity

    max_similarity_idx = max(similarities, key=similarities.get)

    # Minimum acceptable similarity between user's input and our Chatbot data
    # This number can be changed
    min_similarity = 0.75

    # Do not change these lines
    if similarities[max_similarity_idx] > min_similarity:
        if labels[max_similarity_idx] == 'time':
            print("BOT: " + "It’s " + str(datetime.now().strftime('%H:%M:%S')))
            if final_chatbot:
                print("BOT: You can also ask me what the date is today. (Hint: What is the date today?)")
        elif labels[max_similarity_idx] == 'date':
            print("BOT: " + "It’s " + str(datetime.now().strftime('%Y-%m-%d')))
            if final_chatbot:
                print(
                    "BOT: Now can you tell me where you want to go? (Hints: you can type in a city's name, or an organisation. I am going to London or I want to visit the University of East Anglia.)")
        return True

    return False