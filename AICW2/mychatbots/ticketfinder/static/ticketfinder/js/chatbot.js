$(document).ready(function(){
    function sendMessage() {
        var userInput = $("#user-input").val().trim();
        if (userInput) {
            $("#chat-box").append("<div class='user mb-2 p-2 border rounded text-white bg-primary'>You: " + userInput + "</div>");
            $.ajax({
                url: 'get_response/',  
                data: {
                    'message': userInput
                },
                dataType: 'json',
                success: function(data) {
                    // this checks if data.response is an array and iterate over it
                    if (Array.isArray(data.response)) {
                        data.response.forEach(function(message) {
                            $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>BOT: " + message + "</div>");
                        });
                    } else {
                        // if not a bunch of messages then fallback for single message responses
                        $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>BOT: " + data.response + "</div>");
                    }
                    $("#user-input").val('');  // Clear input field
                    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);  // Scroll to the bottom
                }
            });
        }
    }

    // Code to send message when the send button is clicked
    $("#send").click(sendMessage);

    // Code to send message via the enter key
    $("#user-input").keypress(function(event) {
        if (event.keyCode === 13) {  
            event.preventDefault();  
            sendMessage();
        }
    });
});
