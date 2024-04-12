import json
import random
import spacy.cli
import requests
from datetime import datetime, timedelta
from datetime import datetime
from bs4 import BeautifulSoup
from difflib import get_close_matches, SequenceMatcher
from experta import *

intentions_path = "data/intentions.json"
sentences_path = "data/sentences.txt"

weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'today', 'tomorrow', 'a week']

chosen_dest = []
chosen_date = None
chosen_time = []
chosen_time_str = None

# Opening JSON file and return JSON object as a dictionary

with open(intentions_path) as f:
    intentions = json.load(f)

final_chatbot = False

def date_conversion(weekday):

    if weekday == "today":
        return datetime.today()
    if weekday == "tomorrow":
        return datetime.today() + timedelta(days=1)
    if weekday == "a week":
        return datetime.today() + timedelta(days=7)

    index = weekdays.index(weekday)
    today = datetime.today()
    todayindex = today.weekday()
    if todayindex == index:
        return datetime.today() + timedelta(days=7)
    else :
        if today.weekday() < index:
            return datetime.today() + timedelta(days=(index - todayindex))
        else :
            return datetime.today() + timedelta(days=7 - today.weekday() + index)

def time_conversion(time):

    if "afternoon" in str(time).lower():
        return datetime.strptime("12:00", "%H:%M").strftime("%H:%M")
    if "midnight" in str(time).lower():
        return datetime.strptime("00:00", "%H:%M").strftime("%H:%M")
    if "noon" in str(time).lower():
        return datetime.strptime("15:00", "%H:%M").strftime("%H:%M")
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
    for word in sentence.split():
        for type_of_intention in intentions:
            if word.lower() in intentions[type_of_intention]["patterns"]:
                print("BOT: " + random.choice(intentions[type_of_intention]["responses"]))

                # Do not change these lines
                if type_of_intention == 'greeting' and final_chatbot:
                    print("BOT: We can talk about the time, date, and train tickets.\n(Hint: What time is it?)")
                return type_of_intention
    return None

def lemmatize_and_clean(text):
    doc = nlp(text.lower())
    out = ""
    for token in doc:
        if not token.is_stop and not token.is_punct:
            out = out + token.lemma_ + " "
    return out.strip()

nlp = spacy.load("en_core_web_sm")

labels = []
sentences = []

url = "https://www.4icu.org/gb/a-z/"
content = requests.get(url)
soup = BeautifulSoup(content.text, 'html.parser')

universities = {}
for tr in soup.find_all('tr')[2:]:
    tds = tr.find_all('td')
    if len(tds) == 3:
        university = {}
        university['Rank'] = tds[0].text
        university['Name'] = tds[1].text
        university['City'] = tds[2].text.replace(' ...', '')
        universities[tds[1].text] = university



def get_best_match_university(user_input):
    university_list = universities.keys()
    matches = get_close_matches(user_input, university_list, n=1, cutoff=0.6)
    if len(matches) > 0:
        best_match = matches[0]
    else:
        return None

    sm = SequenceMatcher(None, user_input, best_match)
    score = sm.ratio()
    if score >= 0.6:
        return best_match
    else:
        return None


def ner_response(user_input):
    doc = nlp(user_input)
    global chosen_dest
    global chosen_date
    global chosen_time
    global chosen_time_str

    for token in doc:
        if token.pos_ == "VERB":
            choose = False
            if token.text.lower() == "going":
                choose = True
            if token.text.lower() == "visit":
                choose = True
            if token.text.lower() == "travel":
                choose = True
            if token.text.lower() == "go":
                choose = True
            if token.text.lower() == "choose":
                choose = True
            if choose:
                if any(doc.ents):
                    for ent in doc.ents:
                        if ent.label_ == "GPE":
                            chosen_dest.append(ent.text)
                        if ent.label_ == "ORG":
                            chosen_dest.append(ent.text)
                        if ent.label_ == "DATE":
                            doc = nlp(ent.text)
                            for check in doc:
                                if check.pos_ != "DET":
                                    if ent.text.lower() in weekdays:
                                        chosen_date = date_conversion(ent.text.lower())
                                        print("BOT: " + "I understand that you want travel on " + chosen_date.strftime("%Y-%m-%d") + ".")
                                    else:
                                        print("BOT: " + "I understand that you want travel on " + ent.text + ".")
                        if ent.label_ == "TIME":
                            chosen_time.append(ent.text)
                    if chosen_time != []:
                        chosen_time_str = " ".join(chosen_time)
                        chosen_time_str = time_conversion(chosen_time_str)
                        print("BOT: " + "You want to travel at " + chosen_time_str + ".")
                    if chosen_dest != []:
                        print("BOT: " + "You want to go to " + "".join(chosen_dest) + ".")
                    if chosen_dest != None and chosen_date != None and chosen_time != []:
                        print("BOT: " + "I understand that you want to go to " + "".join(chosen_dest) + " on " + chosen_date.strftime("%Y-%m-%d") + " at " + chosen_time_str + ".")
                    if chosen_dest == None:
                        print("BOT: " + "I am sorry I don't understand where you want to go.")
                    if chosen_date == None:
                        print("BOT: " + "I am sorry I don't understand when you want to go.")
                    if chosen_time == []:
                        print("BOT: " + "I am sorry I don't understand when you want to go.")
                    if final_chatbot:
                        print("BOT: Could you please tell me what kind of ticket you are looking for? (You can just ask for one way, round and open return tickets.)")
                    return True

    return False


def date_time_response(user_input):
    cleaned_user_input = lemmatize_and_clean(user_input)
    doc_1 = nlp(cleaned_user_input)
    similarities = {}
    for idx, sentence in enumerate(sentences):
        cleaned_sentence = lemmatize_and_clean(sentence)
        doc_2 = nlp(cleaned_sentence)
        similarity = doc_1.similarity(doc_2)
        similarities[idx] = similarity

    try:
        max_similarity_idx = max(similarities, key=similarities.get)
    except ValueError:
        return False


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


class Book(Fact):
    """Info about the booking ticket."""
    pass

class TrainBot(KnowledgeEngine):
  @Rule(Book(ticket='one way'))
  def one_way(self):
    print("BOT: You have selected a one way ticket. Have a good trip.")
    if final_chatbot:
      print("BOT: If you don't have any other questions you can type bye.")

  @Rule(Book(ticket='round'))
  def round_way(self):
    print("BOT: You have selected a round ticket. Have a good trip.")
    if final_chatbot:
      print("BOT: If you don't have any other questions you can type bye.")

  @Rule(AS.ticket << Book(ticket=L('open ticket') | L('open return')))
  def open_ticket(self, ticket):
    print("BOT: You have selected a " + ticket["ticket"] +".  Have a good trip.")
    if final_chatbot:
      print("BOT: If you don't have any other questions you can type bye.")


# engine = TrainBot()
# engine.reset()
# engine.declare(Book(ticket=choice(['one way', 'round', 'open ticket', 'open return'])))
# engine.run()

def check_ticket(user_input):
    user_input = user_input.lower()
    ticket_list = ['one way', 'round', 'open ticket', 'open return']

    for ticket in ticket_list:
        if ticket in user_input:
            return ticket_list[ticket_list.index(ticket)]

    return None
def expert_response(user_input):
    engine = TrainBot()
    engine.reset()
    ticket = check_ticket(user_input)
    if ticket != None:
        engine.declare(Book(ticket=ticket))
        engine.run()
        return True

    return False

final_chatbot = True
flag=True
print("BOT: Hi there! How can I help you?.\n (If you want to exit, just type bye!)")
while(flag==True):
    user_input = input()
    intention = check_intention_by_keyword(user_input)
    if intention == 'goodbye':
        if chosen_dest != None and chosen_date != None and chosen_time != []:
            print("location: " + "".join(chosen_dest) + " Date: " + str(chosen_date.strftime("%Y-%m-%d")) + " Time: " + chosen_time_str)
        if chosen_dest == None:
            print("BOT: No city chosen")
        if chosen_date == None:
            print("BOT: No date chosen")
        if chosen_time == []:
            print("BOT: No time chosen")
        flag=False
    elif intention == None:
        if not ner_response(user_input):
            #if not date_time_response(user_input):
                if not expert_response(user_input):
                    if not ner_response(user_input):
                        print("BOT: Sorry I don't understand that. Please rephrase your statement.")

