from NLP_booking import *
import requests
import csv
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

    global printout

    final_chatbot = True

    flag = True


    printout.append("BOT: Hi there! How can I help you?.\n (If you want to exit, just type bye!")
    print_out()

    while (flag == True):
        printout.clear()

        user_input = input()
        with open('data/past_inputs.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_input])

        if user_input == "reset":
            with open('data/reset.json', 'r') as reset:
                default = json.load(reset)

            with open('data/data.json', 'w') as file:
                json.dump(default, file, indent=4)
            printout.append("BOT: I have reset the selection. start by telling me your ticket type.")
            print_out()
            printout.clear()
            continue

        data['chosen_intention'] = check_intention_by_keyword(user_input)
        with open('data/data.json', 'w') as file:
            json.dump(data, file, indent=4)

        if printout[0]:
            printout.pop(0)
            print_out()
            printout.clear()
        else:
            printout.pop(0)


        if data['chosen_intention'] == 'goodbye':
            goodbye_response()
            print_out()
            printout.clear()

            with open('data/reset.json', 'r') as reset:
                default = json.load(reset)

            with open('data/data.json', 'w') as file:
                    json.dump(default, file, indent=4)

            flag = False
            # change intention for different responses (prediction etc)

            # if one way ticket I only need destination, date and time
            # if round ticket I need destination, date and time arriving and date and time leaving
            # if open ticket I need destination and date no extra info is needed
            # if open return ticket I need destination and date arriving and date leaving no extra info is needed

        if data['chosen_intention'] == 'book':
            ner_response(user_input)
            if printout[0]:
                printout.pop(0)
                print_out()
            else:
                printout.pop(0)
                date_time_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    print_out()
                else:
                    printout.pop(0)
                    expert_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        print_out()
                    else:
                        printout.pop(0)
                        ner_response(user_input)
                        if printout[0]:
                            printout.pop(0)
                            print_out()
                        else:
                            printout.pop(0)
                            if check_intention_by_keyword_nr(user_input) != "book":
                                printout.append("BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                                printout.append(f"BOT: {llama3_response(user_input)}")
                                print_out()
        if data['chosen_intention'] == None:
            ner_response(user_input)
            if printout[0]:
                printout.pop(0)
                print_out()
            else:
                printout.pop(0)
                date_time_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    print_out()
                else:
                    printout.pop(0)
                    expert_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        print_out()
                    else:
                        printout.pop(0)
                        ner_response(user_input)
                        if printout[0]:
                            printout.pop(0)
                            print_out()
                        else:
                            printout.pop(0)
                            if check_intention_by_keyword_nr(user_input) != "book":
                                printout.append(
                                    "BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                                printout.append(f"BOT: {llama3_response(user_input)}")
                                print_out()


        if data['chosen_intention'] == 'greeting':
            data['chosen_intention'] = None
            ner_response(user_input)
            if printout[0]:
                printout.pop(0)
                print_out()
            else:
                printout.pop(0)
                date_time_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    print_out()
                else:
                    printout.pop(0)
                    expert_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        print_out()
                    else:
                        printout.pop(0)
                        ner_response(user_input)
                        if printout[0]:
                            printout.pop(0)
                            print_out()
                        else:
                            printout.pop(0)

        if data['chosen_intention'] != 'goodbye' and data['chosen_intention'] != 'book' and data['chosen_intention'] != None and data['chosen_intention'] != 'greeting':
            date_time_response(user_input)
            if printout[0]:
                printout.pop(0)
                print_out()
            else:
                printout.pop(0)
                expert_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    print_out()
                else:
                    printout.pop(0)
                    ner_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        print_out()
                    else:
                        printout.pop(0)
                        printout.append(
                            "BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                        printout.append(f"BOT: {llama3_response(user_input)}")
                        print_out()