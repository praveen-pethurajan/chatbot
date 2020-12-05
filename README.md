# chatbot

Restaurant Chatbot using Zomato API1 from scratch Rasa where the bot can help to find the restaurant using location and cuisine preference shared by the user.

Things to know before building a chatbot:
1. Defining the scope of the bot 
2. Exploring Zomato API 
3. Understand RASA and its components 

Setup And execution:
1. Clone the repo
2. Setup rasa (refer https://rasa.com/docs/rasa/installation/)
3. Train the model using command - rasa train
4. Open the chat interface by running the rasa shell by using the command -  rasa shell
5. Continue the converstion by providing the necessary details

Sample conversation:
1. User - Hi
2. Bot - Hey! How are you?
3. User - good
4. Bot - Can you please help me with your location?
5. User - italian
6. Bot - {Lists all italian cusine restaurants in chennai}
7. Bot - Bye. Have a great time.

References:
1. https://developers.zomato.com/api
2. https://rasa.com/docs/

