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
                    if (Array.isArray(data.response)) {
                        data.response.forEach(function(message) {
                            message = formatMessage(message);
                            $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>" + message + "</div>");
                        });
                    } else {
                        var formattedMessage = formatMessage(data.response);
                        $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>" + formattedMessage + "</div>");
                    }
                    $("#user-input").val('');  
                    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);  
                }
            });
        }
    }

    function formatMessage(message) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        return message.replace(urlRegex, function(url) {
            return 'Please click <a href="' + url + '" target="_blank">here</a> to view this ticket';
        });
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

