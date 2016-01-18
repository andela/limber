angular.module('limberApp', ['ngResource', 'ngCookies'])
.factory('sessionInjector', function($cookies) {
    console.log($cookies.get("token"));
    var sessionInjector = {
        request: function(config) {
            var token = $cookies.get("token");
            console.log(token);
            config.headers['Authorization'] = "JWT " + token;
            return config;
        }
    };
    return sessionInjector;
})
.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('sessionInjector');
    // $httpProvider.defaults.headers.common['Authorization'] = 'divnDvjkSFJCBisdzfladsiocguhsfjcnfkcsahd';

})
