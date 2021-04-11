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

## Personal consumer
### Description
Personal consumer is used to receive data from other users, for example invitation (invitation, cancel, accept, decline). For example if User1 wants to
invite User2, he will connect to User2 personal consumer and send him data with type: **invitation**.

### Data sent:
* type:
    * invitation
    * cancel_invitation (for reject invitation and cancel invitation)
    * accept_invitation
* invited: user who is invited
* invited_img: invited user's profile img
* inviting: user who is inviting