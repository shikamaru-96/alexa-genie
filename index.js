"use strict"


const Alexa = require('alexa-sdk');

const handlers = {
    "LaunchRequest":function(){
        this.attributes['query'] = '';
        this.response.speak("welcome to search columbus");
        this.emit(':responseReady');
    },
    "SearchIntent":function(){
        var query = this.event.request.intent.slots.query.value;
        this.response.speak("Ok. Searching for a skill that "+query);
        this.emit(":responseReady");
    },
    "helpIntent": function(){
        this.response.speak("Ask me anything that you wish alexa to do. I will check whether it is possible or not and if possible then how")
        this.emit(":responseReady");
    },
    "AskIntent" : function(){
        var query = this.event.request.intent.slots.number.value;
        this.response.speak("Ok. Fetching details about" + query);
        this.emit(":responseReady");
    }
}

exports.handler = function(event, context, callback){
  var alexa = Alexa.handler(event, context);
    alexa.registerHandlers(handlers);
    alexa.execute();
};
