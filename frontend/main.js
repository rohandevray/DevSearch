let projectsUrl = "http://127.0.0.1:8000/api/projects/"
let baseUrl = "http://127.0.0.1:8000"

let getProjects = () => {
    fetch(projectsUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildProjects(data)
        })
}


let buildProjects = (projects) =>{
    let projectwrapper = document.getElementById('projects--wrapper')
    projectwrapper.innerHTML = ''
    for(let i=0 ; i < projects.length ; i++){
        let project = projects[i]
        
        // i am not a loser and i will prevail for sure its not over until i win 
        let projectCard = `
            <div class="project--card">
              <img src="${baseUrl}${project.featured_image}" />
              <div>
                 <div class="card--header">
                   <h3>${project.title}</h3>
                   <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                   <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                 </div>
                 <i>${project.vote_ratio}% Positive Feedback</i>
                  <p>${project.description.substring(0,150)}</p>

              </div>

              <h3>${project.title}</h3> 
            </div>
        `
        projectwrapper.innerHTML += projectCard
    }
     
    addVoteBtns()

   

}


let addVoteBtns = () =>{
   let voteBtns = document.getElementsByClassName('vote--option')
   for(let i=0 ;i < voteBtns.length ;i++){
      
      voteBtns[i].addEventListener('click' , (e)=>{
         let vote = e.target.dataset.vote
         let project = e.target.dataset.project
         let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcwOTUxMjQ1LCJpYXQiOjE2NzA4NjQ4NDUsImp0aSI6ImI5OGE1NDkyNDc1OTQ4OTNhNjA0ZTk0OTRmMjk0YTRmIiwidXNlcl9pZCI6MjF9.mLdXCokqVxIuBJUFdVLE62raM_WxM-4MrISpHdcjlbc"

        
         fetch(`${projectsUrl}${project}/vote/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                 Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ 'value': vote })

         }).then(response => response.json())
           .then(data => {
             console.log('Success:', data)
             
           })
         
          
      })

   }


}

getProjects()

