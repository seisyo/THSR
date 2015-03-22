angular.module("root",[])
	.controller("index",["$scope",function($scope){
		$scope.message="THSR student's ticket price search system";
		$scope.depstation;
		$scope.arrstation;
		$scope.deptime;
	}]);