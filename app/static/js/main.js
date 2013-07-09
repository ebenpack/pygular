// function calc_regex() {
//     var url = "/doregex";
//     var params = $("#form").serialize();
//     $.post(url, params, 
//     function(data) {
//         $('#id_result').html(data);
//     }, 
//     "text"
//     )
//     .error(function(data) {
//         $('#id_result').val("");
//     }
//     );
// }

function regulate() {
    /**
     * Get the form values, send them to the serve as a JSON object, properly format the results and stick them back in the page.
     */
    var req = {regexp: $('input[name="regex"]').val(), options: $("input[name='options']").serialize(), test: $('textarea[name="test"]').val()}

    $.getJSON('/regexp', req, function(data) {

        var items = [];
        $match_list = $('#result ol');
        $text = $("#result .text");

        $.each(data.result, function(key, val) {
            items.push(val);
        });

        $match_list.empty();
        if (items.length > 0) {
            $('<li/>', {
                'class': 'matches',
                html: items.join('')
            }).appendTo($match_list);
        }
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