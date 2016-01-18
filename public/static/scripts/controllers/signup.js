angular.module('limberApp', ['ngResource', 'ngCookies']).
    // config(['$httpProvider', function($httpProvider){
    //     // django and angular both support csrf tokens. This tells
    //     // angular which cookie to add to what header.
    //     $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    //     $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    //     // console.log($scope)
    // }]).
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
    controller('authController', function($scope, api, $cookies, $location, $window) {

        $scope.login = function(){
            // dt = {email: $scope.username, password: $scope.password};
            api.auth.login($scope.user).
                $promise.
                    then(function(data){
                        $cookies.put('token', data.token);
                        // $window.location.href = '/api/user'
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
            // dt = {email: $scope.email, username: $scope.username, password: $scope.password};
            api.users.create($scope.signup).
                $promise.
                    then(function(data){
                        console.log(data);
                        // $window.location.href = '/api'
                    }).
                    catch(function(data){
                        console.log(data);
                    });
            };
    });
