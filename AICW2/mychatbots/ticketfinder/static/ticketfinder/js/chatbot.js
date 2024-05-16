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
                    $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>BOT: " + data.response + "</div>");
                    $("#user-input").val('');  
                    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);  
                }
            });
        }
    }

    // Code to send message via the enter key
    $("#send").click(sendMessage);

    // Code to send message via the enter key
    $("#user-input").keypress(function(event) {
        if (event.keyCode === 13) {  
            event.preventDefault();  
            sendMessage();
        }
    });
});
