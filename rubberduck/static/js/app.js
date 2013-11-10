var config = {};

//Grab configuration info
$.getJSON('./config.json', function(data) {
    config = data;

    //Initialize Parse JS SDK
    Parse.initialize(config.parseAppId, config.parseJavaScriptKey);
});
function sendSMSForHelp() {


    var $phoneNumber = "6263197945"; //Graham
//    var $phoneNumber = "4089406688"; //Mary
    var $textMessage = "Someone needs help!";

    //Handle the SMS form
    //execute Parse cloud code to send an SMS
    Parse.Cloud.run('sendLink', {
        phoneNumber:$phoneNumber,
        textMessage:$textMessage
    }, {
        success:function(response) {
			console.log('success');
        },
        error: function(response) {
            console.log('error');
        }
    });
    return false;
};