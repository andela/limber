var app = angular.module('limberApp', ['ngRoute', 'ngResource', 'ngCookies']);

app.config(function($httpProvider, $locationProvider, $interpolateProvider) {

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('sessionInjector');

    $interpolateProvider.startSymbol('[[').endSymbol(']]');

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
});

app.run(function($cookies, mainService) {
    cookie = $cookies.get('token')
    mainService.verify.token({'token': cookie})
    .$promise.then(function  (data) {
        // console.log(data)
    }).
    catch(function(response) {
        if (response.status == 400) {
            $cookies.remove('token')
        };
    });
});

app.directive("compareTo", function() {
    return {
        require: "ngModel",
        scope: {
            otherModelValue: "=compareTo"
        },
        link: function(scope, element, attributes, ngModel) {

            ngModel.$validators.compareTo = function(modelValue) {
                return modelValue == scope.otherModelValue;
            };

            scope.$watch("otherModelValue", function() {
                ngModel.$validate();
            });
        }
    };
});
$(document).ready(function(){
    $('ul.tabs').tabs();
    $(".button-collapse").sideNav();
});
