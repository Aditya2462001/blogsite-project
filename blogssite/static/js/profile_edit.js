const img_field = document.querySelector(".input-image");
const prev_img = document.querySelector(".preview-img");
const file_name = document.querySelector('.file-name');
const click_btn = document.querySelector('.click-btn');


click_btn.addEventListener("click",() =>
{
    img_field.click();
})

img_field.addEventListener("change",(e) =>
{
    // console.log(e.target.files[0]);
    file_name.innerHTML = e.target.files[0].name ;
    const file = new FileReader();

    file.onload = (e) =>
    {
        prev_img.value = e.target.result ;
        prev_img.src = e.target.result ;
        
    }
    file.readAsDataURL(e.target.files[0]);
    
})