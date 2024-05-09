$(document).ready(function(){
    function getCsrfToken() {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCsrfToken());
            }
        }
    });

    window.onbeforeunload = function() {
        $.ajax({
            type: 'POST',
            url: '/clear_json/',  
            async: false,  
            data: {
                csrfmiddlewaretoken: getCsrfToken(),  
                'confirm': true
            },
            success: function() {
                console.log("JSON cleared");
            }
        });
    };
});
