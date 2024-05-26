$(document).ready(function() {
    function sendMessage(message = null) {
        var userInput = message || $("#user-input").val().trim();
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
                            if (/^\d+ Station:/.test(message)) {
                                var index = message.split(' ')[0];
                                var buttonText = message.replace(/^\d+ Station:/, '').trim();
                                buttonText = buttonText.replace(/\\N/g, '').trim();
                                var button = $('<button>')
                                    .addClass('btn station-button')
                                    .text(index + ') ' + buttonText) 
                                    .attr('data-index', index);
                                $("#chat-box").append(button);
                            } else {
                                $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>" + message + "</div>");
                            }
                        });
                    } else {
                        $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>" + data.response + "</div>");
                    }
                    $("#user-input").val('');  
                    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
                }
            });
        }
    }

    // Code to handle when station button is clicked
    $(document).on('click', '.station-button', function() {
        var index = $(this).data('index');
        sendMessage(index); 
    });

    // Code to send message when the send button is clicked
    $("#send").click(function() {
        sendMessage();
    });

    // Code to send message via the enter key
    $("#user-input").keypress(function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            sendMessage();
        }
    });
});
