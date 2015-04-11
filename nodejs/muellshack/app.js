var express = require('express');
var cors = require('cors');
var app = express();

app.use(cors());

var config = require('./gelber_sack.json');

app.get('/muellshack/gelber_sack', function(req, res) {

	for (i = 0; i < config.gelber_sack.length; i++) {
		date_i = new Date(config.gelber_sack[i])
		if (date_i > new Date())
		{
			break;
		}
	}


	var output = {}
	output['gelber_sack'] = config.gelber_sack[i]

	res.type('application/json'); // set content-type
	res.json(output);
});

app.listen(process.env.PORT || 8081);

