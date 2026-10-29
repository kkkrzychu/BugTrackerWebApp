const bugsList = document.getElementById("bugs-list")

async function loadBugs(){    

    const response = await fetch("http://127.0.0.1:8000/bugs");

    const bugs = await response.json();

    bugsList.innerHTML = "";

    if (bugs.length === 0){
        bugsList.innerHTML = "<p>Brak zgłoszeń</p>"
    }

    for (const bug of bugs){

        const bugCard = document.createElement("div");
        bugCard.classList.add("bug-card");

        const title = document.createElement("h3");        
        title.textContent = bug.title;
        bugCard.appendChild(title);        

        const priority = document.createElement("p");
        priority.textContent = bug.priority;
        bugCard.appendChild(priority);

        const status = document.createElement("p");
        status.textContent = bug.status;
        bugCard.appendChild(status);

        bugsList.appendChild(bugCard);
    }
}

loadBugs()

const refreshButton = document.getElementById("refresh-button");

refreshButton.addEventListener("click", loadBugs);

