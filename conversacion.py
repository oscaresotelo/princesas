import asyncio
from EdgeGPT import Chatbot, ConversationStyle

async def main():
    
    bot = await Chatbot.create(cookie_path='./cookies.json')
    # bot = await Chatbot.create()
    print(await bot.ask(prompt="historia del che guevara en 200 palabras? en español ", conversation_style=ConversationStyle.creative))
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())