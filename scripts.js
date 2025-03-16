const attractions = document.querySelector('.attractions');


const attraction = document.createElement('div');
attraction.classList.add('attraction');

attractions.appendChild(attraction);

async function fetchAttractions() {
    let reponse = await fetch('api/attractions', {method: 'GET'});
    if (Response.ok) {
        
    }

}