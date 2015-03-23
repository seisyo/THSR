angular.module("root",[])
	.controller("index",["$scope",function($scope){
		$scope.message="THSR student's ticket price search system";
		$scope.depstation;
		$scope.arrstation;
		$scope.depdate;
		$scope.deptime;
		$scope.isBold=function(){return true;};
		$scope.isItalic=function(){return true;};
		$scope.isUnderline=function(){return true;};
	}]);