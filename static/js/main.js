const generateBtn = document.querySelector('#generateBtn')

generateBtn.addEventListener('click', async () => {
    const youtubeLink = document.querySelector('#youtubeLink').value
    const blogContent = document.querySelector('#blogContent')
    const loadingCircle = document.querySelector('#loadingCircle')

    if(youtubeLink) {
        loadingCircle.classList.toggle('hidden')
        loadingCircle.classList.toggle('block')
        blogContent.innerText = ''

        const endpoint = '/generate-blog'

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ link: youtubeLink })
            })
             
            const data = await response.json()
            
            blogContent.innerHTML = data.content
            
        } catch (error) {
            console.log(error);
            alert("Error occurred")
        }

        loadingCircle.classList.toggle('hidden')
        loadingCircle.classList.toggle('block')
    }
    else{
        alert("Enter a youtube link")
    }
})