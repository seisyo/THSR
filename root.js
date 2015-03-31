angular.module("root",[])
.controller("index", ["$scope", "$http", function($scope, $http){

    $scope.depclick = function(){
        if($scope.depstation != "undefined" && $scope.arrstation != "undefined" && $scope.depdate != "undefined" && $scope.deptime != "undefined"){
            console.log($scope.depstation);
            console.log($scope.arrstation);
            console.log($scope.depdate);
            console.log($scope.deptime);
                
            $http.jsonp("http://127.0.0.1:5000/searchtrain?callback=JSON_CALLBACK"+"&depsta="+$scope.depstation+"&arrsta="+$scope.arrstation+"&date="+$scope.depdate+"&time="+$scope.deptime).success(function(data){
                console.log(data);
             }).error(function(){
                console.log("error!!")
             });

            // ,{
            //     depsta: $scope.depstation, 
            //     arrsta: $scope.arrstation, 
            //     date: $scope.depdate, 
            //     time: $scope.deptime
            //  }

        };
    };
}]);