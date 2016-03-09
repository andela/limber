app.controller('ProjectCtrl', function($scope, $cookies, mainService){
    $('.modal-trigger').leanModal();

    var loadPersonalProjects = function () {
    	$scope.personal_projects = mainService.personal.getProjects();
    }
    loadPersonalProjects();
    $scope.org_projects = mainService.org.getProjects();
    $scope.other_projects = mainService.other.getProjects();
    $scope.personal = {};

    $scope.createPersonalProject = function () {

    	console.log($scope.personal);
    	mainService.Projects.createPersonalProject($scope.personal).$promise.then(
    		function (response) {
    			loadPersonalProjects()
    			$scope.personal.project_name = '';
    			$scope.personal.project_desc = '';
    		},
    		function (error) {
    			console.log(error);
    		}
    	);
    };
});
