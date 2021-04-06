$(document).ready(function(){
    var socket = io.connect('http://127.0.0.1:5000')

    var usersConnected = document.getElementById("usersConnected");
    var textBoxID =  document.getElementById("textBox");

    socket.on('users', function(users) {
        userCount = document.getElementById("usersConnected");
        userCount.innerText = users.user_count;
        console.log('Connected');
        /*$('#textBox').val(users.message);*/
    });
    
    socket.on('message', function(msg){
        textBoxID.innerHTML = msg;
        console.log(msg);
    });

    $('#textBox').on('keyup', function() {
        socket.send($('#textBox').html());
        console.log('sending...');
    });
    
    
    $('#boldButton').on('click', function(){
      socket.send($('#textBox').html());
    });

    $('#italicButton').on('click', function(){
      socket.send($('#textBox').html());
    });

    $('#underlineButton').on('click', function(){
      socket.send($('#textBox').html());
    });

});
