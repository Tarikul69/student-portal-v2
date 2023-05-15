(function () {
    'use strict';

    //to store different channel created by individual student
    let vdoChannel = {}
    let rtcConnections = {}


    // Contains the stun server URL we will be using.
    // let iceServers = {
    //     iceServers: [
    //     { urls: "stun:stun.services.mozilla.com" },
    //     { urls: "stun:stun.l.google.com:19302" },
    // ],
    // };

    // ----------------------------------------------------
    // Configure Pusher instance
    // ----------------------------------------------------

    var pusher = new Pusher('a60f02f7bde182f427ce', {
        authEndpoint: '/pusher/auth',
        cluster: 'ap2',
        encrypted: true,
      });

    //Pusher.logToConsole = true

    // ----------------------------------------------------
    // Chat Details
    // ----------------------------------------------------

    let chat = {
        messages: [],
        currentRoom: '',
        currentChannel: '',
        subscribedChannels: [],
        subscribedUsers: []
    }
    // ----------------------------------------------------
    // Chat History
    // ----------------------------------------------------
    let chatHist = {}
    
    // ----------------------------------------------------
    // Subscribe to the generalChannel  and vdoChannel
    // ----------------------------------------------------

    var generalChannel = pusher.subscribe('general-channel');

    //this channel helps to listen to event created by server
    //to form private channel with student
    var vdoInit = pusher.subscribe('vdo-channel');

    // ----------------------------------------------------
    // Targeted Elements
    // ----------------------------------------------------

    const chatBody = $(document)
    const chatRoomsList = $('#rooms')
    const chatReplyMessage = $('#replyMessage')

    // ----------------------------------------------------
    // Register helpers
    // ----------------------------------------------------

    const helpers = {

        createAnswer: function(data){
            axios.post('/getcredential', {'verifiedName':email})
            .then((response)=>{
                let iceServersTwo = {
                    iceServers : [
                        {
                            urls : "turn:161.97.79.224:3478?transport=tcp",
                            username: response.data.username,
                            credential: response.data.credential
                        }
                    ]
                }
                rtcConnections[data.email] = new RTCPeerConnection(iceServersTwo) 
                rtcConnections[data.email].ontrack =(eve)=>{
                    helpers.OnTrackFunction(eve, data)
                }
                rtcConnections[data.email].onicecandidate = (eve)=>{
                    helpers.OniceCandidateFunction(eve, data)        
                }
                rtcConnections[data.email].onconnectionstatechange = (eve)=>{
                    helpers.ConnectionStateChgFun(eve, data)
                }
                rtcConnections[data.email].setRemoteDescription(data['offer'])       
                rtcConnections[data.email].createAnswer().then((answer)=>{
                    // console.log(answer)
                    rtcConnections[data.email].setLocalDescription(answer, ()=>{
                        console.log('it was successfull')
                    },(eve)=>{
                        console.log(eve)
                    })
                    vdoChannel[data.email].trigger('client-set-ans', {'email':data.email, 'answer':answer})
                })
            })
            .catch((e)=>{
                console.log(e)
            })
        },

        OniceCandidateFunction : function(eve, data){
            
            if(eve.candidate !== null){
                console.log('Candidate sent')
                vdoChannel[data.email].trigger('client-admin-ice', {'email':data.email, 'candidate':eve.candidate})
            }
        },

        ConnectionStateChgFun: function(eve, data){
            console.log(rtcConnections[data.email].connectionState)
            switch(rtcConnections[data.email].connectionState){
                case "closed":
                    //remove the vdo
                    helpers.RemoveVdo(data)
                    rtcConnections[data.email] = null
                case "failed":
                    helpers.RemoveVdo(data)
                case "disconnected":
                    //hide the vdo and display connecting
                    var el = document.getElementById(data.email)
                    if(el){
                        el.parentNode.style.display = 'none'
                    }
                case "connected":
                    //show the vdo
                    var el = document.getElementById(data.email)
                    if(el){
                        el.parentNode.style.display = 'block'
                    }
            }

        },

        OnTrackFunction : function(eve,data){
            console.log('add user vdo and audio stream')
            var el = document.getElementById(data.email)
            if(el){
                el.srcObject = eve.streams[0];
                el.addEventListener('loadedmetadata', function (e) {
                    el.muted = true
                    el.play();
                })
            }else{
                var div = document.createElement('div')
                var p = document.createElement('p')
                div.setAttribute('class', 'video-container')
                p.innerHTML = data.name
                const peerVdo = document.createElement('video')
                peerVdo.setAttribute('id', data.email)
                const displayVdo = document.getElementById('student-vdo-container')
                div.appendChild(peerVdo)
                div.appendChild(p)
                displayVdo.appendChild(div)
                peerVdo.srcObject = eve.streams[0];
                peerVdo.addEventListener('loadedmetadata', function (e) {
                    peerVdo.muted = true
                    peerVdo.play();
                })
            }
        },

        RemoveVdo : function(data){
            var el = document.getElementById(data.email)
                if(el){
                    console.log("Removed User vdo")
                    el.parentNode.parentNode.removeChild(el.parentNode)
                }
        },

        




        // ------------------------------------------------------------------
        // Clear the chat messages UI
        // ------------------------------------------------------------------

        clearChatMessages: () => $('#chat-msgs').html(''),

        // ------------------------------------------------------------------
        // Add a new chat message to the chat window.
        // ------------------------------------------------------------------

        displayChatMessage: (message) => {
            var n=names.includes(message.email)
            if(n==true)
            {
                //to store the chats for future use
                //check is email alredy exists
                if(chatHist[message.email]){
                    chatHist[message.email].push({
                        sender:message.sender,
                        text:message.text,
                        createdAt:message.createdAt
                    })
                    console.log('messge saved to history of guest')
                }else{
                    //msg from new email
                    chatHist[message.email] = [
                        {
                            sender:message.sender,
                            text:message.text,
                            createdAt:message.createdAt
                        }
                    ]
                    console.log('new message saved')
                }

            if (message.email === chat.currentRoom) {
                console.log(chat.messages)
                $('#chat-msgs').prepend(
                    `<tr>
                        <td>
                            <div class="sender" style="text-align:right;font-size:12px;"><strong>~ ${message.sender} @ <span class="date">${message.createdAt}</span></strong></div>
                            <div class="message">${message.text}</div>
                        </td>
                    </tr>`
                )
            }
        }
        else{
            console.log("not found");
        }


        },

        // ------------------------------------------------------------------
        // Update guest chat history  chatroom
        // ------------------------------------------------------------------
        updateChatHist: () =>{
            
            if(chatHist[chat.currentRoom]){
                chatHist[chat.currentRoom].map(item=>{
                    $('#chat-msgs').prepend(                    
                        `<tr>
                            <td>
                                <div class="sender" style="text-align:right;font-size:12px;"><strong>~ ${item.sender} @ <span class="date">${item.createdAt}</span></strong></div>
                                <div class="message">${item.text}</div>
                            </td>
                        </tr>`    
                    ) 
                })
            }else{
                //do nothing
            }
        },

        // ------------------------------------------------------------------
        // Select a new guest chatroom
        // ------------------------------------------------------------------

        loadChatRoom: evt => {
            chat.currentRoom = evt.target.dataset.roomId
            chat.currentChannel = evt.target.dataset.channelId
            console.log(chat)

            if (chat.currentRoom !== undefined) {
                $('.response').show()
                $('#room-title').text("Connected to "+evt.target.dataset.roomId+'2550')
            }

            evt.preventDefault()
            helpers.clearChatMessages()
            helpers.updateChatHist()

        },

        // ------------------------------------------------------------------
        // Reply a message
        // ------------------------------------------------------------------
        replyMessage: evt => {
            evt.preventDefault()

            let createdAt = new Date()
            createdAt = createdAt.toLocaleString()

            const message = $('#replyMessage input').val().trim()

            chat.subscribedChannels[chat.currentChannel].trigger('client-support-new-message', {
                'name': 'Admin',
                'email': chat.currentRoom,
                'text': message, 
                'createdAt': createdAt 
            });

            helpers.displayChatMessage({
                
                'email': chat.currentRoom,
                'sender': 'tea_name',
                'text': message, 
                'createdAt': createdAt
            })


            $('#replyMessage input').val('')
        },
    }


      // ------------------------------------------------------------------
      // Listen to the event that returns the details of a new guest user
      // ------------------------------------------------------------------

      generalChannel.bind('new-guest-details', function(data) {

        chat.subscribedChannels.push(pusher.subscribe('private-' + data.email));

        chat.subscribedUsers.push(data);

        // render the new list of subscribed users and clear the former
        $('#rooms').html("");
        chat.subscribedUsers.forEach(function (user, index) {
            var n1=names.includes(user.email)
            if(n1==true)
            {
        
                $('#rooms').append(
                    `<li class="nav-item"><a style="background-color: #f44336; color: white;padding:7px 7px; text-align: center;text-decoration: none; margin-bottom:4px;display:inline-block"  data-room-id="${user.email}" data-channel-id="${index}" class="nav-link" href="#">${user.name}</a></li>`
                )
            }
            else{
                console.log("Nothing")
            }
        })
    
      })

      

      // ------------------------------------------------------------------
      // Listen for a new message event from a guest
      // ------------------------------------------------------------------

      pusher.bind('client-guest-new-message', function(data){
          helpers.displayChatMessage(data)
      })

      //subscribe to private channels created by each user
        vdoInit.bind('new-call-details', (data)=>{
            console.log(data.email)
            console.log(names.includes(data.email))
            if(names.includes(data.email)){
                if(vdoChannel[data.email]){
                    console.log("Private channel alredy joined by admin")
                    vdoChannel[data.email].trigger("client-admin-ready", data)
                }else{
                    console.log('private channel join by admin')
                    console.log(data)
                    vdoChannel[data.email] = pusher.subscribe('private-'+data.email + '2550')
                    vdoChannel[data.email].bind("pusher:subscription_succeeded", ()=>{
                        console.log('ready emited')
                        vdoChannel[data.email].trigger("client-admin-ready", data)
                    })
                }
            }
            
            // emitRedy(data)
        })

        pusher.bind('client-set-offer', (data)=>{
            console.log('Creating answer')
            helpers.createAnswer(data)
        })

        pusher.bind('client-stu-ice', (data)=>{
            console.log(data.email)
            if(rtcConnections[data.email])
            {
                console.log('set student ice')
                let iceCandidate = new RTCIceCandidate(data['candidate'])
                rtcConnections[data.email].addIceCandidate(iceCandidate)
            }
        })


    // ----------------------------------------------------
    // Register page event listeners
    // ----------------------------------------------------

    chatReplyMessage.on('submit', helpers.replyMessage)
    chatRoomsList.on('click', 'li', helpers.loadChatRoom)

}())
