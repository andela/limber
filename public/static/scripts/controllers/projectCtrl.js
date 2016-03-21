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
    $scope.delete = {};
    $scope.confirm = {};

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

        if ($scope.organisational.owner) {
            mainService.Projects.createProject($scope.organisational).$promise.then(
                function (response) {
                    var $toastContent = $('<span style="font-weight: bold;">Organisation project created.</span>');
                    Materialize.toast($toastContent, 5000);
                    // Refresh view
                    loadOrgProjects();
                    //  Clear data in modal
                    $scope.organisational = {};
                },
                function (error) {
                    var $toastContent = $('<span style="font-weight: bold;">Error! Organisation project not created.</span>');
                    Materialize.toast($toastContent, 5000);
                }
            );
        } else {
            var $toastContent = $('<span style="font-weight: bold;">' +
                '<p>You are creating an organisational project.</p>' +
                '<p>Please specify the Organisation that owns this project</p></span>');
            Materialize.toast($toastContent, 10000);
        }

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

    $scope.openEditProjectModal = function (project_id, project_owner_id, owner_type) {
        $('#editProjectModal').openModal();
        $scope.edit_project_id = project_id;
        $scope.edit_project_owner_id = project_owner_id;
        $scope.edit_owner_type = owner_type;
    };

    $scope.editProject = function(project_id) {
        var data = {
            project_id: $scope.edit_project_id,
            owner: $scope.edit_project_owner_id,
            project_name: $scope.edit.project_name,
            project_desc: $scope.edit.project_desc
        };
        mainService.Projects.editProject(data).$promise.then(
            function (response) {
                var $toastContent = $('<span style="font-weight: bold;">Project details updated.</span>');
                Materialize.toast($toastContent, 5000);
                // reload page
                if ($scope.edit_owner_type === 'personal') {
                    loadPersonalProjects();
                } else if ($scope.edit_owner_type === 'organisational') {
                    loadOrgProjects();
                }
                // Reset modal values
                $scope.edit.project_name = '';
                $scope.edit.project_desc = '';
            },
            function (error) {
                var $toastContent = $('<span style="font-weight: bold;">Error! Project not updated.</span>');
                Materialize.toast($toastContent, 5000);
            }
        );
    };

    $scope.openDeleteModal = function (project_id, owner_type) {
        $('#confirmDeleteProjectModal').openModal();
        $scope.delete_project_id = project_id;
        $scope.delete_owner_type = owner_type;
    };

    $scope.deleteProject = function () {
        if ($scope.confirm.delete === 'DELETE') {
            var data = {
                project_id: $scope.delete_project_id
            };
            mainService.Projects.deleteProject(data).$promise.then(
                function (response) {
                    var $toastContent = $('<span style="font-weight: bold;">Project deleted.</span>');
                    Materialize.toast($toastContent, 5000);
                    if ($scope.delete_owner_type === 'personal') {
                        loadPersonalProjects();
                    } else if ($scope.delete_owner_type === 'organisational') {
                        loadOrgProjects();
                    }
                    // clear modal field on success
                    $scope.confirm.delete = '';
                },
                function (error) {
                    var $toastContent = $('<span style="font-weight: bold;">Error! Project not deleted.</span>');
                    Materialize.toast($toastContent, 5000);
                }
            );

        } else {
            var $toastContent = $('<span style="font-weight: bold;">Please confirm this operation by typing DELETE.</span>');
            Materialize.toast($toastContent, 5000);
        }

    };
});
