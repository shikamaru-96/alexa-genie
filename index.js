"use strict"

var Alexa = require('alexa-sdk');
var mysql = require('mysql2');
var pool;
function pool_init()
{
    pool = mysql.createPool(
    {
        connectionLimit : 100,
        host     : "",
        user     : "",
        password : "",
        database : "",
        debug    : true,
        acquireTimeout: 1000000,
    });
    pool.getConnection(
        function(err, connection) {
          if (err) throw err;
          console.log("Connected!");
        }
    );
}

var glob = []
var Query = function(text, q)
{
    pool.getConnection(function(erri, connection)
    {
        if(erri) console.log("Could not get connection from pool!");
        else
        {
            connection.query("SELECT *, MATCH (name,invocation,description) AGAINST ('"+text+"') as score FROM skills WHERE MATCH (name,invocation,description) AGAINST ('"+text+"') > 0 ORDER BY score DESC;", 
                function(err, result, fields)
                {
                    connection.release();
                    if(err) 
                    {
                        console.log(err);
                        q.response.speak("It seems I am getting old! There was some weird error.!\n");
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
                            q.response.speak("Oi! Ten thousand years will give you such a crick in the neck! I could find no skill matching that.");
                        }
                    }
                    q.emit(":responseReady");
                }
            );
        }
    });
}

const handlers = {
    "LaunchRequest":function(){
        this.response.speak("WOW!! Does it feel good to be outta there!");
        this.emit(':responseReady');
    },
    "SearchIntent":function(){
        var query = this.event.request.intent.slots.query.value;
        Query(query, this);
    },
    "AMAZON.HelpIntent": function(){
        this.response.speak("Rub on the lamp and ask me anything that you wish alexa to do. I will find you a skill that can make it possible.");
        this.emit(":responseReady");
    },
    "AMAZON.StopIntent" : function(){
        this.response.speak("Ugghh! Not back in the lamp");
        this.emit(":responseReady");
    },
    "AMAZON.CancelIntent" : function(){
        this.response.speak("Ok.");
        this.emit(":responseReady");
    },		
    "AskIntent" : function(){
        var query = this.event.request.intent.slots.number.value;
        if (query>glob.length){
            this.response.speak("Enter a valid number, master.").listen();
	    }
        else{
            this.response.speak(glob[query-1].description);
        }
        this.emit(":responseReady");
    }
}

exports.handler = function(event, context, callback){
    pool_init();
    var alexa = Alexa.handler(event, context);
    alexa.registerHandlers(handlers);
    alexa.execute();
};
