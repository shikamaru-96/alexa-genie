# alexa-genie

<img src="lamp.png">

An alexa skill that can help you find other skills in a more conveinient and simple way. it return 3 outputs that will be the best match for your query. 
ID of our skill : amzn1.ask.skill.0d6c83ac-8024-4eb4-97e2-e62d51e6bbb4


## Requirements
* Nodejs
* Python2.7
* AWS lambda services
* Alexa Skills Kit
* Mysql

## Build Instructions
* Build your database on amazon-rds and enter the credentials in rds_config.json
* Build the skill interface with frontend.json
* Use index.js as lambda function

## Usage Instructions
* Alexa open genie (Launch Instruction)
* Alexa ask genie to find me a skill that can "your query"
* Alexa ask genie to elaborate "number in range (1-3)"
