var app = angular.module('limberApp', ['ngRoute', 'ngResource', 'ngCookies', 'ui.materialize']);

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

app.directive("passwordStrength", function(){
    return {
        restrict: 'A',
        link: function(scope, element, attrs){
            scope.$watch(attrs.passwordStrength, function(value) {
                if(angular.isDefined(value)){
                    if (value.length >= 8) {
                        scope.valid_password = '';
                    } else {
                        scope.valid_password = 'password too short';
                    }
                }
            });
        }
    };
});

$(document).ready(function(){
    $('ul.tabs').tabs();
    $(".button-collapse").sideNav();
});
