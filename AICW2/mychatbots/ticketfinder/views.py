from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import UserQuery




def chat_interface(request):
    return render(request, 'ticketfinder/chat_interface.html')

def get_response(request):
    # Get the user's input from the GET parameters
    user_input = request.GET.get('message', '')

    # Save the user's input as a UserQuery instance
    if user_input:  # Make sure the input is not empty
        UserQuery.objects.create(query_text=user_input)
        # Now you can add additional logic here if you want to process the input further
        # For example, you can pass the user_input to your chatbot's NLP engine

    # Prepare the chatbot's response. Here it's simply echoing back the user_input
    # In a real scenario, you would replace this with actual processing
    response = {'response': f'Echo: {user_input}'}

    # Return the JsonResponse object that includes the chatbot's response
    return JsonResponse(response)