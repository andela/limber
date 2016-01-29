app.controller('authController', function ($scope, AuthService, $cookies, $location,  $window) {

    nextParam = $location.search().code;
    $scope.signup_tab = ''
    $scope.login_tab = ''
    console.log(nextParam);

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
    $scope.register = function() {
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
    };



    $scope.confirm_Org_Addition = function () {
        var data = {
            pk : nextParam,
            register: "org"
        }
        AuthService.OrgConfirmation.comfirmMember(data)
        .$promise
        .then(function  (successResponse) {
            if (successResponse.status == 200) {

            }
        })
        .catch(function  (errorResponse) {
            //If a user is not currently registered and logged in
            if (errorResponse.status == 428){
                //log current user and redirect to signup with the code
                $cookies.remove('token');
                $scope.user = {};
                $scope.signup_tab = 'active'
                $scope.signup.email = errorResponse.data.email
                $window.location.href = '/signup?code='+nextParam;

            } else if (errorResponse.status == 403){
                //log user out and redirect to login
                $cookies.remove('token');
                $scope.user = {};
                $scope.user.email = errorResponse.data.email
                // $scope.login_tab = 'active'
                $window.location.href = '/signup?code='+nextParam;
            }
        });
    };
});
