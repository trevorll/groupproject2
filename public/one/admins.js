function myFunction() {




    const url = location.protocol + '//' + location.host + '/admin_s';
    (fetch(url).then(response => response.json()).then(json => {
        one(JSON.parse(json))
    }));

}

function one(data) {
    var username = document.querySelector("#username");
    var email = document.querySelector("#email");
    var nationalid = document.querySelector("#nationalid");
    var phone = document.querySelector("#phone");
    var staffid = document.querySelector("#staffid");
    let valid = true;
    $("#message").html('');

    for (var i = 0; i < data.length; i++) {
        if (username.value.toLowerCase() == data[i].username.toLowerCase()) {
            valid = false;
            $('#message').html('Pick another username').css('color', 'red');
            break

        } else if (email.value.toLowerCase() == data[i].email.toLowerCase()) {
            valid = false;
            $('#message').html('Pick another email this is already registered').css('color', 'red');
            break;

        } else if (phone.value == data[i].phone_number) {
            valid = false;
            $('#message').html('Pick another phone number this is already registered').css('color', 'red');
            break;

        } else if (staffid.value.toLowerCase() == data[i].staff_id.toLowerCase()) {
            valid = false;
            $('#message').html('Pick another staff id this is already registered').css('color', 'red');
            break;

        } else if (nationalid.value == data[i].national_id) {
            valid = false;
            $('#message').html('Pick another national id this is already registered').css('color', 'red');
            break;

        }
    }
    return valid;

}