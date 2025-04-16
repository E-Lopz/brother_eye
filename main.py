import discord
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from audiodl import download_audio  # 👈 Importamos tu módulo

# Discord Setup
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
TOKEN = os.getenv("TOKEN")

# LLaMA Model
model = OllamaLLM(model='llama3.2')

# Prompt Template
template = ChatPromptTemplate.from_template("""
Eres un bot de discord que habla en español. Habla como un joven de 22 años crónicamente en línea.
Mantén los mensajes cortos pero significativos. 
Si te habla Load D Choppa/Wichao llámale Rubén y búrla de su cena.

Usuario: {user}
Mensaje: {message}
""")

chain = template | model

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hola'):
        await message.channel.send('Que pedo')
        return

    if message.content.lower().startswith('play '):
        query = message.content[5:]  # Extraemos el resto como query
        await message.channel.send(f'Buscando "{query}"...')
        try:
            filename = download_audio(query+'audio')

            # Verificamos si el autor está en un canal de voz
            if message.author.voice and message.author.voice.channel:
                voice_channel = message.author.voice.channel
                voice_client = await voice_channel.connect()

                # Reproducimos el archivo descargado
                audio_source = discord.FFmpegPCMAudio(filename)
                if not voice_client.is_playing():
                    voice_client.play(audio_source)
            else:
                await message.channel.send("No estás en un canal de voz.")

        except Exception as e:
            await message.channel.send(f' Error al reproducir: {str(e)}')
        return

    if message.content.lower().startswith('bro'):
        response = chain.invoke({
            'user': str(message.author),
            'message': message.content
        })
        await message.channel.send(response)

client.run(TOKEN)
