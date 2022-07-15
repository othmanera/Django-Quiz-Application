console.log('hello quiz')
const url = window.location.href

const quizdiv=document.getElementById('quiz-div')
const scorediv=document.getElementById('score-div')
const resultdiv=document.getElementById('result-div')


const timerBox = document.getElementById('timer-box')

const Timer  = (time) =>{

    if(time.toString().length < 2){
        timerBox.innerHTML += `<b>0${time}:00</b>`

    } else{
        timerBox.innerHTML += `<b>${time}:00</b>`
    }
    let minutes = time -1
    let seconds = 60
    let displaySec 
    let displayMin 
    
    const timer = setInterval(()=>{
        seconds--
        if (seconds <0 ){
            seconds = 59
            minutes--
            
        }
        if(minutes.toString().length <2){
            displayMin = '0' +minutes 
        }
        else{
                displayMin = minutes 
            }
            
        if (seconds.toString() <2){
            displaySec = '0' + seconds
        }
        else{
            displaySec = seconds
        }

        if (minutes == 0 && seconds == 0){
           timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
            clearInterval(timer)
            alert('Time is up !')
            sendData()

           }, 500)

        }
        timerBox.innerHTML = `<b>${displayMin}:${displaySec}</b>`
    },1000)
}



$.ajax({
    type: 'GET',
    url: `${url}data`,

    success: function(response){
        // console.log(response)
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                quizdiv.innerHTML+=`
                    <div class="mb-2">
                    <hr>
                        <b> ${question} </b>
                    </div>
                `
                answers.forEach(answer=>{
                    quizdiv.innerHTML+=`
                    <div >
                    <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}" >
                       <label for="${question}">${answer}</label>
                    </div>
                    
                    `
                })
            }
            
        });
        Timer(response.time)
        
 


    },
    error: function(error){
        console.log(error)
    } 
})


const quizForm=document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData=()=>{
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=> {
        if (el.checked){
            data[el.name]= el.value
        }
        else{
            if (!data[el.name]){
                data[el.name] = null
            }
        }

    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            // console.log(response)
            const results = response.results
            quizForm.classList.add('not-visible')
            
            
            scorediv.innerHTML = ` Your score is ${response.score} out of 10`
            

            results.forEach(res=>{
                const resDiv = document.createElement("div")
                for (const [question , resp ] of Object.entries(res)){
                // console.log(question)
                // console.log(resp)
                // console.log('------')
                

                    resDiv.innerHTML += question
                    const cls=['container','p-3','text-light','h5']

                    resDiv.classList.add(...cls)

                    if (resp == 'not answered'){
                        resDiv.innerHTML += ' -not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else{
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                       if (answer == correct){
                           resDiv.classList.add('bg-success')
                           resDiv.innerHTML += ` Your answer: ${answer} `
                       }
                       else{
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer: ${correct}`
                            resDiv.innerHTML += ` | Your answer : ${answer}`
                        }
                    }
                }

                resultdiv.append(resDiv)
            })
            

                
        },

        error: function(error){
            console.log(error)
        }
        
    })
}

 
quizForm.addEventListener('submit' , e=>{
    e.preventDefault()
    
    sendData()
})







// ----------------------------------


