import jsonFormatHighlight from 'https://cdn.skypack.dev/json-format-highlight';

const button = document.getElementById('button');
const avatar = document.getElementById('avatar');
const name = document.getElementById('name');
const email = document.getElementById('email');
const jsonData = document.getElementById('json-data');

jsonData.innerHTML = jsonFormatHighlight(JSON.parse(jsonData.textContent))

const handleClick = () => {
    button.classList.add("is-loading");

    fetch('/api/random/user')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            avatar.src = data.avatar;
            avatar.alt = data.name;
            name.textContent = data.name;
            email.textContent = data.email;
            jsonData.innerHTML = jsonFormatHighlight(data)

            button.classList.remove("is-loading");
        });
}

button.addEventListener("click", handleClick)