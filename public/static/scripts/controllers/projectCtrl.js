app.controller('ProjectCtrl', function($scope, $cookies, mainService){
    $('.modal-trigger').leanModal();

    var loadPersonalProjects = function () {
    	$scope.personal_projects = mainService.personal.getProjects();
    };
    loadPersonalProjects();
    var loadOrgProjects = function () {
    	$scope.org_projects = mainService.org.getProjects();
    };
    loadOrgProjects();
    $scope.other_projects = mainService.other.getProjects();
    $scope.personal = {};
    $scope.organisational = {};

    $scope.createPersonalProject = function () {
    	mainService.Projects.createProject($scope.personal).$promise.then(
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

    $scope.createOrganisationalProject = function () {
    	mainService.Projects.createProject($scope.organisational).$promise.then(
    		function (response) {
    			loadOrgProjects();
    		},
    		function (error) {
    			console.log(error);
    		}
    	);
    };

    $scope.getAssociatedOrgs = function () {
    	mainService.OrgAssociations.getAll().$promise.then(
    		function (response) {
    			$scope.org_associations = response;
    		},
    		function (error) {
    			console.log(error);
    		}
    	);
    };
});
