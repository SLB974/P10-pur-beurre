window.addEventListener('DOMContentLoaded', event => {


const NutriA = '#0e8c4f';
const NutriB ='#7ec247';
const NutriC ='#fbcb29';
const NutriD ='#fb7f1d';
const NutriE ='#f13c1d';
const badges = document.body.querySelectorAll('#pscore');

var Nutriscore = function (element) {
    var color = ''
    switch (element.textContent) {
        case 'A':
            color = NutriA;
            enability = false;
            break;
        case 'B':
            color= NutriB;
            break;
        case 'C':
            color= NutriC;
            break;
        case 'D':
            color= NutriD;
            break;
        case 'E':
            color= NutriE;
    }
    element.style.backgroundColor = color;
    element.parentNode.style.backgroundColor = color;
    element.parentNode.parentNode.style.backgroundColor = color;
    console.log('coucou')
};

badges.forEach(Nutriscore);

const banner = document.querySelector('.product_banner');

if(banner) {
    banner.style.backgroundImage = 'url(' + banner.id + ')';
};

});
