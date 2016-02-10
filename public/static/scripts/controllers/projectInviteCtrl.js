app.controller('ProjectInviteCtrl', function($scope, $window, projectInviteService){

	$scope.completeProjectInvite = function(invite_code) {
		var data = {
			invite_code: invite_code
		};
		projectInviteService.ProjectInvite.confirmUserExists(data).$promise.then(
			function (response) {
				// invited user probably exists in the system
				if (response.status === 'User found') {
					$window.location.href = '/login?completeinvite=yes&invitecode=' + data.invite_code;
				} else {
					console.log(response);
				}
			},
			function (error) {
				// Probably a 404 - Invited user currently not in system
				if (error.data.status === 'User not found') {
					$window.location.href = '/signup?completeinvite=yes&invitecode=' + data.invite_code;
				} else {
					console.log(error);
				}

			}
		)
    };
});