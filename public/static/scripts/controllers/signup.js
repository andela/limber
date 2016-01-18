angular.module('limberApp').
    factory('api', function($resource){
        return {
            auth: $resource('/api/api-token-auth/', {}, {
                login: {method: 'POST'},
                logout: {method: 'DELETE'}
            },{
                stripTrailingSlashes: false
            }),
            users: $resource('/api/user/', {}, {
                create: {method: 'POST'}
            },{
                stripTrailingSlashes: false
            })
        };
    }).
    controller('authController', function($scope, api, $cookies, $location, $window) {

        $scope.confirmmessage = ""

        $scope.login = function(){
            api.auth.login($scope.user).
                $promise.
                    then(function(data){
                        $cookies.put('token', data.token);
                        $window.location.href = '/api/user'

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
            api.users.create($scope.signup).
                $promise.
                    then(function(result){
                        console.log(result);
                        $scope.confirmmessage = "Registration complete. Please confirm your email address before logging in."
                        $scope.signup = {}
                        $window.location.href = '/api'
                    }).
                    catch(function(response){
                        console.log(response);
                    });
            };
    });
