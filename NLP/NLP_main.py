from NLP_booking import *
from NLP_predict import *
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

    with open(past_inputs, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_input])



    if user_input == "reset":
        with open(reset_path, 'r') as reset:
            default = json.load(reset)

        with open(data_path, 'w') as file:
            json.dump(default, file, indent=4)

        with open(pred_reset_path, 'r') as pd_rs:
            pd_default = json.load(pd_rs)

        with open(pred_data_path, 'w') as pd_file:
            json.dump(pd_default, pd_file, indent=4)
        printout.append("I have reset the selection. start by telling me your ticket type. or type 'predict' to predict a train.")
        return printout

    data['chosen_intention'] = check_intention_by_keyword(user_input)
    with open(data_path, 'w') as file:
        json.dump(data, file, indent=4)

    if data['station_selector']:
        if data['selected'] == None:
            data['selected'] = user_input
            with open(data_path, 'w') as file:
                json.dump(data, file, indent=4)

            with open(past_inputs, 'r') as past:
                user_input = past.readlines()[-2]
        else:
            data['selected'] = int(user_input)
            with open(data_path, 'w') as file:
                json.dump(data, file, indent=4)

            with open(past_inputs, 'r') as past:
                user_input = past.readlines()[-3]

    if pd_data['pred_station_selector']:
        if pd_data['pred_selected'] == None:
            pd_data['pred_selected'] = user_input
            with open(pred_data_path, 'w') as file:
                json.dump(pd_data, file, indent=4)

            with open(past_inputs, 'r') as past:
                user_input = past.readlines()[-2]
        else:
            pd_data['pred_selected'] = int(user_input)
            with open(pred_data_path, 'w') as file:
                json.dump(pd_data, file, indent=4)

            with open(past_inputs, 'r') as past:
                user_input = past.readlines()[-3]


    printout.pop(0)


    if data['chosen_intention'] == 'goodbye':
        goodbye_response()


        with open(reset_path, 'r') as reset:
            default = json.load(reset)

        with open(data_path, 'w') as file:
                json.dump(default, file, indent=4)

        with open(pred_reset_path, 'r') as pd_rs:
            pd_default = json.load(pd_rs)

        with open(pred_data_path, 'w') as pd_file:
            json.dump(pd_default, pd_file, indent=4)

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
                            printout.append("Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                            printout.append(f"{llama3_response(user_input)}")
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
                        printout.append( "Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                        printout.append(f"{llama3_response(user_input)}")
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
                            printout.append("Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                            printout.append(f"{llama3_response(user_input)}")
                            return printout

    if data['chosen_intention'] == 'predict':
        pred_ner_response(user_input)
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
                pred_expert_response(user_input)
                if printout[0]:
                    printout.pop(0)
                    return printout
                else:
                    printout.pop(0)
                    pred_ner_response(user_input)
                    if printout[0]:
                        printout.pop(0)
                        return printout
                    else:
                        printout.pop(0)
                        if check_intention_by_keyword_nr(user_input) == "predict":
                            return printout
                        else:
                            printout.append("Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                            printout.append(f"{llama3_response(user_input)}")
                            return printout

    if data['chosen_intention'] != 'goodbye' and data['chosen_intention'] != 'book' and data['chosen_intention'] != None and data['chosen_intention'] != 'greeting' and data['chosen_intention'] != 'predict':
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
                        printout.append("Sorry I don't understand that. I have sent your message to a LLM and this is the response:")
                        printout.append(f"{llama3_response(user_input)}")
                        return printout

if __name__ == "__main__":

    sentence = ["hello", "I would like to predict a ticket","future train", "I want to go from Norwich to London on sunday at 5pm", "1", "2","goodbye"]

    output = main("hello")
    print(output)
    output = main(sentence[1])
    print(output)
    output = main(sentence[2])
    print(output)
    output = main(sentence[3])
    print(output)
    output = main(sentence[4])
    print(output)
    output = main(sentence[5])
    print(output)
    output = main(sentence[6])
    print(output)

    exit()


