var express = require('express');
var cors = require('cors');
var app = express();

app.use(cors());

var config = require('./static_muelldata.json');

app.get('/muellshack/:muellarg', function(req, res, next) {
	var muellarg = req.params.muellarg;
	var muelldata = config[muellarg];

	if (!(muellarg in config))
		return next();

	for (i = 0; i < muelldata.length; i++) {
		date_i = new Date(muelldata[i])
		if (date_i > new Date())
		{
			break;
		}
	}

	var output = {}
	output[muellarg] = muelldata[i]

	res.type('application/json'); // set content-type
	res.json(output);
});

app.listen(process.env.PORT || 8081);

