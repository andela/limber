angular.module('limberApp').controller('SignupController', function($scope, $http, $location, $window) {

    $scope.user = {};

    $scope.submitForm = function() {
        $http({
            method  : 'POST',
            url     : '/api/user/',
            data    : $scope.user,
            headers : {'Content-Type': 'application/json'}
        })
        .then(function successCallback(response) {
            $window.location.href = '/api/api-auth/login/';
        }, function errorCallback(response) {
            $window.location.href = '/signup'
        });
    };


});
