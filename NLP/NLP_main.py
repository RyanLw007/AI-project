from NLP_booking import *
import requests
import json

llama_url = "http://localhost:11434/api/chat"

def llama3_response(user_input):
    data = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "stream": False
    }

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(llama_url, headers=headers, json=data)

    return (response.json()['message']['content'])




if __name__ == "__main__":

    final_chatbot = True

    flag = True

    print("BOT: Hi there! How can I help you?.\n (If you want to exit, just type bye!)")

    while (flag == True):

        user_input = input()
        with open('data/past_inputs.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_input])

        if user_input == "reset":
            chosen_origin_str = "Norwich"
            chosen_dest_str = None
            arrive_date_str = None
            arrive_time_str = None
            leave_date_str = None
            leave_time_str = None
            ticket_type = None
            leave_arrive = None
            chosen_intention = None
            print("BOT: I have reset the selection. start by telling me your ticket type.")
            continue

        chosen_intention = check_intention_by_keyword(user_input)

        if chosen_intention == 'goodbye':
            goodbye_response()
            flag = False
            # change intention for different responses (prediction etc)

            # if one way ticket I only need destination, date and time
            # if round ticket I need destination, date and time arriving and date and time leaving
            # if open ticket I need destination and date no extra info is needed
            # if open return ticket I need destination and date arriving and date leaving no extra info is needed

        if chosen_intention == 'book':
            if not ner_response(user_input):
                if not date_time_response(user_input):
                    if not expert_response(user_input):
                        if not ner_response(user_input):
                            if check_intention_by_keyword_nr(user_input) != "book":
                                print("BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                                print(f"\033[32mBOT: {llama3_response(user_input)}")
                                print(f"\n \033[0m")
        if chosen_intention == None:
            if not ner_response(user_input):
                if not date_time_response(user_input):
                    if not expert_response(user_input):
                        if not ner_response(user_input):
                            print("BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                            print(f"\033[32mBOT: {llama3_response(user_input)}")
                            print(f"\n \033[0m")

        if chosen_intention == 'greeting':
            chosen_intention = None
            if not ner_response(user_input):
                if not date_time_response(user_input):
                    if not expert_response(user_input):
                        if not ner_response(user_input):
                            continue

        if chosen_intention != 'goodbye' and chosen_intention != 'book' and chosen_intention != None and chosen_intention != 'greeting':
            if not date_time_response(user_input):
                if not expert_response(user_input):
                    if not ner_response(user_input):
                        print("BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                        print(f"\033[32mBOT: {llama3_response(user_input)}")
                        print(f"\n \033[0m")