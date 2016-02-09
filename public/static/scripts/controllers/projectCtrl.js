app.controller('ProjectCtrl', function($scope, $cookies, mainService){
    $('.modal-trigger').leanModal();
    $scope.projects = mainService.projects.getProjects();
});
