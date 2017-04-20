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
    var cardIndex = -1;
    var cards = [];
    var maxIndex = -1;

    // TODO refactor to object style
    function displayNextCard() {
        cardIndex++;
        var $answer = $('#answer');
        $answer.hide();
        $('#scores').hide();
        $('#question').text(cards[cardIndex].question);
        $answer.text(cards[cardIndex].answer);
        isAnswerShown = false;
    }

    $.get(window.location.pathname + 'next/', function(response) {
        cards = response.output;
        maxIndex = response.output.length - 1;
        displayNextCard();
    });

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
            $.post('/cards/' + cards[cardIndex].id + '/score/',
                {'score': KEY_CODES[e.which]},
                function() {
                    if (cardIndex === maxIndex) {
                        // when review is done, go back to home page
                        document.location.href = '/cards/';
                    }
                    displayNextCard();
                }
            );
        }
    });
});