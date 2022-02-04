import jsonFormatHighlight from 'https://cdn.skypack.dev/json-format-highlight';

const status = document.getElementById('status');
const jsonElement = document.getElementById('json');
const form = document.getElementById('form');

jsonElement.innerHTML = jsonFormatHighlight(JSON.parse(jsonElement.textContent))

form.addEventListener('submit', (e) => {
    if (!form.checkValidity()) return

    e.preventDefault()


    const baseUrl = form.endpoint.getAttribute('data-base-url');
    const endpoint = form.endpoint.value

    form.submit.classList.add('is-loading')

    fetch(`${baseUrl}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`)
        .then(response => {
            status.textContent = `${response.status} ${response.statusText}`

            if (response.ok) {
                status.classList.remove('has-text-danger')
                status.classList.add('has-text-success')
            } else {
                status.classList.remove('has-text-success')
                status.classList.add('has-text-danger')

            }

            return response.json()
        })
        .then(data => {
            jsonElement.classList.remove("has-text-danger")
            jsonElement.innerHTML = jsonFormatHighlight(data)
        })
        .catch(error => {
            console.error(error);
            jsonElement.classList.add("has-text-danger")
            jsonElement.textContent = error.message
        })
        .finally(() => {
            form.submit.classList.remove('is-loading')
        })
})