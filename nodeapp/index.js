var express = require('express');
var bodyParser = require("body-parser")
var path = require('path');
const crypto = require('crypto');

// Replace with your secret key (must be a string or buffer)
const secretKey = 'your_secret_key_here';



// Choose a digest algorithm (e.g. 'sha256')
const algorithm = 'sha256';


var app = express();
app.use(
    bodyParser.urlencoded({
        extended: true
    })
);
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname + '/public')));


app.get('/', function (req, res) {
	res.sendfile(path.join(__dirname + "/public/index.html"));
});

app.post('/display', function(req, res) {

	var num = req.body.userId;
	// Update hmac with the message (implicitly encoded to bytes)
	console.log("body="+JSON.stringify(req.body));
	const hmac = crypto.createHmac(algorithm, secretKey);
	hmac.update(JSON.stringify(req.body));

	// Get the HMAC digest in hexadecimal format
	const hmacDigest = hmac.digest('hex');
	console.log("calculated="+hmacDigest);
	console.log("header="+req.header('X-Auth'));

	if(hmacDigest == req.header('X-Auth'))
	{
		res.send("Successful");
	}
	else
	{
		res.send("Failed");
	}

	//res.send("The user ID is " + num);
})

app.listen(8088, function () {
	console.log('Simple Web Application running on port 8088!');
});