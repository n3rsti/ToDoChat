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

### Delay functionality
Delay is implemented so users can't spam other users with invitation + cancel and server gets less ws requests.
Spamming can be still abused by creating ws connection through browser console and sending data without any frontend limits implemented for buttons.
Delay is implemented in invitationBase object for invite, cancel (reject / cancel) functions. Delay is disabled for accept
function because it can't be really abused by spamming buttons. 

How delay works:

Interval variable value: 1500ms

* Function creates variable with value of current time in milliseconds
```javascript
  let date = new Date();
  let milliseconds = date.getTime();
```
* Function gets value of time when specific method was used for specific user. In this example method = **invite**. If localStorage value
doesn't exist, lastTimeUsed = **NaN**
```javascript
let invited = btn.dataset.user; // Value from button
let lastTimeUsed = Number(localStorage[`invite_delay_${invited}`]);
```
* Function compares **current time** - **lastTimeUsed** to **interval** variable. If previous function was executed more than
**interval variable value** seconds ago **OR** localStorage value doesn't exist, ws request is executed and localStorage value is set to current time.
```javascript
if ((milliseconds - lastTimeUsed) > interval || isNaN(lastTimeUsed)) {
    // *code for ws request*
    localStorage.setItem(`invite_delay_${invited}`, String(date.getTime()));
}
```