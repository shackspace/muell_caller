var express = require('express');
var cors = require('cors');
var app = express();
var nconf = require('nconf');
var body_parser = require('body-parser');

app.use(cors());
app.use(body_parser.json());

var config = require('./static_muelldata.json');

nconf.file({file: require('path').resolve(__dirname, 'storage.json') });
var muell_log = nconf.get('muell_log');
var muell_status = nconf.get('muell_status');

app.post('/muellshack/:muellarg/', function(req, res, next) {
	var muellarg  = req.params.muellarg;
	var next_muelldate = getNextMuelldate(muellarg)[muellarg];
	var muelldata = config[muellarg];

	if (!(muellarg in config))
		return next();
	if (muelldata.indexOf(next_muelldate) === -1)
		return next();

	if (!muell_status[muellarg])
		muell_status[muellarg] = {};
	if (!muell_status[muellarg][next_muelldate])
		muell_status[muellarg][next_muelldate] = {};

	muell_status[muellarg][next_muelldate].main_action_done = req.body.main_action_done;

	const limit   = 5;
	var dat_limit = new Date(next_muelldate);
	dat_limit = new Date(dat_limit.setDate(dat_limit.getDate() - limit));

	res.type('application/json'); // set content-type
	if (new Date() < dat_limit) {
		log_msg(muellarg, next_muelldate, '403 - Forbidden', req.body);
		res.status(403).send('Forbidden');
	} else {
		log_msg(muellarg, next_muelldate, 'put event', req.body);
		res.json({'message':'Thanks for using muellshack'});
	}

});

app.get('/muellshack/:muellarg', function(req, res, next) {
	var muellarg = req.params.muellarg;
	var output = getNextMuelldate(muellarg);

	if (!output[muellarg])
		return next();

	output['main_action_done'] = false;

	var value = get_muell_status(muellarg, output[muellarg]);
	if (value.hasOwnProperty("main_action_done"))
		output['main_action_done'] = value.main_action_done;

	res.type('application/json'); // set content-type
	res.json(output);
});

app.listen(process.env.PORT || 8081);

function getNextMuelldate(muell_type) {
	var muelldata = config[muell_type];

	var retval = {};
	retval[muell_type] = false;

	if (!(muell_type in config))
		return retval;

	for (i = 0; i < muelldata.length; i++) {
		date_i = new Date(muelldata[i])
		if (date_i > new Date())
		{
			retval[muell_type] = muelldata[i]
			break;
		}
	}

	return retval;
}

function get_muell_status(muell_type,muell_date) {
	if (muell_status.hasOwnProperty(muell_type) && muell_status[muell_type].hasOwnProperty(muell_date)) {
		return muell_status[muell_type][muell_date];
	}
	return {"date":muell_date};
}

function log_msg(muellarg, next_muelldate, event_msg, message) {
	muell_log.push({
		'event_date': new Date(),
		'muell_type':muellarg,
		'muell_date':next_muelldate,
		'event_msg': event_msg,
		'message': message
	});
	nconf.save();
}

function exitHandler(options, err) {
	nconf.save();
    if (options.exit) process.exit();
}
//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {exit:true}));
//catches sigterm event
process.on('SIGTERM', exitHandler.bind(null, {exit:true}));
//catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, {exit:true}));

