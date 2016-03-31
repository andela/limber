app.controller('passwordResetCtrl', function($scope, mainService){
  $scope.changePassword = function () {
    // Ensure the user has entered something in both fields
    if ($scope.first_pass && $scope.second_pass) {
      // Ensure the 'password' and the 'confirmation password' are the same
      if ($scope.first_pass === $scope.second_pass) {
        var data = {
          reset_id: $scope.reset_code,
          new_password: $scope.first_pass
        };
        mainService.PasswordReset.resetPassword(data).$promise.then(
          function (response) {
            Materialize.toast('Password reset complete! Proceed to login.', 5000);
          },
          function (error) {
            Materialize.toast('An error occured while trying to reset the password', 5000);
          }
        );
      } else {
        Materialize.toast('Passwords entered do not match!', 5000);
      }
    } else {
      Materialize.toast('Passwords (and confirmation password) required!', 5000);
    }

  };
});
