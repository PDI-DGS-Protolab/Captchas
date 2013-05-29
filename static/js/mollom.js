$(function() {

    var session_id = null;

    var btn  = $('#btn-send');
    var form = $('#form');

    var getServerRespond = function(data) {
        if (! data) {
            console.err("The server does not respond");
        }

        if (data.url && data.session_id) {
            captcha.removeClass('hidden')[0].src = data.url;
            session_id = data.session_id;
            btn.off('click', sendContent);
            btn.on('click', sendContentWithCaptcha);
        }
    };


    var sendContentWithCaptcha = function() {
        var data = {
            user       : form.find('.user'),
            comment    : form.find('.comment'),
            captcha    : form.find('#captcha'),
            session_id : session_id
        };

        var json = JSON.stringify(data);
        $.post(window.location.url, json);
    };


    var sendContent = function() {
        var data = {
            user    : form.find('.user'),
            comment : form.find('.comment')
        };

        var json = JSON.stringify(data);
        $.post(window.location.url, json, getServerRespond);
    };


    // Main
    (function() {

        btn.on('click', sendContent);

    })();

});
