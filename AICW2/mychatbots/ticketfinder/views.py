from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import UserQuery, TrainJourney
from .predictions_functionised import load_and_clean_data, calculate_features, train_and_evaluate
import logging
from .jsonpurifier import purify_json, purify_pred_json
from .NLP_main import main

def clear_json(request):
    if request.method == 'POST':
        purify_json()
        purify_pred_json()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'}, status=400)



def chat_interface(request):
    return render(request, 'ticketfinder/chat_interface.html')

def get_response(request):

    user_input = request.GET.get('message', '')
    bot_response = None

    messages = []

    if user_input:
        output = main(user_input)

    if output:
        for message in output:
            messages.append(message)

    print(messages)

    response = {'response': messages }

    return JsonResponse(response)

# copy encase it doesn't work
# def get_response(request):
#     user_input = request.GET.get('message', '')
#
#     if user_input:
#         UserQuery.objects.create(query_text=user_input)
#
#     response = {'response': f'Echo: {user_input}'}
#
#     return JsonResponse(response)

logger = logging.getLogger(__name__)
def train_view(request):
    try:
        data = load_and_clean_data()
        data = calculate_features(data)
        if data.empty or 'arrival_delay' not in data.columns:
            raise ValueError("No data available for training or missing target variable.")

        
        model, mse, mae, rmse = train_and_evaluate(data)
        return render(request, 'ticketfinder/results.html', {
            'model': model,
            'mse': mse,
            'mae': mae,
            'rmse': rmse
        })

    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')
        return render(request, 'ticketfinder/results.html', {'error': str(e)})