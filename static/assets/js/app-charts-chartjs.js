var App = (function () {
	'use strict';

	App.ChartJs = function( ){

    var randomScalingFactor = function() {
      return Math.round(Math.random() * 100);
    };

    	var endpoint = '/api/condition/'
    	var dataCon = []
    	var labelsCon = []
    	$.ajax({
    		method : "GET",
    		url : endpoint,
    		success : function(data){
    			labelsCon = data.labels
    			dataCon = data.default
    			pieChart()
    		},
    		error: function(error_data){
    			console.log("error")
    			console.log("error_data")
    		}

    	})

    	var endpointSts = '/api/statistik/'
    	var dataSts = []
    	var labelsSts = []
    	$.ajax({
    		method : "GET",
    		url : endpointSts,
    		success : function(data){
    			labelsSts = data.labels
    			dataSts = data.default
    			barChart()
    		},
    		error: function(error_data){
    			console.log("error")
    			console.log("error_data")
    		}

    	})

		function pieChart(){
		//Set the chart colors
			var color1 = App.color.primary;
			var color2 = App.color.danger;
			var color3 = App.color.warning;

      //Get the canvas element
			var ctx = document.getElementById("pie-chart");
			
			var data = {
			  labels: labelsCon ,
			  datasets: [
			    {
			      data: dataCon,
			      backgroundColor: [
			        color1,
			        color2
			      ],
			      hoverBackgroundColor: [
			        color1,
			        color2
			      ]
			  	}]
			};

		    var pie = new Chart(ctx, {
	        type: 'pie',
	        data: data
	      });
		}


		function barChart(){
			var color1 = App.color.success;
			var color2 = App.color.warning;
			var color3 = App.color.danger;
			var ctx = document.getElementById("bar-chart").getContext('2d');
			var myChart = new Chart(ctx, {
			    type: 'bar',
			    data: {
			        labels: labelsSts,
			        datasets: [{
			            label: 'Jumlah Berita',
			            data: dataSts,
			            backgroundColor: [
			                color1,
			        		color2,
			        		color3
			             
			            ],
			            borderColor: [
			                'rgba(255,99,132,1)',
			                'rgba(54, 162, 235, 1)',
			                'rgba(255, 206, 86, 1)',
			            ],
			            borderWidth: 1
			        }]
			    },
			    options: {
			        scales: {
			            yAxes: [{
			                ticks: {
			                    beginAtZero:true
			                }
			            }]
			        }
			    }
			});
		}

		barChart();
		pieChart();
	};

	return App;
})(App || {});