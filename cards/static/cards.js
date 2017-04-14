var KEY_CODES = {
    49: 1,
    50: 2,
    51: 3
};

function setupCsrf() {
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

$(document).ready(function() {

    setupCsrf();
    var isAnswerShown = false;

    $(document).keypress(function(e) {
        // if user presses space bar, show answer
        if (e.which == 32) {
            $('#answer').show();
            $('#scores').show();
            isAnswerShown = true;
        }
    });

    $(document).keypress(function (e) {
        if (isAnswerShown && e.which in KEY_CODES) {
            // post score for the current card
            $.post(window.location.pathname + 'score/',
                {'score': KEY_CODES[e.which]},
                function() {
                    location.assign('/cards/random');
                }
            );
        }
    });
});