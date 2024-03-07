from flask import Flask, jsonify
from telethon import TelegramClient, events
from telethon.tl.types import InputDocumentFileLocation  # Import for file download logic 


# Your Telegram API ID and Hash 
api_id = 27317545 
api_hash = 'd1f33a01246e61a342e5b4cece1bf916'

client = TelegramClient('bharatfreecloudtest', api_id, api_hash) 

app = Flask(__name__)

@app.route('/fetchFiles')
async def get_files():
    messages = []
    async with client:
        async for message in client.iter_messages('me'):  # Fetching from 'Saved Messages'
            if message.file:  # Check if it has a file
                messages.append({
                    'name': message.file.name,
                    # Add more properties, e.g., 'size': message.file.size 
                })

    return jsonify(messages) 

app.route('/download/<filename>')
async def download_file(filename):
    async with client:
        # Search for the file in your 'Saved Messages'
        # You might want to make this search more robust, 
        # potentially storing some link between the original filename 
        # and how it's stored in Telegram.
        for message in await client.iter_messages('me'):
            if message.file and message.file.name == filename: 
                result = await client.download_media(message, file=filename)

                # Prepare a Flask response to serve the file
                return send_file(result, as_attachment=True)

    return "File not found", 404  # Return an error if the file is not found 

if __name__ == '__main__':
    client.start() 
    app.run(debug=True, use_reloader=False, use_debugger=False) # Modified for testing
