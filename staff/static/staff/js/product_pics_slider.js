document.addEventListener('DOMContentLoaded', function() {
    let thumbnails = document.getElementsByClassName('thumbnail-product-detail')
    let activeIMG = document.getElementsByClassName('active')
    const featured = document.querySelector('#featured').src

    for (var i = 0; i < thumbnails.length; i++){
        thumbnails[i].addEventListener('mouseover', function(){
            if (activeIMG.length > 0){
                activeIMG[0].classList.remove('active')
            }
            this.classList.add('active')
            document.querySelector('#featured').src = this.src
        })
    }

    const buttonRight = document.querySelector('#slideRight');
    const buttonLeft = document.querySelector('#slideLeft');

    buttonRight.addEventListener('click', function(){
        document.getElementById('slider').scrollLeft += 180;
    })

    buttonLeft.addEventListener('click', function(){
        document.getElementById('slider').scrollLeft -= 180;
    })
})  