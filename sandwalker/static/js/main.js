$(document).ready(function () {

    var setUpLightense = function () {
	Lightense('img:not(.no-lightense)', {
	    time: 300,
	    padding: 40,
	    offset: 40,
	    keyboard: true,
	    cubicBezier: '',
	    background: 'rgba(0, 0, 0, .98)',
	    zIndex: 1000000,
	});
    };

    setUpLightense();
});
