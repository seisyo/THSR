angular.module("root",[])
.controller("index", ["$scope", "$http", function($scope, $http){

    $scope.depclick = function(){
        if($scope.depstation != "undefined" && $scope.arrstation != "undefined" && $scope.depdate != "undefined" && $scope.deptime != "undefined"){
            console.log($scope.depstation);
            console.log($scope.arrstation);
            console.log($scope.depdate);
            console.log($scope.deptime);
                // console.log($http);
                // $http.get('http://127.0.0.1:5000/searchtrain', {
                //     depsta: $scope.depstation, 
                //     arrsta: $scope.arrstation, 
                //     date: $scope.depdate, 
                //     time: $scope.deptime
                // }).success(function(data){
                //     console.log(data);
                // });
            var responsePromise = $http.jsonp( "http://127.0.0.1:5000/searchtrain?callback=JSON_CALLBACK", {
                depsta: $scope.depstation | String, 
                arrsta: $scope.arrstation | String, 
                date: $scope.depdate | String, 
                time: $scope.deptime | String
             });

            responsePromise.success(function(data) {
                console.log(data);
    // do something with the returned JavaScript object
    // ( in the "data" parameter ).
            });

}
};
}]);