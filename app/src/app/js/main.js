// ----- INPUT AREA -----
const userInput = document.getElementById('search-input');
const userInputScollHeight = userInput.scrollHeight;
function autosize(el) {
    setTimeout(function(){
        el.style.height = '';
        if (el.scrollHeight > userInputScollHeight) {
            el.style.height = el.scrollHeight + 'px';
            document.getElementById('input-wrapper').classList.add('expand');
        }
        else {
            document.getElementById('input-wrapper').classList.remove('expand');
        }
    }, 0);
}