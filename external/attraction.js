let id = "";

function setId() {
  let urlPath = window.location.pathname;
  let path = urlPath.split('/');
  id = path[path.length - 1];
}

if (document.readyState === "loading") {
  window.addEventListener('DOMContentLoaded', setId);
} else {
  setId();
}

async function fetchAPI(){
  let endpoint = `/api/attraction/${id}`;
  let response = await fetch(endpoint, {method: "GET"});
  let data = await response.json();
  let dataArray = data.data;
  console.log(dataArray);
  return dataArray;
}



async function renderAPI(){
  let data = await fetchAPI();
  let imgArray = JSON.parse(data.images);
  for (let i=0; i<imgArray.length; i++){
    const newImg = document.createElement('img');
    newImg.src = imgArray[i];
    newImg.id = `slide${i}`;
    const slider = document.querySelector('.slider');
    slider.appendChild(newImg);
    const newNav = document.createElement('a');
    newNav.href = `#slide${i}`;
    const sliderNav = document.querySelector('.slider-nav');
    sliderNav.appendChild(newNav);
  }
  setupObserver();

  const name = document.getElementById('name');
  const nameH3 = document.createElement('h3');
  nameH3.textContent = data.name;
  name.insertAdjacentElement('afterbegin', nameH3);

  const subtitle = document.getElementById('subtitle');
  const category = document.createElement('span');
  category.id = 'category';
  category.textContent = data.category;
  subtitle.insertAdjacentElement('afterbegin', category);

  const station = document.createElement('span');
  station.id = 'station';
  station.textContent = data.mrt;
  subtitle.appendChild(station);

  const overview = document.querySelector('section');
  const address = document.getElementById('address');
  const transport = document.getElementById('transport');

  const intro = document.createElement('p');
  intro.textContent = data.description;
  overview.insertAdjacentElement('afterbegin', intro);

  const addressDetail = document.createElement('p');
  addressDetail.textContent = data.address;
  address.insertAdjacentElement('afterend', addressDetail);

  const transportDetail = document.createElement('p');
  transportDetail.textContent = data.transport;
  transport.insertAdjacentElement('afterend', transportDetail);
}



function scrollClick(container, scrollDistance) {
    container.scrollBy({ left: scrollDistance, behavior: 'smooth' });
  }

const slider = document.querySelector(".slider");
const leftArrow = document.getElementById("leftArrow");
const rightArrow = document.getElementById("rightArrow");

leftArrow.addEventListener('click', ()=>scrollClick(slider, -540));
rightArrow.addEventListener('click', ()=>scrollClick(slider, 540));




function setupObserver(){
  const slides = document.querySelectorAll('.slider img');
  const navLinks = document.querySelectorAll('.slider-nav a');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const slideId = entry.target.id;
      const correspondingLink = document.querySelector(`.slider-nav a[href="#${slideId}"]`);
      if (entry.isIntersecting) {
        navLinks.forEach(link => link.classList.remove('selected'));
        correspondingLink.classList.add('selected');
      }
    });
  }, {
    threshold: 0.5
  });

  slides.forEach(slide => observer.observe(slide));
}




const morning = document.getElementById('morning');
const afternoon = document.getElementById('afternoon');
const cost = document.getElementById('cost');
const radioButtons = document.querySelectorAll('input[name="radioPicker"]');

radioButtons.forEach(option => {
  option.addEventListener('change', ()=> {
    if (morning.checked) {
      cost.textContent = "新台幣2000元";

    } else {
      cost.textContent = "新台幣2500元";
    }
  })
})

window.addEventListener('DOMContentLoaded', renderAPI);
