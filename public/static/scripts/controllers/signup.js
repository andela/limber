// angular.module('limberApp').controller('SignupController', function($scope, $http, $location, $window) {

//     $scope.user = {};

//     $scope.submitForm = function() {
//         $http({
//             method  : 'POST',
//             url     : '/api/user/',
//             data    : $scope.user,
//             headers : {'Content-Type': 'application/json'}
//         })
//         .then(function successCallback(response) {
//             $window.location.href = '/api/api-auth/login/';
//         }, function errorCallback(response) {
//             // $window.location.href = '/signup'
//             console.log($scope.user)
//         });
//         // console.log($scope.user)
//     };


// });
angular.module('limberApp', ['ngResource', 'ngCookies']).
    config(['$httpProvider', function($httpProvider){
        // django and angular both support csrf tokens. This tells
        // angular which cookie to add to what header.
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        // console.log($scope)
    }]).
    factory('api', function($resource){
        // function add_auth_header(data, headersGetter){
        //     var headers = headersGetter();
        //     console.log(data);
        //     headers['Authorization'] = ('JWT ' + $scope.token);
        // }
        // defining the endpoints. Note we escape url trailing dashes: Angular
        // strips unescaped trailing slashes. Problem as Django redirects urls
        // not ending in slashes to url that ends in slash for SEO reasons, unless
        // we tell Django not to [3]. This is a problem as the POST data cannot
        // be sent with the redirect. So we want Angular to not strip the slashes!
        return {
            auth: $resource('/api/api-token-auth\\/', {}, {
                login: {method: 'POST'},
                logout: {method: 'DELETE'}
            }),
            users: $resource('/api/user\\/', {}, {
                create: {method: 'POST'}
            })
        };
    }).
    controller('authController', function($scope, api, $cookies) {

        $scope.login = function(){
            dt = {email: $scope.username, password: $scope.password};
            api.auth.login(dt).
                $promise.
                    then(function(data){
                        $cookies.put('token', data.token);
                    }).
                    catch(function(data){
                        console.log(data);
                        console.log('error');
                    });

        };

        $scope.logout = function(){
            api.auth.logout(function(){
                $scope.user = undefined;
            });
        };
        $scope.register = function(){
            dt = {email: $scope.email, username: $scope.username, password: $scope.password};
            api.users.create(dt).
                $promise.
                    then($scope.login).
                    catch(function(data){
                        alert(data.data.username);
                    });
            };
    });
