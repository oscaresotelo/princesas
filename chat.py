from pyChatGPT import ChatGPT 
session_token = ""

api = ChatGPT(session_token)

response = api.send_message("historia de tucuman")
print(response["message"])