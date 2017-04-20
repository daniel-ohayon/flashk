$(document).ready(function() {
    $('#card-modal').on('show.bs.modal', function (event) {
        var $modal = $(this);
        var $link = $(event.relatedTarget);
        var answer = $link.data('answer');
        var question = $link.text();
        $modal.find('#modal-question').text(question);
        $modal.find('#modal-answer').text(answer);
    });
});