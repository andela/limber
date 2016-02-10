app.factory('projectInviteService', function ($resource) {
	return {
		ProjectInvite: $resource('/api/project-invites/:invite_code/', {invite_code: '@invite_code'}, {
			confirmUserExists: {
				method: 'GET',
				isArray: false
			},
			acceptInvite: {
				method: 'PUT'
			}
		}, {
			stripTrailingSlashes: false
		})
	};
});