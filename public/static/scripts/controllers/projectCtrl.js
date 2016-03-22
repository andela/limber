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
                // $scope.org_projects = response;
                // console.log("One" + org_id, $scope.org_projects);
                $scope.orgProjectClassifier[org_id] = response;
                console.log($scope.orgProjectClassifier);
            },
            function (error) {
                console.log(error);
            }
        );
    };
    // loadOrgProjects();

    var loadUserOrganisations = function() {
        // load all the organisations in which current user belongs
        $scope.user_organisations = mainService.OrgAssociations.getAll();
        console.log($scope.user_organisations);

        // console.log($scope.user_organisations.length);
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
                    loadPersonalProjects()
                    var $toastContent = $('<span style="font-weight: bold;">Personal project created.</span>');
                    Materialize.toast($toastContent, 5000);
                    // clear modal fields
                    $scope.personal.project_name = '';
                    $scope.personal.project_desc = '';
                },
                function (error) {
                    var $toastContent = $('<span style="font-weight: bold;">An error occured while creating project.</span>');
                    Materialize.toast($toastContent, 5000);
                }
            );
        } else {
            var $toastContent = $('<span style="font-weight: bold;">Please fill in both fields.</span>');
            Materialize.toast($toastContent, 5000);
        }

    };

    $scope.createOrganisationalProject = function () {
        if ($scope.organisational.owner && $scope.organisational.project_name && $scope.organisational.project_desc) {
            $('#organisationalProjectModal').closeModal();
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
            var $toastContent = $('<span style="font-weight: bold;"><p>Please fill all the fields.</p></span>');
            Materialize.toast($toastContent, 10000);
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
        } else {
            var $toastContent = $('<span style="font-weight: bold;"><p>Please fill all the fields.</p></span>');
            Materialize.toast($toastContent, 10000);
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
