document.addEventListener('DOMContentLoaded', () => {
    var socket = io();
    // That's what he has (old verison)
    // var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Add events
    // socket.on('connect', () => {
    //     socket.send("I am connected"); // Send goes automatically to the server pocket called message
    // });


    let room = "Lounge";
    joinRoom("Lounge");

    // Display incoming message
    socket.on('message', data => {
        //console.log(`Message received: ${data}`); // Using backticks, not single quotes
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br'); // line break
        
        if (data.username) {
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + 
                br.outerHTML + span_timestamp.outerHTML; // This holds the message text
            document.querySelector('#display-message-section').append(p)
        } else {
            printSysMsg(data.msg);
        }
    
    });

    // For demonstration
    // socket.on('some-event', data => {
    //     console.log(data);
    // });

    // event listener for clicking the button SEND
    // Send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 
            'username': username, 'room': room});
        // Clear input area
        document.querySelector('#user_message').value='';
    }

    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                // System notifications that a user is already in the desired room
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom)
                room = newRoom;
            }
        }
    });

    // Leave room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room}); // If we use send, it goes to message bucket but we want it to go to leave bucket (custom bucket)
    }

    // Join room
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
        // Clear message area
        document.querySelector('#display-message-section').innerHTML=''
        // Autofocus on text box
        document.querySelector('#user_message').focus()
    }

    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})