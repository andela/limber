app.controller('DashCtrl', function($scope, $cookies, mainService){
    $scope.logout = function() {
        $cookies.remove('token');
        $scope.user = undefined;
    };
});
