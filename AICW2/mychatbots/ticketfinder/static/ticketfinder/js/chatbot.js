// $(document).ready(function() {
//     // Function to retrieve the CSRF token from cookies
//     function getCsrfToken() {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 let cookie = cookies[i].trim();
//                 if (cookie.indexOf('csrftoken=') == 0) {
//                     cookieValue = cookie.substring('csrftoken='.length, cookie.length);
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }

//     // Function to handle the unload event
//     function handleUnloadEvent() {
//         let data = new URLSearchParams({
//             'csrfmiddlewaretoken': getCsrfToken(),
//             'confirm': 'true'
//         });
//         navigator.sendBeacon('/ticketfinder/clear_json/', data);
//     }

//     // Attach the event listener to beforeunload
//     window.addEventListener('beforeunload', handleUnloadEvent);

//     // Function to handle sending messages
//     function sendMessage(message = null) {
//         var userInput = message || $("#user-input").val().trim();
//         if (userInput) {
//             $("#chat-box").append("<div class='user mb-2 p-2 border rounded text-white bg-primary'>You: " + userInput + "</div>");
//             $.ajax({
//                 url: 'get_response/',  
//                 data: {'message': userInput},
//                 dataType: 'json',
//                 success: function(data) {
//                     if (Array.isArray(data.response)) {
//                         data.response.forEach(function(message) {
//                             if (/^\d+ Station:/.test(message)) {
//                                 var index = message.split(' ')[0];
//                                 var buttonText = message.replace(/^\d+ Station:/, '').trim().replace(/\\N/g, '').trim();
//                                 var button = $('<button>').addClass('btn station-button').text(index + ') ' + buttonText).attr('data-index', index);
//                                 $("#chat-box").append(button);
//                             } else {
//                                 $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>" + message + "</div>");
//                             }
//                         });
//                     } else {
//                         $("#chat-box").append("<div class='bot mb-2 p-2 border rounded bg-light'>" + data.response + "</div>");
//                     }
//                     $("#user-input").val('');
//                     $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
//                 }
//             });
//         }
//     }

//     // Event handling for dynamically created station buttons
//     $(document).on('click', '.station-button', function() {
//         var index = $(this).data('index');
//         sendMessage(index);
//     });

//     // Bind sendMessage to the Send button
//     $("#send").click(function() {
//         sendMessage();
//     });

//     // Bind sendMessage to the Enter key
//     $("#user-input").keypress(function(event) {
//         if (event.keyCode === 13) {
//             event.preventDefault();
//             sendMessage();
//         }
//     });
// });
$(document).ready(function() {
    // Function to retrieve the CSRF token from cookies
    function getCsrfToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.indexOf('csrftoken=') == 0) {
                    cookieValue = cookie.substring('csrftoken='.length, cookie.length);
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to handle the unload event
    function handleUnloadEvent() {
        let data = new URLSearchParams({
            'csrfmiddlewaretoken': getCsrfToken(),
            'confirm': 'true'
        });
        navigator.sendBeacon('/ticketfinder/clear_json/', data);
    }

    // Attach the event listener to beforeunload
    window.addEventListener('beforeunload', handleUnloadEvent);

    // Function to handle sending messages
    function sendMessage(message = null) {
        var userInput = message || $("#user-input").val().trim();
        if (userInput) {
            $("#chat-box").append("<div class='user mb-2 p-2 border rounded text-white bg-primary'>You: " + userInput + "</div>");
            $.ajax({
                url: 'get_response/',  
                data: {'message': userInput},
                dataType: 'json',
                success: function(data) {
                    if (Array.isArray(data.response)) {
                        data.response.forEach(function(message) {
                            if (/^\d+ Station:/.test(message)) {
                                var index = message.split(' ')[0];
                                var buttonText = message.replace(/^\d+ Station:/, '').trim().replace(/\\N/g, '').trim();
                                var button = $('<button>').addClass('btn station-button').text(index + ') ' + buttonText).attr('data-index', index);
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

    // Event handling for dynamically created station buttons
    $(document).on('click', '.station-button', function() {
        var index = $(this).data('index');
        sendMessage(index);
    });

    // Bind sendMessage to the Send button
    $("#send").click(function() {
        sendMessage();
    });

    // Bind sendMessage to the Enter key
    $("#user-input").keypress(function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            sendMessage();
        }
    });
});
