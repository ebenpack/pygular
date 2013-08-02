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
     * Get the form values, send them to the server as a JSON object, properly format the results and stick them back in the page.
     */
    var req = $('#regex_form').serialize();

    var $match_text = $("#result .text");
    var $match_list = $('#result .match_list');

    var $regex = $('#regex')
    var $test_string = $('#test')



    if (! $regex.val()) {
        $match_text.empty();
        $match_text.text($test_string.val());
    }

    if (! $test_string.val()) {
        $match_text.empty();
    }

    if ($regex.val() && $test_string.val()) {
        $.ajax({
          type: "POST",
          url: '/',
          data: req,
          dataType: 'json',
          success: function(data){
              var match_groups = [];
              $.each(data.match_groups, function(key, val) {
                match_groups.push(val);
              });

            $('#result .match_list .list').empty();
            // Build match group lists
            // This feels wrong. Surely there's a better way to do this. Been working on this too long now.
            if (match_groups.length > 0) {

                for (var i = 0; i < match_groups.length; i++) {
                    $('#result .match_list .list').append($('<div/>', {'class': 'match_group', 'id': 'match_group' + i,  html: 'Match ' + (i + 1) + ':'}).append(

                    ));
                    for (var j = 0; j < match_groups[i].length; j++)
                        {
                            var match = ""
                            $.each(
                                    match_groups[i][j], function(key, val){
                                        match = "<span class='match_name'>" + key + ".</span>" + '&nbsp;&nbsp;' + val;
                                    });

                            $('<pre/>',
                                {html: match,
                                'class': 'match'
                                }).appendTo($('#match_group' + i));
                        }
                }
            }

            $match_text.empty();
            $match_text.append(data.match_text);

            var $warn = $("#warning");
            if (data.warn) {
                if ($warn.text().length > 0) {
                    $warn.text(data.warn)
                }
                else {
                    $warn.fadeOut(function(){
                        $warn.empty();
                        $warn.text(data.warn);
                        $warn.fadeIn();
                    });
                }
            }
            else {
                $warn.fadeOut(function(){
                    $warn.empty();
                });
            }
          }
        });
    }
}

$(function(){
    $("#regex, #test").keyup(function(){
        regulate();
    });

    $("input[name='options']").click(function(){
        regulate();
    });

    $("input[type=submit]").hide();

    $(".quickref").hide();
    $(".reference-heading").after(
        $("<a href='#'>").html("[Show]").on('click', function(){

            $(this).text($(".quickref").is(':hidden') ? '[Hide]' : '[Show]');
            $(".quickref").slideToggle();
            return false;
        })
    );

});
