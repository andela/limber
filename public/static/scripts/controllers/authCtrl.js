
app.controller('authController', function($rootScope, $scope, mainService, $cookies, $location, $window) {

    nextParam = $location.search().code;


    $scope.$on('AutoLogin', function(event, args) {
        console.log(args);
        AuthService.auth.login(args.data).
        $promise.
        then(function(response) {
            console.log(response)
            $cookies.put('token', response.token);
            window.location.href = '/comfirm/?code=' + args.code;
        });
    });

    $scope.login = function() {
        mainService.auth.login($scope.user).
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
            mainService.users.create(data).
            $promise.
            then(function(result) {
                //when we get a code param in the url
                if (typeof nextParam === 'undefined') {
                    //if a code param doesn't exist in the url
                    //then follow the normal registration process
                    $scope.signupmsg = "Registration complete. You may now log in."
                    $scope.signup = {}
                } else {
                    //otherwise login a user and redirect the user to
                    //the org invite page
                    var login_data = {
                        email: $scope.signup.username,
                        password: $scope.signup.password
                    };
                    $rootScope.$broadcast('AutoLogin', {
                        data: login_data,
                        code: nextParam
                    });
                }

            }).
            catch(function(response) {
                $scope.signuperror = "Error creating account. Please try again"
            });

        };
    };



    $scope.confirm_Org_Addition = function() {
        var data = {
            pk: nextParam,
            register: "org"
        }


        AuthService.OrgConfirmation.comfirmMember(data)
            .$promise
            .then(function(successResponse) {
                //if a user has accepted, redirect to organisation view
                $window.location.href = '/dashboard/';
            })
            .catch(function(errorResponse) {

                //If a user is not currently registered and logged in
                if (errorResponse.status == 428) {
                    //log current user and redirect to signup with the code
                    $cookies.remove('token');

                    $scope.signup = {};
                    $scope.signup.email = errorResponse.data.email;

                    $window.location.href = '/signup?code=' + nextParam;

                } else if (errorResponse.status == 403) {
                    //log user out and redirect to login
                    $cookies.remove('token');
                    $scope.user = {};
                    $scope.user.email = errorResponse.data.email
                        // $scope.login_tab = 'active'
                    $window.location.href = '/signup?code=' + nextParam;
                }
            });
    };
});
