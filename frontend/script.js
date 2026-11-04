const bugsList = document.getElementById("bugs-list")
const formMessage = document.getElementById("form-message")

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
        title.textContent = `Tytuł: ${bug.title}`;
        bugCard.appendChild(title);        

        const priority = document.createElement("p");
        priority.textContent = `Priorytet: ${bug.priority}`;
        bugCard.appendChild(priority);

        const status = document.createElement("p");
        status.textContent = `Status: ${bug.status}`;
        bugCard.appendChild(status);

        const description = document.createElement("p");
        description.textContent = `Description: ${bug.description}`;
        bugCard.appendChild(description);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = `Usuń bug`;

        deleteButton.addEventListener("click", () => {
            deleteBug(bug.id)
        });

        bugCard.appendChild(deleteButton);

        bugsList.appendChild(bugCard);
    }
}

async function createBug(){

    formMessage.textContent = "";
     
    const titleInput = document.getElementById("title");
    console.log(titleInput.value);

    const descriptionInput = document.getElementById("description");
    console.log(descriptionInput.value);

    const priorityInput = document.getElementById("priority");
    console.log(priorityInput.value);

    const bugData = {
        title: titleInput.value,
        description: descriptionInput.value,
        priority: priorityInput.value
    };

    /*
    if (priorityInput.value === "") {
        console.log("Wybierz priorytet!");
        formMessage.textContent = "Wybierz priorytet!";
        return;
    }    
        */

    const response = await fetch("http://127.0.0.1:8000/bugs",{
        method: "POST",
        headers: {
            "Content-Type": "application/json" //informujemy backend, że wysyłamy JSON
        },
        body: JSON.stringify(bugData) //zamienamy obiekt JS na tekst JSON
    });

    if (response.ok) {
        console.log("Zgłoszenie dodane");
        await loadBugs();
        titleInput.value = "";
        descriptionInput.value = "";
        priorityInput.value = "";
        formMessage.textContent = "Zgłoszenie dodane";
    }
    else{
        //console.log("Nie udało się dodać zgłoszenia");
        //formMessage.textContent = "Nie udało się dodać zgłoszenia";
        
        const errorData = await response.json();
        console.log("Błędy z API:", errorData)
        //console.log(errorData.detail[0].msg);
        //formMessage.textContent = errorData.detail[0].msg;

        formMessage.textContent = "";

        for (const message of errorData.detail){
            formMessage.textContent += message.msg + "\n";            
        }
    }
}

async function deleteBug(id){
    const response = await fetch(`http://127.0.0.1:8000/bugs/${id}`,{
        method: "DELETE"
    });

    if (response.ok){
        await loadBugs();
    }
}

loadBugs()

const refreshButton = document.getElementById("refresh-button");
refreshButton.addEventListener("click", loadBugs);

const addButton = document.getElementById("add-button");
addButton.addEventListener("click", createBug);