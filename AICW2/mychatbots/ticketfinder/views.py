from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import UserQuery, TrainJourney
from .predictions_functionised import load_and_clean_data, calculate_features, train_and_evaluate
import logging



def chat_interface(request):
    return render(request, 'ticketfinder/chat_interface.html')

def get_response(request):
     # Get the user's input from the GET parameters
     user_input = request.GET.get('message', '')

     # Save the user's input as a UserQuery instance
     if user_input:  # Make sure the input is not empty
         UserQuery.objects.create(query_text=user_input)


     response = {'response': f'Echo: {user_input}'}

     # Return the JsonResponse object that includes the chatbot's response
     return JsonResponse(response)

# def get_input(request):
#     user_input = request.GET.get('message', '')

#     if user_input:
#         UserQuery.objects.create(query_text=user_input)

#     return user_input

# def send(text):
#     response = {'response': f'Echo: {text}'}
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
        # Log the error
        logger.error(f'An error occurred: {str(e)}')
        # If you want to handle errors without an error page, consider rendering the same or a different page with error info
        return render(request, 'ticketfinder/results.html', {'error': str(e)})