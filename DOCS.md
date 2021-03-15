# Websockets
## Server
### Overall
We are using django-channels and redis for websocket connection. Frontend is connected through
reconnecting WebSocket (js library). Backend logic is in **consumers.py** files. Every time user sends message, it's sent
to consumers with data: 
* type
* message
* author
* image (author's profile image url)
* server
* channel
* id (temporary id using JS Date.now() to prevent WebSockets from receiving messages multiple times from multiple tabs)

### Frontend - receive
**app_base**:

Every time frontend receives websocket message, 
function is executed to check if message wasn't already received on the other tab. If message wasn't received yet,
**localStorage** value for last_msg_id will be updated and function will be executed to increment notifications counter in **localStorage** for:
* server
* channel

After localStorage update, notification badge for the specific server will be incremented as well.
