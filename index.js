"use strict"

var Alexa = require('alexa-sdk');
var mysql = require('mysql2');
var connection = mysql.createConnection({
    host     : "",
    user     : "",
    password : "",
    database : "",
    debug    : true,
    acquireTimeout: 1000000,
});

var glob = []
var Query = function(text, q)
{
    connection.query("SELECT * FROM skills WHERE MATCH (name,invocation,description) AGAINST ('"+text+"' IN NATURAL LANGUAGE MODE)>0", 
        function(err, result, fields)
        {
            connection.commit();
            if(err) 
            {
                console.log(err);
                q.response.speak("There was some weird error.. Sorry bruh!\n");
            }
            else {
                var siz = result.length;
                glob = result;
                if(siz>=3)
                {
                    q.response.speak("The best matches for your search are, 1,"+result[0].name+",2, "+result[1].name+",3, "+result[2].name);
                }
                else if(siz==2)
                {
                    q.response.speak("The best matches for your search are, 1,"+result[0].name+",2, "+result[1].name);
                }
                else if(siz==1)
                {
                    q.response.speak("The best match for your search is, 1,"+result[0].name);
                }
                else
                {
                    q.response.speak("Sorry man, I could not find any match for that.");
                }
            }
            q.emit(":responseReady");
        }
    );
}

const handlers = {
    "LaunchRequest":function(){
        this.response.speak("welcome my lord");
        this.emit(':responseReady');
    },
    "SearchIntent":function(){
        var query = this.event.request.intent.slots.query.value;
        Query(query, this);
    },
    "AMAZON.HelpIntent": function(){
        this.response.speak("Ask me anything that you wish alexa to do. I will check whether it is possible or not and if possible then how");
        this.emit(":responseReady");
    },
    "AMAZON.StopIntent" : function(){
        this.response.speak("Exiting my lord");
        this.emit(":responseReady");
    },
    "AMAZON.CancelIntent" : function(){
        this.response.speak("Ok try again");
        this.emit(":responseReady");
    },		
    "AskIntent" : function(){
        var query = this.event.request.intent.slots.number.value;
        if (query>glob.length){
            this.response.speak("Enter a valid number dude.").listen();
	}
        else{
            this.response.speak(glob[query-1].description);
        }
        this.emit(":responseReady");
    }
}

exports.handler = function(event, context, callback){
    var alexa = Alexa.handler(event, context);
    alexa.registerHandlers(handlers);
    alexa.execute();
};

