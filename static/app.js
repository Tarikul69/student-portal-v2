window.onload = function () {
  show(0);
};

let questionso = [
  {
    id: 1,
    question: "What is the full form of RAM ?",
    answer: "Random Access Memory",
    options: [
      "Random Access Memory",
      "Randomely Access Memory",
      "Run Aceapt Memory",
      "None of these",
    ],
  },
  {
    id: 2,
    question: "What is the full form of CPU?",
    answer: "Central Processing Unit",
    options: [
      "Central Program Unit",
      "Central Processing Unit",
      "Central Preload Unit",
      "None of these",
    ],
  },
  {
    id: 3,
    question: "What is the full form of E-mail",
    answer: "Electronic Mail",
    options: [
      "Electronic Mail",
      "Electric Mail",
      "Engine Mail",
      "None of these",
    ],
  },
];

const submitForm = (e) => {
  e.preventDefault();
  console.log("form submitted !!");
  let name = document.forms["welcome-forms"]["name"].value;

  sessionStorage.setItem("name", name);
  location.href = "./Questions/quiz";
  console.log(name);
};

let questionCount = 0;
let point = 0;

const next = () => {
  let userAnswer = document.querySelector("li.option.active").innerHTML;
  // check user answer
  if (userAnswer == questions[questionCount].answer) {
    console.log("right answer");
    point += 10;
    sessionStorage.setItem("points", point);
  } else {
    console.log("wrong answer");
  }

  if (questionCount == questions.length - 1) {
    sessionStorage.setItem("time", `${minutes} minutes and ${seconds} seconds`);
    clearInterval(mytime);

    location.href = "./end.html";
    return;
  }

  console.log(userAnswer);

  questionCount++;
  show(questionCount);
};

function show(count) {
  let question = document.getElementById("questions");
  // question.innerHTML = "<h2>" + questions[count].question + "</h2>";

  question.innerHTML = `
  <h1>Q${questionCount + 1}. ${questions[count].question}</h1>
  <ul class="option-group">
              <li class="option ">${questions[count].options[0]}</li>
              <li class="option">${questions[count].options[1]}</li>
              <li class="option">${questions[count].options[2]}</li>
              <li class="option">${questions[count].options[3]}</li>
            </ul> 
  `;

  toggleActive();
}

function toggleActive() {
  let option = document.querySelectorAll("li.option");

  for (let i = 0; i < option.length; i++) {
    option[i].onclick = function () {
      for (let j = 0; j < option.length; j++) {
        if (option[j].classList.contains("active")) {
          option[j].classList.remove("active");
        }
      }
      option[i].classList.add("active");
    };
  }
}

// ----------------------------------------------------
// Start vdo of student
// ----------------------------------------------------
        

// function startVdo(){
//   navigator.mediaDevices
//     .getUserMedia({
//       audio:true,
//       video: { width: 1280, height: 720 }
//     })
//     .then((stream)=>{
//       userStream = stream
//       const uservdo = vdoWindow.find('#my-vdo')
//       uservdo.srcObject = stream
//       uservdo.onloadmetadata = function(e){
//           uservdo.play()
//       }
//   })
// }

// //get the div element where to show vdo of user

// // const vdoWindow = $('.disp-vdo')
// // vdoWindow.find('#start-vdo').on('click', startVdo)
