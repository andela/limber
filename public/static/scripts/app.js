var app = angular.module('limberApp', ['ngResource', 'ngCookies']);

app.config(function ($httpProvider, $locationProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('sessionInjector');

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
});

app.run(function($cookies, AuthService) {
    cookie = $cookies.get('token')
    AuthService.verify.token({'token': cookie})
    .$promise.then(function  (data) {
        // console.log(data)
    }).
    catch(function(response) {
        if (response.status == 400) {
           $cookies.remove('token')
        };
    });
});