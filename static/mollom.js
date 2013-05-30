$(function() {

    var session_id = null;

    var btn  = $('#btn-send');
    var form = $('#form');

    var getServerRespond = function(data) {
        if (! data) {
            console.err("The server does not respond");
        } else {
            if(data.status == "spam" || data.status == "ham"){
                window.location.href = data.url;
            }else{
                form.find('#showable').removeClass('hidden');
                form.find('#captcha')[0].src = data.url;
                session_id = data.session_id;
                btn.off('click', sendContent);
                btn.on('click', sendContentWithCaptcha);
            }
        }
    };


    var sendContentWithCaptcha = function() {
        var data = {
            user       : form.find('.user').val(),
            comment    : form.find('.comment').val(),
            answer     : form.find('.captcha-input').val(),
            session_id : session_id
        };

        var json = JSON.stringify(data);
        $.post(window.location.href+"check", json,function(data){
            window.location.href = data.url
        });
    };


    var sendContent = function() {
        var data = {
            user    : form.find('.user').val(),
            comment : form.find('.comment').val()
        };

        var json = JSON.stringify(data);
        $.post(window.location.href+"checkSpam", json, getServerRespond);
    };


    // Main
    (function() {

        btn.on('click', sendContent);

    })();

});
