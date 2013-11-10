var config = {};

//Grab configuration info
$.getJSON('./static/js/config.json', function(data) {
    config = data;

    //Initialize Parse JS SDK
    Parse.initialize(config.parseAppId, config.parseJavaScriptKey);
});
function sendSMSForHelp(helperPhones) {


    // phoneNumber is a list of numbers
    var $phoneNumber = helperPhones; //actual variable setting
    // var $phoneNumber = "6263197945"; //Graham
//    var $phoneNumber = "4089406688"; //Mary
    var $textMessage = "Someone needs help! Reply to this text to get in touch with them.";

    for (var i = 0; i < helperPhones.length; i++) {
        //Handle the SMS form
        //execute Parse cloud code to send an SMS
        console.log($phoneNumber[i]);
        Parse.Cloud.run('sendLink', {
            phoneNumber:$phoneNumber[i],
            textMessage:$textMessage
        }, {
            success:function(response) {
                window.location.href = "http://localhost:5000/helpisontheway";
            },
            error: function(response) {
                console.log('error');
            }
        });
        return false;
    }
};