$(document).ready(function(){
    function sendMessage() {
        var userInput = $("#user-input").val().trim();
        if (userInput) {
            $("#chat-box").append("<div class='user mb-2 p-2 border rounded text-white bg-primary'>You: " + userInput + "</div>");
            $.ajax({
                url: 'get_response/',  // Make sure this URL matches  Django URL configuration
                data: {
                    'message': userInput
                },
                dataType: 'json',
                success: function(data) {
                    $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>Bot: " + data.response + "</div>");
                    $("#user-input").val('');  // Clear input field
                    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);  // Scroll to the bottom
                }
            });
        }
    }

    // Send message on button click
    $("#send").click(sendMessage);

    // Send message on Enter key press
    $("#user-input").keypress(function(event) {
        if (event.keyCode === 13) {  // 13 is the Enter key
            event.preventDefault();  // Prevent default "Enter" behavior 
            sendMessage();
        }
    });
});