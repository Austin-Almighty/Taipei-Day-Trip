function scrollClick(container, scrollDistance) {
    container.scrollBy({ left: scrollDistance, behavior: 'smooth' });
  }

const slider = document.querySelector(".slider");
const leftArrow = document.getElementById("leftArrow");
const rightArrow = document.getElementById("rightArrow");

leftArrow.addEventListener('click', ()=>scrollClick(slider, -50));
rightArrow.addEventListener('click', ()=>scrollClick(slider, 50));

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


