app.controller('LandingController', function($scope){
    $(".animation").typed({
        strings: ["agile software development", "faster project delivery",  "effective project planning", "better project management."],
        typeSpeed: 70,
        backDelay: 70,
        loop: true,
        cursorChar: " | "
     });
     $('.slider').slider({height: 120, indicators: false, interval : 2000});
});
