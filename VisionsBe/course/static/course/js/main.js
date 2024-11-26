const tooltips = document.querySelectorAll(".all-tooltips .mytooltip");
const fullDiv = document.querySelector("section");
const container = document.querySelector(".mycontainer");

let timeoutId;
window.addEventListener("resize", contentPosition);
window.addEventListener("DOMContentLoaded", contentPosition);

function contentPosition() {
  tooltips.forEach((tooltip) => {
    const pin = tooltip.querySelector(".pin");
    const content = tooltip.querySelector(".tooltip-content");
    const arrow = tooltip.querySelector(".arrow");
    content.style.left = pin.offsetWidth + "px";
    content.style.top = pin.offsetTop + "px";
    arrow.style.left = pin.offsetLeft - 5 + 'px';
    arrow.style.top =  content.offsetHeight/2 -pin.offsetHeight/2 + "px";
  })
}

tooltips.forEach(tooltip =>{
  const pin = tooltip.querySelector(".pin");
  const content = tooltip.querySelector(".tooltip-content");
  pin.addEventListener('mousemove', () =>{
    tooltip.classList.add('active');
  })
  pin.addEventListener('mouseleave', () =>{
    timeoutId = setTimeout(()=>{
      tooltip.classList.remove('active');
    }, 1000)
  })
  content.addEventListener('mousemove', ()=>{
    clearTimeout(timeoutId);
    tooltip.classList.add('active');
  })
  content.addEventListener('mouseleave', () =>{
    timeoutId = setTimeout(()=>{
      tooltip.classList.remove('active');
    }, 1000)
  })
})