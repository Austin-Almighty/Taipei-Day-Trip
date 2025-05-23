const attractions = document.querySelector('.attractions');
const listBar = document.querySelector('.list-bar');

let nextPage = 0;
let keyword = null;

const searchBox = document.getElementById('searchBox');
const searchIcon = document.getElementById('searchIcon');
const searchImage = document.getElementById('searchImage');
const searchForm = document.getElementById('searchForm');



const footer = document.querySelector('footer');
const gridDiv = document.querySelector('.grid');

function performSearch() {
    let searchKeyword = searchBox.value.trim();
    nextPage = 0;
    keyword = searchKeyword;
    footer.classList.add("hidden");
    gridDiv.innerHTML = '';
    footer.classList.remove("footer-animate");
    void footer.offsetWidth; // Force reflow
    footer.classList.remove("hidden");
    footer.classList.add("footer-animate");
    setTimeout(()=>{
      loadNextPage();
    }, 10)
    
  }


searchIcon.addEventListener('click', performSearch)
searchImage.addEventListener('click', performSearch)
searchBox.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); 
      performSearch();
    }
  });



async function renderStation(station) {
    const addMRT = document.createElement('div');
    addMRT.classList.add('stations');
    addMRT.textContent = station;
    addMRT.addEventListener('click', ()=>{
        nextPage = 0;
        keyword = station;
        footer.classList.add("hidden");
        gridDiv.innerHTML = '';
        footer.classList.remove("footer-animate");
        void footer.offsetWidth; // Force reflow
        footer.classList.remove("hidden");
        footer.classList.add("footer-animate");
        setTimeout(()=>{
      loadNextPage();
    }, 10)

    })
    listBar.appendChild(addMRT);
}

async function fetchStations() {
    let response = await fetch('api/mrts', {method: 'GET'});
    if (response.ok) {
        let data = await response.json();
        for (station of data.data) {
            renderStation(station["mrt"]);
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


async function fetchAttractions(page, keyword = null) {

    let endpoint = `api/attractions?page=${page}`;
    if (keyword !== null) {
        endpoint += `&keyword=${keyword}`;
    }
    let response = await fetch(endpoint, {method: 'GET'});
    if (response.ok) {
        let data = await response.json();
        return data;
    } else {
        console.log('Cannot reach API endpoints.');
    }
}

async function renderAttractions() {
    if (nextPage === null) {
      return;
    }
    const data = await fetchAttractions(nextPage, keyword);
    const dataArray = await data.data;
    nextPage = data.nextPage;
    const length = dataArray.length
    const gridDiv = document.querySelector('.grid');
    for (let i=0; i<length; i++) {
        const link = document.createElement('a');
        link.href=`/attraction/${dataArray[i].id}`;

        const locationDiv = document.createElement("div");
        locationDiv.classList.add("locationCard");

        const img = document.createElement("img");
        img.src = JSON.parse(dataArray[i].images)[0];

        const attractionName = document.createElement("div");
        attractionName.classList.add("attractionName");
        attractionName.textContent = dataArray[i].name;
        if (dataArray[i].name.length >=16) {
            attractionName.style.fontSize = "15px";
        }

        const attractionInfo = document.createElement("div");
        attractionInfo.classList.add("attractionInfo");

        const station = document.createElement("div");
        station.classList.add("station");
        station.textContent = dataArray[i].mrt;

        const category = document.createElement("div");
        category.classList.add("category");
        category.textContent = dataArray[i].category;

        attractionInfo.appendChild(station);
        attractionInfo.appendChild(category);

        locationDiv.appendChild(img);
        locationDiv.appendChild(attractionName);
        locationDiv.appendChild(attractionInfo);

        link.appendChild(locationDiv);
        gridDiv.appendChild(link);

        
    }
}

let isFetching = false;

async function loadNextPage() {
  if (isFetching) return; 
  isFetching = true;
  await renderAttractions();
  isFetching = false;
}




async function observeBottom(){
  const observer = new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if (entry.isIntersecting) loadNextPage();
    }, {
      threshold: 1
    }
  );
  });

  const sentinel = document.getElementById("sentinel");
  observer.observe(sentinel);
}

document.addEventListener("DOMContentLoaded", observeBottom);



