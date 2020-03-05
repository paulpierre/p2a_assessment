$(document).ready(function(){

    // Setup regex patterns
    let regex_email = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
    let regex_phone = /^\d{10}$/;

    // Assign the submit button
    let btn_submit = $('button[type="submit"]');

    let btn_login = $('a#btnLogin');

    let btn_show_login = $('#toggle-login');

    let btn_send_sms = $('#btnSMS');

    // Submit button event handler
    btn_submit.click(function(e){

        // Don't do that thing that you like to do
        e.preventDefault();

        // Lets assign every click so we get latest input
        let input_fn = $('#firstName').val();
        let input_ln = $('#lastName').val();
        let input_email = $('#email').val();
        let input_phone = $('#phone').val();

        // Lets validate the input first
        if(input_fn == '' || input_fn.length < 1) {$('.val-fn').show();return false;} else $('.val-fn').hide();
        if(input_ln == '' || input_ln.length < 1) {$('.val-ln').show();return false;} else $('.val-ln').hide();
        if(!input_email.match(regex_email)) {$('.val-email').show();return false;} else $('.val-email').hide();
        if(!input_phone.match(regex_phone)) {$('.val-phone').show();return false;} else $('.val-phone').hide();

        // If we're here it means the user has submitted properly
        console.log('Form validated!');

        // Lets post to the API
        $.post('/submit', $('form#registration').serialize(), function(data){

            console.log('Response:');
            console.log(data)
        });
    });

    btn_login.click(function(e) {

        // Don't do that thing that you like to do
        e.preventDefault();

        let input_username = $('#userName').val();
        let input_password = $('#userPassword').val();

        if(input_username == '' || input_username.length < 1) {$('.val-username').show();return false;} else $('.val-username').hide();
        if(input_password == '' || input_password.length < 1) {$('.val-password').show();return false;} else $('.val-password').hide();

        $.post('/authenticate', $('form#login').serialize(), function(data){
            console.log('Response:');
            console.log(data);
            if(data.response == 1 && typeof data.url != "undefined")
            {
                console.log('redirecting user to the dashboard');
                window.location.href = data.url;
            }
        });
    });

    btn_show_login.click(function(e){
        e.preventDefault();
        $('#login-panel').fadeIn();
    });

    btn_send_sms.click(function(e){
        e.preventDefault();
        let user_list = $('form#user-sms').serialize();

        if (user_list.length == 0)
        {
            alert('You must select users to send a message to!');
            return;
        }
        let data = {'users':user_list,'message': $('#message').val()};
        console.log('attempting to send SMS data:');
        console.log(data);

            $.ajax('/sms', {
                data : JSON.stringify(data),
                contentType : 'application/json',
                type : 'POST',
                success:function(data){
                    console.log('Response:');
                    console.log(data);
                    if(data.response == 1)
                    {
                        alert('Successfully sent SMS')
                    } else {
                        alert('Error sending SMS')
                    }
                }
            });
    });
});