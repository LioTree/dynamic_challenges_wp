// ctfd在提交flag后会把所有class为alert的标签全部设成display:none(见challenge.js)
// 所以得监听style的改变，变了就该回去..
var observer = new MutationObserver(function(mutations) {
    $("#upload-result-notification").css('display','block');
});

$(document).ready(function () {
    observer.observe(document.getElementById("upload-result-notification"), { attributes : true, attributeFilter : ['style'] });
    $("#submit-files").click(function () {
        var $input = $('#upload-writeup');
        var files = $input.prop('files');
        var challenge_id = $('#challenge-id').attr('value');
        // var challenge_name = $('.challenge-name').text();
        var data = new FormData();
        data.append('writeup', files[0]);
        data.append('cid', challenge_id);
        data.append('nonce', init.csrfNonce);

        $.ajax({
            url: '/writeup',
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result == 'Success')
                    uploaded_message(true);
                else
                    error_message();
            },
            error: function (xhr, status, error) {
                error_message();
            }
        });
    });

    $("#writeup-tab").click(function () {
        // $("#upload-result-notification").css('display','block')
        var challenge_id = $('#challenge-id').attr('value');
        url = '/writeup?cid=' + challenge_id;
        $.get(url, function (data, status) {
            if (data == 'Uploaded')
                uploaded_message(false);
        });
    });

    var uploaded_message = function (upload) {
        if (upload) {
            $("#upload-result-message").text('Success');
            $("#upload-result-notification").removeClass('alert-info');
            $("#upload-result-notification").addClass('alert-success');
            setTimeout(function () {
                $("#upload-result-notification").removeClass('alert-success');
                $("#upload-result-notification").addClass('alert-primary');
                $("#upload-result-message").text('Uploaded');
            }, 3000);
        } else {
            $("#upload-result-notification").removeClass('alert-info');
            $("#upload-result-notification").addClass('alert-primary');
            $("#upload-result-message").text('Uploaded');
        }
    };

    var error_message = function () {
        var pre_text = $("#upload-result-message").text();
        $("#upload-result-message").text('Error');
        $("#upload-result-notification").addClass('alert-danger');
        setTimeout(function () {
            $("#upload-result-notification").removeClass('alert-danger');
            $("#upload-result-message").text(pre_text);
        }, 3000);
    }
});