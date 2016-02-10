app.controller('ProjectCtrl', function($scope, $cookies, mainService){
    $('.modal-trigger').leanModal();
    $scope.personal_projects = mainService.personal.getProjects();
    $scope.org_projects = mainService.org.getProjects();
    $scope.other_projects = mainService.other.getProjects();
});
