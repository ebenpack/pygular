function show_example() {
    $("#result").hide();
    $(".example").show();
}

function hide_example() {
    $(".example").hide();
    $("#result").show();
}

function ViewModel() {
	var self = this;

	self.matchtext = ko.observable();
	self.matchgroups = ko.observable();
	self.warning = ko.observable();
}

var vm = new ViewModel();
ko.applyBindings(vm);


var re_json = function() {
    var $match_text = $("#result .text");
    var $match_list = $('#result .match_list');

	var req = $('#regex_form').serialize();
    var $regex = $('#regex');
    var $test_string = $('#test');

    // Hide results if inputs are empty
    if (! $regex.val()) {
        $match_text.empty();
        $match_text.text($test_string.val());
        show_example();
    }

    if (! $test_string.val()) {
        $match_text.empty();
        show_example();
    }

    if ($regex.val() && $test_string.val()) {
		$.ajax({
				type: "POST",
				url: '/',
				data: req,
				dataType: 'json',
				success: function(data) {
					hide_example();
					ko.mapping.fromJS(data, {}, vm);
				}
			}
		);
	}
};

$(function(){
    // Show match group block which is hidden for noscript
    // and hide submit button
	$(".js").css("display", "block");
	$("input[type=submit]").hide();

    $("#regex, #test").keyup(function(){
		re_json();
    });

    $("input[name='options']").click(function(){
        re_json();
    });

	if (!($("#regex").val() && $("#test").val())) {
        show_example();
    }
    re_json();

    // Show/hide quickref
    $(".quickref").hide();
    $(".reference-heading").after(
        $("<a href='#'>").html("[Show]").on('click', function(){

            $(this).text($(".quickref").is(':hidden') ? '[Hide]' : '[Show]');
            $(".quickref").slideToggle();
            return false;
        })
    );
});
