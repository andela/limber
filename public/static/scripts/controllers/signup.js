app.controller('authController', function($scope, AuthService, $cookies, $location, $window) {

    $scope.confirmmessage = ""

    $scope.login = function() {
        AuthService.auth.login($scope.user).
        $promise.
        then(function(data) {
            $cookies.put('token', data.token);
            $window.location.href = '/dashboard';

        }).
        catch(function(data) {
            console.log(data);
            console.log('error');
        });

    };

    $scope.logout = function() {
        AuthService.auth.logout(function() {
            $scope.user = undefined;
        });
    };
    $scope.register = function() {
        var data = {
            username:$scope.signup.username,
            email:$scope.signup.email,
            password:$scope.signup.password
        };
        AuthService.users.create(data).
        $promise.
        then(function(result) {
            console.log(result);
            $scope.confirmmessage = "Registration complete. Please confirm your email address before logging in."
            $scope.signup = {}
            $window.location.href = '/signup';
        }).
        catch(function(response) {
            console.log(response);
        });
    };
});
