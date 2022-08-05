var $navbarLeft  = $('#collapseExample0');
var $navbarRight = $('#collapseExample1');
var $navbarMiddle = $('#collapseExample2');

$navbarLeft.on('show.bs.collapse', function () {
  $navbarRight.collapse('hide');
  $navbarMiddle.collapse('hide');
})
$navbarRight.on('show.bs.collapse', function () {
  $navbarLeft.collapse('hide');
  $navbarMiddle.collapse('hide');
})


function log() {
  console.log('вот я тут');
}