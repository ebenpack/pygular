$(function(){

    $("#regexp, #options, #test").keyup(function(){
//        var checked = $('input[name="options"]').serializeArray();

        var params = $("input[name='options']").serialize();
        var req = {regexp: $('input[name="regexp"]').val(), options: params, test: $('textarea[name="test"]').val()}
    $.getJSON('/regexp', req, function(data) {

        var items = [];
        $.each(data.result, function(key, val) {
            items.push('<li>' + val + '</li>');
        });

        $('#result .match_list .list').empty();

        $('<ol/>', {
            'class': 'matches',
            html: items.join('')
        }).appendTo('#result .match_list .list');

        $("#result .match_text .text").empty();
        $("#result .match_text .text").append(data.fulltext);

        })
    });
});