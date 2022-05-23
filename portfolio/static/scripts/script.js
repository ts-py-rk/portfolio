$(function() {
  jGroup = $('.group');
  jContent = $('.content');  
  jGroup.on('click', function(event) {
    jThis = $(event.currentTarget);
    jGroup.removeClass('opened');
    jContent.find('.container').removeClass('opened');
    jThis.addClass('opened');
    if (jThis.hasClass('a')) {
      jContent.find('.container.a').addClass('opened');
    }
    if (jThis.hasClass('b')) {
      jContent.find('.container.b').addClass('opened');
    }
    if (jThis.hasClass('c')) {
      jContent.find('.container.c').addClass('opened');
    }
    if (jThis.hasClass('d')) {
      jContent.find('.container.d').addClass('opened');
    }
  });
});



document.addEventListener('DOMContentLoaded', () => {
const getSort = ({ target }) => {
    const order = (target.dataset.order = -(target.dataset.order || -1));
    const index = [...target.parentNode.cells].indexOf(target);
    const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
    const comparator = (index, order) => (a, b) => order * collator.compare(
        a.children[index].innerHTML,
        b.children[index].innerHTML
    );
    for(const tBody of target.closest('table').tBodies)
        tBody.append(...[...tBody.rows].sort(comparator(index, order)));
    for(const cell of target.parentNode.cells)
        cell.classList.toggle('sorted', cell === target);
};
document.querySelectorAll('.table_sort thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));
});



var bigsize = "900";
var smallsize = "350";
function changeSizeImage(im) {
  if(im.height == bigsize) im.height = smallsize;
  else im.height = bigsize;
  }


var bigsiz = "red";
var smallsiz = "green";
function changeColor(im) {
  if(im.color == bigsiz) im.color = smallsiz;
  else im.color = bigsiz;
}