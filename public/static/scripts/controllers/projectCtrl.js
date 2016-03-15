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
    $scope.edit = {};

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

    $scope.openEditOrgModal = function (project_id, project_owner_id) {
        $('#editOrgProjectModal').openModal();
        $scope.edit_org_project_id = project_id;
        $scope.edit_org_project_owner_id = project_owner_id;
    }

    $scope.editOrganisationalProject = function(project_id) {
        var data = {
            project_id: $scope.edit_org_project_id,
            owner: $scope.edit_org_project_owner_id,
            project_name: $scope.edit.org_project_name,
            project_desc: $scope.edit.org_project_desc
        };
        mainService.Projects.editProject(data).$promise.then(
            function (response) {
                var $toastContent = $('<span style="font-weight: bold;">Project details updated.</span>');
                Materialize.toast($toastContent, 5000);
                // reload page
                loadOrgProjects();
                // Reset modal values
                $scope.edit.org_project_name = '';
                $scope.edit.org_project_desc = '';
            },
            function (error) {
                var $toastContent = $('<span style="font-weight: bold;">Error! Project not updated.</span>');
                Materialize.toast($toastContent, 5000);
            }
        );
    }
});
