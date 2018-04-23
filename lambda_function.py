import sys
import logging
import rds_config
import pymysql
rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)
#glob = []

def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)
    
def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet,
                          session_attributes=session_attributes)
    
def on_launch(event, context):
    return statement("Welcome", "WOW!! Does it feel good to be outta there!")

def search_intent(event, context):
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, charset='utf8', connect_timeout=5)
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()
    cur = conn.cursor()
    keyword = event["request"]["intent"]["slots"]["query"]["value"]
    query = ("SELECT *, MATCH (name,invocation,description) AGAINST ('{0}') as score FROM skills WHERE MATCH (name,invocation,description) AGAINST ('{1}') > 0 ORDER BY score DESC;").format(keyword, keyword)
    cur.execute(query)
    res = []
    z = 0
    for row in cur:
        if z==3:
            break
        res.append(row)
        z+=1
    cur.close()
    #glob = res
    try:
        session_attributes = event['session']['attributes']
    except:
        session_attributes = {}
    session_attributes['res'] = res
    if len(res)>=3:
        return conversation("Search", ("The best matches for your search are, 1, {0}, 2, {1}, 3, {2}").format(res[0][1], res[1][1], res[2][1]), session_attributes)
    elif len(res)==2:
        return conversation("Search", ("The best matches for your search are, 1, {0}, 2, {1}.").format(res[0][1], res[1][1]), session_attributes)
    elif len(res)==1:
        return conversation("Search", ("The best match for your search is, 1, {0}.").format(res[0][1]), session_attributes)
    else:
        return statement("Search", "Oi! Ten thousand years will give you such a crick in the neck! I could find no skill matching that.")
    
def ask_intent(event, context):
    #event.request.intent.slots.number.value
    try:
        session_attributes = event['session']['attributes']
    except:
        session_attributes = {}
    num = event["request"]["intent"]["slots"]["number"]["value"]
    #print(len(glob))
    """try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, charset='utf8', connect_timeout=5)
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()
    cur = conn.cursor()
    query = ("SELECT * FROM skills WHERE  name='{0}'").format(num)
    cur.execute(query)
    z = 0
    g = ()
    for row in cur:
        g = row
        z+=1
    cur.close()
    if z==0:
        return statement("Ask", "No such skill found")
    else:
        return statement("Ask", g[3])"""
    num = int(num)
    try:
        res = session_attributes['res']
    except:
        return conversation("Ask", "Oi Alladin! That is not available now.", session_attributes)
    if num>len(res):
        return conversation("Ask", "Enter a valid number, master.", session_attributes)
    else:
        return conversation("Ask", res[num-1][3], session_attributes)

def cancel_intent(event, context):
    try:
        session_attributes = event['session']['attributes']
    except:
        session_attributes = {}
    return conversation("Cancel", "Cancelling", session_attributes)

def help_intent(event, context):
    try:
        session_attributes = event['session']['attributes']
    except:
        session_attributes = {}
    return conversation("Help", "Rub on the lamp and ask me anything that you wish alexa to do. I will find you a skill that can make it possible.", session_attributes)

def stop_intent(event, context):
    try:
        session_attributes = event['session']['attributes']
    except:
        session_attributes = {}
    return conversation("Stop", "Oohhh! Not back in the lamp", session_attributes)

def intent_router(event, context):
    intent = event['request']['intent']['name']
    # Custom Intents
    if intent == "SearchIntent":
        return search_intent(event, context)
    if intent == "AskIntent":
        return ask_intent(event, context)
    # Required Intents
    if intent == "AMAZON.CancelIntent":
        return cancel_intent(event, context)
    if intent == "AMAZON.HelpIntent":
        return help_intent(event, context)
    if intent == "AMAZON.StopIntent":
        return stop_intent(event, context)

def lambda_handler(event, context):
    
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)

