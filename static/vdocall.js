//start hear
let rtcPeerConnection
let upstream

const offerOptions = {
  offerToReceiveAudio: 0,
  offerToReceiveVideo: 1
}

// Contains the stun server URL we will be using.
let iceServers = {
  iceServers: [
    { urls: "stun:stun.services.mozilla.com" },
    { urls: "stun:stun.l.google.com:19302" },
  ],
};

//Initial  connection with the server
const socket = io.connect() 

socket.on('connect', ()=>{
  console.log('Student connected')
  //get the user media which can be stored in userstream for access
  navigator.mediaDevices.getUserMedia({
    audio:false,
    video: true
  })
  .then((stream)=>{
    console.log('gotMedia')
    upstream = stream
    const uservdo = document.getElementById('my-vdo')
    console.log(uservdo)
    uservdo.srcObject = stream
    uservdo.addEventListener('loadedmetadata' , function(e){
      // console.log('loding dttt')
      uservdo.muted = true
      uservdo.play()
    })
    socket.emit('join room', {'roomId':'2550'})
  })
  .catch(err=>{
  console.log(err.name)
  })
})

//This reply if admin checks student present
socket.on('is present', (data)=>{
  socket.emit('yes present', {'roomId':data['roomId']})
})

//Event fired when iceCandidate are redy to send
const OniceCandidateFunction = function(eve){
  console.log('Candidate sent to admin')
  if(eve.candidate != null){
    socket.emit('stu ice', {'roomId':'2550', 'candidate':eve.candidate})
  }
}

//If admin is present this event is fired
socket.on('ready', (data)=>{
  console.log('Creating offer')
  rtcPeerConnection = new RTCPeerConnection(iceServers)
  rtcPeerConnection.onicecandidate = OniceCandidateFunction
  rtcPeerConnection.addTrack(upstream.getTracks()[0], upstream)
  rtcPeerConnection.createOffer(offerOptions).then((offer)=>{
    console.log('created offer')
    console.log(offer)
    rtcPeerConnection.setLocalDescription(offer, 
      ()=>{
          console.log('it was successfull')
      },
      (eve)=>{
          console.log(eve)
      }
      )
    socket.emit('stu offer', {'roomId':data['roomId'], 'offer':offer, 'sid':data['sid']})
  })
})

//Set the admin answer as Remotedescription
socket.on('set ans', (data)=>{
  console.log('Setting ans')
  rtcPeerConnection.setRemoteDescription(data['answer'])
})

//Sets iceCandidate received by admin
socket.on('set admin ice', (data)=>{
  console.log('Setting admin ice')
  let iceCandidate = new RTCIceCandidate(data['candidate'])
  rtcPeerConnection.addIceCandidate(iceCandidate)

})
