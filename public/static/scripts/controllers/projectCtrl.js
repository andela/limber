app.controller('ProjectCtrl', function($scope, $cookies, mainService){
    $('.modal-trigger').leanModal();


    $scope.orgProjectClassifier = {};

    var loadPersonalProjects = function () {
    	$scope.personal_projects = mainService.personal.getProjects();
    };
    loadPersonalProjects();

    $scope.loadOrgProjects = function (org_id) {
        // Provide the owner_id query parameter. This returns projects that belong
        // to organisations of this org_id
        var data = {
            owner_id: org_id
        }
        mainService.org.getProjects(data).$promise.then(
            function (response) {
                $scope.orgProjectClassifier[org_id] = response;
            },
            function (error) {
                console.log(error);
            }
        );
    };

    var loadUserOrganisations = function() {
        // load all the organisations in which current user belongs
        $scope.user_organisations = mainService.OrgAssociations.getAll();
    }
    loadUserOrganisations();

    $scope.other_projects = mainService.other.getProjects();
    $scope.personal = {};
    $scope.organisational = {};
    $scope.edit = {};
    $scope.delete = {};
    $scope.confirm = {};

    $scope.createPersonalProject = function () {
        if ($scope.personal.project_name && $scope.personal.project_desc) {
            $('#personalProjectModal').closeModal();
            mainService.Projects.createProject($scope.personal).$promise.then(
                function (response) {
                    // refresh projects
                    loadPersonalProjects();
                    Materialize.toast('Personal project created.', 5000);
                    // clear modal fields
                    $scope.personal.project_name = '';
                    $scope.personal.project_desc = '';
                },
                function (error) {
                    Materialize.toast('An error occured while creating project.', 5000);
                }
            );
        } else {
            Materialize.toast('Please fill in both fields.', 5000);
        }

    };

    $scope.createOrganisationalProject = function () {
        if ($scope.organisational.owner && $scope.organisational.project_name && $scope.organisational.project_desc) {
            $('#organisationalProjectModal').closeModal();
            mainService.Projects.createProject($scope.organisational).$promise.then(
                function (response) {
                    Materialize.toast('Organisation project created.', 5000);
                    // Refresh view
                    loadUserOrganisations();
                    //  Clear data in modal
                    $scope.organisational = {};
                },
                function (error) {
                    Materialize.toast('Error! Organisation project not created.', 5000);
                }
            );
        } else {
            Materialize.toast('Please fill all the fields.', 10000);
        }

    };

    $scope.getAdminAssociatedOrgs = function () {
    	mainService.OrgAdminAssociations.getAll().$promise.then(
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
        if ($scope.edit.project_desc && $scope.edit.project_name) {
            $('#editProjectModal').closeModal();
            var data = {
                project_id: $scope.edit_project_id,
                owner: $scope.edit_project_owner_id,
                project_name: $scope.edit.project_name,
                project_desc: $scope.edit.project_desc
            };
            mainService.Projects.editProject(data).$promise.then(
                function (response) {
                    Materialize.toast('Project details updated.', 5000);
                    // reload page
                    if ($scope.edit_owner_type === 'personal') {
                        loadPersonalProjects();
                    } else if ($scope.edit_owner_type === 'organisational') {
                        loadUserOrganisations();
                    }
                    // Reset modal values
                    $scope.edit.project_name = '';
                    $scope.edit.project_desc = '';
                },
                function (error) {
                    Materialize.toast('Error! Project not updated.', 5000);
                }
            );
        } else {
            Materialize.toast('Please fill all the fields.', 10000);
        }

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
                    Materialize.toast('Project deleted.', 5000);
                    if ($scope.delete_owner_type === 'personal') {
                        loadPersonalProjects();
                    } else if ($scope.delete_owner_type === 'organisational') {
                        loadUserOrganisations();
                    }
                    // clear modal field on success
                    $scope.confirm.delete = '';
                },
                function (error) {
                    Materialize.toast('Error! Project not deleted.', 5000);
                }
            );

        } else {
            Materialize.toast('Please confirm this operation by typing DELETE.', 5000);
        }

    };
});
