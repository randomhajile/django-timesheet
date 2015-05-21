$('#suggestion').keyup(function() {
    var query;
    var secret = /^[ab]+$/i
    var super_secret = /^((aa|ab(bb)*ba)|(ab(bb)*a|b)(a(bb)*a)*(a(bb)*ba|b))*(ab(bb)*a|b)(a(bb)*a)*$/i
    query = $(this).val();
    if (super_secret.test(query)) {
        $('#secret').text('Super Secret');
    } else if (secret.test(query)) {
        $('#secret').text('Secret, but not super secret');
    } else {
        $('#secret').text('');
    }
    $.get('/timesheet/suggest_job/', {suggestion: query}, function(data) {
        $('#jobs-list').html(data);
    })
})

$('#suggestion').keypress(function (e) {
    var key = e.which;
    if (key != 13) {
        return e;
    } else {
        return false;
    }
})


$(document).ready(function() {
    $('a[name=delete_time]').click(function() {
        var id;
        var csrf;
        id = $(this).attr('id');
        csrf = $('[name="csrfmiddlewaretoken"]').val();
        $.post('/timesheet/delete_time/'+id, {csrfmiddlewaretoken: csrf}, function(data) {
        })
        $(this).parent().parent().remove();
    })
})

$(document).ready(function() {
    /* With .click we only get the event handler on the currently existing nodes
       which breaks when we rewrite in the search function. This takes care of future
       elements. */
    $(document).on('click', 'a[name=delete_job]', function() {
        var id;
        var csrf;
        id = $(this).attr('id');
        csrf = $('[name="csrfmiddlewaretoken"]').val();
        $.post('/timesheet/delete_job/'+id+'/', {csrfmiddlewaretoken: csrf}, function(data) {
        })
        $(this).parent().parent().remove();
    })
})


$(document).ready(function () {
    var prefix = window.location.pathname.replace('/invoice/', '')
    var start = $('#start-datepicker').val()
    var end = $('#end-datepicker').val()
    $('#start-datepicker').datepicker({
        onSelect: function(dateText, inst) {
            start = dateText.replace(/\//g, '-');
            $(this).val(start);
            $.get(prefix+'/invoice/'+start+'/'+end+'/', {}, function(data) {
                $('div[name="line-items"]').html(data);
            })
        }
    });
    $('#end-datepicker').datepicker({
        onSelect: function(dateText, inst) {
            end = dateText.replace(/\//g, '-');
            $(this).val(end);
            $.get(prefix+'/invoice/'+start+'/'+end+'/', {}, function(data) {
                $('div[name="line-items"]').html(data);
            })
        }
    });
})
