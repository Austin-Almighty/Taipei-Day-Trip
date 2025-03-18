const attractions = document.querySelector('.attractions');
const listBar = document.querySelector('.list-bar');

async function renderStation(station) {
    const addMRT = document.createElement('div');
    addMRT.classList.add('stations');
    addMRT.textContent = station;
    listBar.appendChild(addMRT);
    return;
}

async function fetchStations() {
    let response = await fetch('api/mrts', {method: 'GET'});
    if (response.ok) {
        let data = await response.json();
        for (station of data.data) {
            renderStation(station);
        }
    } else {
        console.log('Unable to fetch station names');
    }
}
fetchStations();

function scrollClick(container, scrollDistance) {
    container.scrollBy({ left: scrollDistance, behavior: 'smooth' });
  }

const leftScroll = document.getElementById('leftClick');
const rightScroll = document.getElementById('rightClick');

leftScroll.addEventListener('click', ()=>scrollClick(listBar, -30));
rightScroll.addEventListener('click', ()=>scrollClick(listBar, 30));


// async function fetchAttractions() {
//     let response = await fetch('api/attractions/?page=1', {method: 'GET'});
//     if (response.ok) {
//         let data = await response.json();
//         console.log(data);
//     }

// }

