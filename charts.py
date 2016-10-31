from highcharts import Highchart

chart = Highchart()
options = {
'chart': {
	'type':'bar'},
'title':{
	'text':'Top 10 Hashtags'},
'xAxis':{
	'categories':['1','2','3','4','5','6','7','8','9','10']},
'yAxis':{
	'title':{
		'text':'Number of times mentioned'}
	},
}

data1 #This is an array. make size 10. first means first graoh

chart.set_dict_options(options)

chart.add_data_set(data1, 'bar', 'Count')

chart.save_file('./bar-highcharts')

