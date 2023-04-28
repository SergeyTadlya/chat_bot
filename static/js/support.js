// manager connect to chat
$("#manager-start").click(function(event) {
    event.preventDefault();
    ManagerConnect("start");
});
$("#manager-finish").click(function(event) {
    event.preventDefault();
    ManagerConnect("finish");
});
function ManagerConnect(status) {
   $.ajax({
        url: '/connecting_manager/',
        type: 'POST',
        data: {
            'manager_id': $("#manager").val(),
            'user_email': $("#user").val(),
            'connecting': status
        },
        success: function (data) {
            // connecting_status - start
            if(data.connecting_status == "start"){
                $("#manager-start")[0].style = "display: none";
                $("#manager-finish")[0].style = "";
                document.getElementById('text-form-area').hidden = false;
                document.getElementById('chat_history').style = "height: 89%";
            // connecting_status - finish
            }else{
                $("#manager-start")[0].style = "";
                $("#manager-finish")[0].style = "display: none";
                document.getElementById('text-form-area').hidden = true;
                document.getElementById('chat_history').style = "height: 100%";
            }
            $('#chat_history').append(data.manager_message_block);
            // send message from websocket
            chatSocket.send(JSON.stringify({
                message: data.manager_message_text,
                username: data.username,
                sender: "manager",
                message_block: "message_block",
            }));
        },
        error: function(error) {
            console.log('ajax connect manager', error);
        }
    });
}

// send message from manager
$("#manager-message-form").keydown(function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      sendManagerMessage();
    }
});
$("#send-manager-message").click(function(event) {
    event.preventDefault();
    sendManagerMessage();
});
function sendManagerMessage() {
    $.ajax({
        url: '/send_manager_message/',
        type: 'POST',
        data: {
            'manager_message': $("#new-manager-message").val(),
            'manager_id': $("#manager").val(),
            'client_email': $("#user").val(),
        },
        success: function (data) {
            // clear message in textarea
            document.getElementById('new-manager-message').value = '';
            // add user message in chat
            if (data.manager_message_text != "") {
                $('#chat_history').append(data.manager_message_block);
                // send message from websocket
                chatSocket.send(JSON.stringify({
                    message: data.manager_message_text,
                    username: data.username,
                    sender: "manager",
                    message_block: "message_block",
                }));
            }
        },
        error: function (error) {
            console.log('ajax send manager answer', error);
        }
    });
}