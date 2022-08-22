// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-app.js";
import {getDatabase, ref, set, child, update, remove} from "https://www.gstatic.com/firebasejs/9.4.0/firebase-database.js"

const quizBox = document.querySelector(".quiz_box");
const nextBtn = document.querySelector("footer .next_btn");
const bottom_ques_counter = document.querySelector("footer .total_que");
const optionList = document.querySelector(".option_list");


const range_btn = document.querySelector('.range_btn');
const names = document.querySelector('.names');
const age = document.querySelector('.age');
const age_btn = document.querySelectorAll('.age_btn button');
const gender = document.querySelector('.gender');
const gender_btn = document.querySelectorAll('.gender_btn button');
const student = document.querySelector('.student');
const student_btn = document.querySelectorAll('.student_btn button');

var disp = document.getElementById('quiz_box');

let counter;
let counterLine;
let que_count = 0;
let que_numb = 0;
let widthValue = 0;
let sumIA = 0;
let sumHappy = 0;
let sumSE = 0;
let increment = Math.floor(Math.random() * 10);

var answers= {};
var wartosc= null;

// object with respondent's data
const participant = {
    age: null,
    gender: null,
    student: null,
    ansIA: null,
    ansHappy: null,
    ansSE: null
}


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    //add your web app info from your firebase
  apiKey: 
  authDomain: 
  databaseURL: 
  projectId: 
  storageBucket: 
  messagingSenderId: 
  appId: 
  measurementId: 
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
//const analytics = getAnalytics(app);
const db = getDatabase();
function InsertData(){
    const time = Date.now();
    set(ref(db, "user/" + time + "/ respondent/"),{
        ID: time,
        Age: participant.age,
        Gender: participant.gender,
        Student: participant.student,
        Answers1: answers,
        
    })
    set(ref(db, "user/" + time + "/ samoocena/" ),{
        ID: time,
        AnsSE: participant.ansSE
        
    })
    set(ref(db, "user/" + time + "/ uzaleznienie/" ),{
        ID: time,
        AnsIA: participant.ansIA,
        
    })
    set(ref(db, "user/" + time + "/ zadowolenie/" ),{
        ID: time,
        AnsHAPPY: participant.ansHappy,
        
    })
    .then(()=>{
        alert("Dziękujemy za wypełnienie ankiety");
    })
    .catch((error)=>{
        alert("unsuccessfull, error" + error);
    });
}


nextBtn.onclick = () => {
    

    if (ifSelected() == false) {
        console.log("false");
        alert("Please select all options")
        // all options need to be chosen

    } else if (ifSelected() == true) {
        
        clearDom();
        if (que_count == 0) {
            displayQuestion1();
            saveOptAnswers();
        } else if (que_count != 0) {
            if (ifOptSelected() == false) {
                console.log('false');
                alert("Please select an option")
                // questions in questions.js start from 1

            } else if (ifOptSelected() === true) {
                if (que_count < questions.length) {
                    displayQuestion1();
                    saveOptAnswers();

                }else{
                    wartosc = Object.values(answers);
                    for( var i = 0; i < wartosc.length; i++){
                        compareS(wartosc[i]);
                        participant.ansIA = sumIA;
                        participant.ansHappy = sumHappy;
                        participant.ansSE = sumSE;
                    }
                    console.log(participant.age, participant.gender, participant.student, answers, participant.ansIA, participant.ansHappy, participant.ansSE);
                    InsertData();
                    
                }
            }
        }
    }

}



function clearDom() {

    // clears unwanted elements
    optionList.style.display = "flex"
    age.remove("show");
    age_btn.forEach(btn => btn.remove("show"));
    gender.remove("show");
    gender_btn.forEach(btn => btn.remove("show"));
    student.remove("show");
    student_btn.forEach(btn => btn.remove("show"));
}

function displayQuestion1() {
    que_numb++;
    showQuetions(que_count);
    que_count++;
    queCounter(que_numb);
    clearInterval(counter);
    clearInterval(counterLine);
}



function savePersonAnswers() {
    // adds an event listener to every button
    age_btn.forEach(btn => btn.addEventListener('click', () => {

        // clears previous option if a new one was selected
        age_btn.forEach(btn => btn.removeAttribute('id', 'selected'))
        // gives selected effect
        btn.setAttribute('id', 'selected')

        // saves chosen option
        participant.age = btn.innerHTML

    }))

    gender_btn.forEach(btn => btn.addEventListener('click', () => {
        gender_btn.forEach(btn => btn.removeAttribute('id', 'selected'))
        btn.setAttribute('id', 'selected')
        participant.gender = btn.innerHTML

    }))

    student_btn.forEach(btn => btn.addEventListener('click', () => {
        student_btn.forEach(btn => btn.removeAttribute('id', 'selected'))
        btn.setAttribute('id', 'selected')
        if (btn.innerHTML == 'Tak') {
            participant.student = true
        } else {
            participant.student = false
        }

    }))
}

function ifSelected() {
    // if any option wasn't selected then returns false
    if (participant.age === null || participant.gender === null || participant.student === null) {
        return false
    } else return true
}


function ifOptSelected() {
    // if any option wasn't selected then returns false
        if (answers[questions[que_count - 1].numb] === undefined) {
        return false
    } else return true
}

function showQuetions(index) {
    // clears previous question
    optionList.innerHTML = ""
    // adds question in "title"
    const que_text = document.querySelector(".que_text");
    let que_tag = `${questions[index].numb}. ${questions[index].question}`
    que_text.innerHTML = que_tag;

    //shows answers from an array
    for ( var i = 0; i < questions[index].options.length; i++) {

        let optionEl = document.createElement("option")
        let optionTag = `${questions[index].options[i]}`
        optionEl.innerHTML = optionTag;
        optionEl.classList.add("option")
        optionEl.setAttribute('id', 'option-element')
        optionList.appendChild(optionEl)
    }
}




function queCounter(index) {
    //Updates Question Counter
    let totalQueCounTag = `${index} z ${questions.length}`;
    bottom_ques_counter.innerHTML = totalQueCounTag;
}

function saveOptAnswers() {
    const optionElement = document.querySelectorAll('#option-element')

    // Assignes choosen option to object
    optionElement.forEach(element => element.addEventListener('click', () => {
        // -1 because questions start from 1
        answers[questions[que_count - 1].numb] = element.innerHTML
    }))

    // Adds class to selected option
    optionElement.forEach(btn => btn.addEventListener('click', () => {
        optionElement.forEach(btn => btn.removeAttribute('id', 'selected'))
        btn.setAttribute('id', 'selected')
    }))

}

function compareS(odp){
    //odp na IA
    var stringNever = "Nigdy";
    var stringVrarely = "Bardzo rzadko";
    var stringRarely = "Rzadko";
    var stringSometimes = "Czasami";
    var stringOften = "Często";
    var stringVoften = "Bardzo często";
    var stringAlways = "Zawsze";
    //odp na depresje

    //odp na self esteem
    var stringSz = "Stanowczo się zgadzam";
    var stringZ = "Zgadzam się";
    var stringNmz = "Nie mam zdania";
    var stringNzs = "Nie zgadzam się";
    var stringSnz = "Stanowczo się nie zgadzam";

    var stringX = "Bardzo nieszczęsliwy/a";
    var stringX1 ="Trochę nieszczęśliwy/a";
    var stringX2 ="Obojętny/a";
    var stringX3 ="Trochę szczęśliwy/a";
    var stringX4 ="Bardzo szczęśliwy/a";

    var stringY ="Zdecydowanie się z nim nie identyfikuję";
    var stringY1 ="Raczej się z nim nie identyfikuję";
    var stringY2 ="Nie potrafię określić";
    var stringY3 ="Uważam, że częściowo mam takie samo nastawienie";
    var stringY4 ="Zdecydowanie się z nim identyfikuję";

    var string = odp.toString();
    var stringk = '.';

    if(stringNever == string){
        sumIA += 1;
    }else if(stringVrarely == string){
        sumIA += 2;
    }else if(stringRarely == string){
        sumIA += 3;
    }else if(stringSometimes == string){
        sumIA += 4;
    }else if(stringOften == string){
        sumIA += 5;
    }else if(stringVoften == string){
        sumIA += 6;
    }else if(stringAlways == string){
        sumIA += 7;
    }

    if(stringSnz == string){
        sumSE += 1;
    }else if(stringNzs == string){
        sumSE += 2;
    }else if(stringZ == string){
        sumSE += 3;
    }else if(stringSz == string){
        sumSE += 4;
    }

    if(stringSnz.concat(stringk) == string){
        sumSE += 4;
    }else if(stringNzs.concat(stringk) == string){
        sumSE += 3;
    }else if(stringZ.concat(stringk) == string){
        sumSE += 2;
    }else if(stringSz.concat(stringk) == string){
        sumSE += 1;
    }

    if(stringX == string){
        sumHappy += 1;
    }else if(stringX1 == string){
        sumHappy += 2;
    }else if(stringX3 == string){
        sumHappy += 3;
    }else if(stringX4 == string){
        sumHappy += 4;
    }

    if(stringY == string){
        sumHappy += 1;
    }else if(stringY1 == string){
        sumHappy += 2;
    }else if(stringY3 == string){
        sumHappy += 3;
    }else if(stringY4 == string){
        sumHappy += 4;
    }

    if(stringY.concat(stringk) == string){
        sumHappy += 4;
    }else if(stringY1.concat(stringk) == string){
        sumHappy += 3;
    }else if(stringY3.concat(stringk) == string){
        sumHappy += 2;
    }else if(stringY4.concat(stringk) == string){
        sumHappy += 1;
    }

}
savePersonAnswers();
