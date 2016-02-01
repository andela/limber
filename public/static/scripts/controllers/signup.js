app.controller('authController', function($scope, AuthService, $cookies, $location, $window) {


    $scope.login = function() {
        AuthService.auth.login($scope.user).
        $promise.
        then(function(data) {
            $cookies.put('token', data.token);
            $window.location.href = '/dashboard';

        }).
        catch(function(data) {
            $scope.loginmsg = "Error Logging in. Please try again"
        });

    };

    $scope.logout = function() {
        $cookies.remove('token');
        $scope.user = undefined;
    };
    
    $scope.register = function(isValid) {

        $scope.signupmsg = ""
        $scope.signuperror = ""

        if (isValid) {
            var data = {
                username: $scope.signup.username,
                email: $scope.signup.email,
                password: $scope.signup.password
            };
            AuthService.users.create(data).
            $promise.
            then(function(result) {
                console.log(result);
                $scope.signupmsg = "Registration complete. You may now log in."
                $scope.signup = {}
            }).
            catch(function(response) {
                $scope.signuperror = "Error creating account. Please try again"
            });
        }else {
            $scope.signuperror = "Password fields do not match"
        }
    };
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
