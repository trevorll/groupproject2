function myFunction() {




    const url = location.protocol + '//' + location.host + '/staff_s';
    (fetch(url).then(response => response.json()).then(json => {
        one(JSON.parse(json))

    }));
}

function one(data) {
    var nationalid = document.querySelector("#nationalid");
    var staffid = document.querySelector("#staffid");
    var phone = document.querySelector("#phone");
    let valid = true;
    $("#message").html('');
    for (var i = 0; i < data.length; i++) {
        if (staffid.value.toUpperCase() == data[i].staff_id) {
            valid = false;
            $('#message').html('Pick another staff id number this is already registered').css('color', 'red');
            break;

        } else if (nationalid.value == data[i].national_id) {
            valid = false;
            $('#message').html('Pick another national id this is already registered').css('color', 'red');
            break;

        } else if (phone.value == data[i].phone_nuber) {
            valid = false;
            $('#message').html('Pick another phone number this is already registered').css('color', 'red');
            break;

        }
    }
    return valid;

}