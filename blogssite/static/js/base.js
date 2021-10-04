console.log("hello world");

window.scroll({
    behavior:'smooth',
});
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });

const top_btn = document.querySelector('.top-btn');
const navBtn = document.querySelector('.menu-container');
const toggleBtn = document.querySelector('.toggle');
const year_field = document.querySelector('.year');
console.log(top_btn);
let year = new Date().getFullYear() ;

year_field.innerHTML = year ; 

top_btn.addEventListener("click",() =>
{
    window.scroll({
        top:0,
        left:0,
        behavior:'smooth'
    });
})


toggleBtn.addEventListener("click",() =>
{
    if(toggleBtn.classList.contains('active'))
    {
        toggleBtn.innerHTML = '<i class="fas fa-chevron-right"></i>' ;
        toggleBtn.classList.remove('active');
        navBtn.style.width = '230px';

    }
    else
    {
        toggleBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
        toggleBtn.classList.add('active');
        navBtn.style.width = null;
    }
})

