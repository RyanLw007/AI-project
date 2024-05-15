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



def main(input):
    global final_chatbot
    global printout

    final_chatbot = True

    printout.clear()

    user_input = input

    with open('data/past_inputs.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_input])



    if user_input == "reset":
        with open('data/reset.json', 'r') as reset:
            default = json.load(reset)

        with open('data/data.json', 'w') as file:
            json.dump(default, file, indent=4)
        printout.append("BOT: I have reset the selection. start by telling me your ticket type.")
        return printout

    data['chosen_intention'] = check_intention_by_keyword(user_input)
    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=4)

    if data['station_selector']:
        if data['selected'] == None:
            data['selected'] = user_input
            with open('data/data.json', 'w') as file:
                json.dump(data, file, indent=4)

            with open('data/past_inputs.csv', 'r') as past:
                user_input = past.readlines()[-2]
        else:
            data['selected'] = int(user_input)
            with open('data/data.json', 'w') as file:
                json.dump(data, file, indent=4)

            with open('data/past_inputs.csv', 'r') as past:
                user_input = past.readlines()[-3]



    printout.pop(0)


    if data['chosen_intention'] == 'goodbye':
        goodbye_response()


        with open('data/reset.json', 'r') as reset:
            default = json.load(reset)

        with open('data/data.json', 'w') as file:
                json.dump(default, file, indent=4)

        return printout

    if data['chosen_intention'] == 'book':
        ner_response(user_input)
        if printout[0]:
            printout.pop(0)
            return printout
        else:
            printout.pop(0)
            date_time_response(user_input)
            if printout[0]:
                printout.pop(0)
                return printout
            else:
                printout.pop(0)
                expert_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    return printout
                else:
                    printout.pop(0)
                    ner_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        return printout
                    else:
                        printout.pop(0)
                        if check_intention_by_keyword_nr(user_input) == "book":
                            return printout
                        else:
                            printout.append("BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                            printout.append(f"BOT: {llama3_response(user_input)}")
                            return printout
    if data['chosen_intention'] == None:
        ner_response(user_input)
        if printout[0]:
            printout.pop(0)
            return printout
        else:
            printout.pop(0)
            date_time_response(user_input)
            if printout[0]:
                printout.pop(0)
                return printout
            else:
                printout.pop(0)
                expert_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    return printout
                else:
                    printout.pop(0)
                    ner_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        return printout
                    else:
                        printout.pop(0)
                        printout.append( "BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                        printout.append(f"BOT: {llama3_response(user_input)}")
                        return printout


    if data['chosen_intention'] == 'greeting':
        data['chosen_intention'] = None
        ner_response(user_input)
        if printout[0]:
            printout.pop(0)
            return printout
        else:
            printout.pop(0)
            date_time_response(user_input)
            if printout[0]:
                printout.pop(0)
                return printout
            else:
                printout.pop(0)
                expert_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    return printout
                else:
                    printout.pop(0)
                    ner_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        return printout
                    else:
                        printout.pop(0)
                        if check_intention_by_keyword_nr(user_input) == "greeting":
                            return printout
                        else:
                            printout.append("BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                            printout.append(f"BOT: {llama3_response(user_input)}")
                            return printout

    if data['chosen_intention'] != 'goodbye' and data['chosen_intention'] != 'book' and data['chosen_intention'] != None and data['chosen_intention'] != 'greeting':
        date_time_response(user_input)
        if printout[0]:
            printout.pop(0)
            return printout
        else:
            printout.pop(0)
            expert_response(user_input)
            if printout[0]:
                printout.pop(0)
                return printout
            else:
                printout.pop(0)
                ner_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    return printout
                else:
                    printout.pop(0)
                    if check_intention_by_keyword_nr(user_input) == "book":
                        return printout
                    else:
                        printout.append("BOT: Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                        printout.append(f"BOT: {llama3_response(user_input)}")
                        return printout

if __name__ == "__main__":




    # output = main("reset")
    # print(output)
    # exit()

    test = ""
    print("Welcome to the chatbot! Type 'exit' to end the conversation")

    while (test != "exit"):
        in_put = input()

        if in_put == "exit":
            in_put = "bye"
            output = main(in_put)
            for item in output:
                print(item)
            test = "exit"
        else:
            output = main(in_put)
            for item in output:
                print(item)
