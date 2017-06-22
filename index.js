var http = require("http");

var port = 3000;

http.createServer(function(reqst, resp) {
    resp.writeHead(200, {'Content-Type': 'text/plain'});
    resp.end('PICTL');
}).listen(port);

console.log('lolilol');
