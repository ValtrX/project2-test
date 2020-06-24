document.addEventListener('DOMContentLoaded', () => {
    var socket = io();
    let room  = "room1"
    joinRoom("room1");

    // socket.on('connect', () => { // Predefined socket event called "Connect"
      //  socket.send("I am connected");
    //});


    //Sending messages 
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 'room': room, 'username': username });

        document.querySelector('#user_message').value='';
    }

    //Display Messages
    socket.on('message', data => { // Predefined socket event called "Message" but this one is on the server side
        
        //creating HTML elements
        const p = document.createElement('p');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        const span_username = document.createElement('span');
        
        if(data.username){

            //span
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;

            //HTML
            p.innerHTML += data.username+ br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML
            document.querySelector('#display-message-section').append(p);

        } else{
            printSysMsg(data.msg);
        }
        

        
    })
    

    // Room selection
    document.querySelectorAll('.select-room').forEach(li => {
        li.onclick = () => {
            let newRoom = li.innerHTML;

            if (newRoom == room){
                msg = `You are already in ${room}`;
                printSysMsg(msg);
            }else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom; //change name from current room to the room that client has joined
            }
             
        };
    });

    // Leave room
    function leaveRoom(room){
        socket.emit('leave', {'username': username, 'room': room});
    }

    // Join room
    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});

        // Clear message area
        document.querySelector('#display-message-section').innerHTML = ''
        // Clear text box
        document.querySelector('#user_message').innerHTML = ''
        // Autofocus on text box
        document.querySelector('#user_message').value=''
    }

    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg
        document.querySelector('#display-message-section').append(p)
    }

    // send new room to the server
    document.querySelector('#send_newRoom').onclick = () => {
        socket.emit('new_room', {'new_room_name': document.querySelector('#new_room').value}); // This is what you SEND to the server
    }

    // list new room
    socket.on('new room received', room => { //This is what you RECEIVE from the server
        
        let createdRoom = room.new_room_name
        console.log(createdRoom);
        const li = document.createElement('li');
        li.innerHTML = createdRoom
        li.setAttribute('class','select-room');

        document.querySelector('#rooms').append(li);
        });


// ################## SUPER IMPORTANT #################
    //document.querySelector('#send_message2').onclick = () => {
    //    socket.emit('my event', document.querySelector('#user_message2').value); // This is what you SEND to the server
    //}
    //
    //socket.on('my response', arg1 => { //This is what you RECEIVE from the server
    //    console.log(arg1);
    //    const p = document.createElement('p');
    //    const br = document.createElement('br');
    //    p.innerHTML = arg1;
    //    document.querySelector('#display-message-section2').append(p);
    //    
    //});
// ################ END SUPER IMPORTANT #################
    
});