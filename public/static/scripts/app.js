var app = angular.module('limberApp', ['ngResource', 'ngCookies']);

app.config(function ($httpProvider, $locationProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('sessionInjector');

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
});