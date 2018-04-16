"use strict"

const Alexa = require('alexa-sdk');
var rds_config = require('rds_config');
var mysql = require('mysql');
var connection = mysql.createConnection({
	host: rds_config.host,
	user: rds_config.user,
	password: rds_config.password,
	database: rds_config.db_name,
});
connection.connect(function(err){
        if(!err) {
              console.log("Database is connected ... nn");
        }
        else {
              console.log("Error connecting database ... nn");
        }
  });
var res = [];
const handlers = {
    "LaunchRequest":function(){
        this.response.speak("welcome to search columbus");
        this.emit(':responseReady');
    },
    "SearchIntent":function(){
        var query = this.event.request.intent.slots.query.value;
		res = []
        this.response.speak("Ok. Searching for a skill that "+query);
		connection.query("SELECT * FROM skills WHERE MATCH (name,invocation,description) AGAINST ('"+query+"' IN NATURAL LANGUAGE MODE)", function(err, result, fields)
		{
		    if(err) throw err;
		    var li = result.length;
		    var cn = 0;
		    var siz=0;
		    if(li<3) siz=li;
		    else siz = 3;
		    for(var i=0;i<siz;i++)
		    {
		        res.push(result[i]);
		    }
		}
		);
        if(res.length==3) 
		    this.response.speak("The results that I found are one, "+res[0]+", two, "+res[1]+", three, "+res[2]+".");
		else if(res.length==2)
		    this.response.speak("The results that I found are one, "+res[0]+", two, "+res[1]+".");
		else if(res.length==1)
		    this.response.speak("The results that I found are one, "+res[0]+".");
		else 
		    this.response.speak("Ma chuda nigga");
		this.emit(":responseReady");
    },
    "helpIntent": function(){
        this.response.speak("Ask me anything that you wish alexa to do. I will check whether it is possible or not and if possible then how")
        this.emit(":responseReady");
    },
    "AskIntent" : function(){
        var query = this.event.request.intent.slots.number.value;
        if (query>res.length)
            this.response.speak("Sorry nigga");
        else
        {
		    this.response.speak("Ok. Fetching details about" + query);
			this.response.speak(res[query-1].description);
        }
        this.emit(":responseReady");
    }
}

exports.handler = function(event, context, callback){
  var alexa = Alexa.handler(event, context);
    alexa.registerHandlers(handlers);
    alexa.execute();
};
