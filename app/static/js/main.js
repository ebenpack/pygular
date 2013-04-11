function regulate() {
    /**
     * Get the form values, send them to the serve as a JSON object, properly format the results and stick them back in the page.
     */
    var req = {regexp: $('input[name="regexp"]').val(), options: $("input[name='options']").serialize(), test: $('textarea[name="test"]').val()}

    $.getJSON('/regexp', req, function(data) {

        var items = [];
        $match_list = $('#result .match_list .list');
        $text = $("#result .match_text .text");

        $.each(data.result, function(key, val) {
            items.push('<li>' + val + '</li>');
        });

        $match_list.empty();
        $('<ol/>', {
            'class': 'matches',
            html: items.join('')
        }).appendTo($match_list);

        $text.empty();
        $text.append(data.fulltext);

        var $warn = $("#warning");
        if (data.warn) {
            if ($warn.text().length > 0) {
                $warn.text(data.warn)
            }
            else {
                $warn.fadeOut(function(){
                    $warn.empty();
                    $warn.append(data.warn);
                    $warn.fadeIn();
                });
            }
        }
        else {
            $warn.fadeOut(function(){
                $warn.empty();
            });
        }
    });
}

$(function(){
    $("#regex, #test").keyup(function(){
        regulate();
    });
});

$(function(){
    $("input[name='options']").click(function(){
        regulate();
    });
});