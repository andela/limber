app.controller('ProjectCtrl', function($scope, $cookies, AuthService){
    $('.modal-trigger').leanModal();
    $scope.projects = AuthService.projects.getProjects();
});
