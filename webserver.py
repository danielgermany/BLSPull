from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

BLSlist = []

with open("BLSlists.txt","r") as data_file:
    BLSlist = data_file.read().splitlines()

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/BLSlist'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1> BLS Link List </h1>'
            output += '<h3><a href="/BLSlist/new">Add New Link</a></h3>'
            for task in BLSlist:
                output += task
                output += '</br>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Add New Link</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/BLSlist/new">'
            output += '<input name="task" type="text" placeholder="Add new link">'
            output += '<input type="submit" value="Add">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())
        for x in BLSlist:
            print(x)
    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task')
                BLSlist.append(new_task[0])
                file = open("BLSlists.txt", "a")
                file.writelines(new_task[0] + "\n")
                file.close()


            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/BLSlist')
            self.end_headers()





def main():
    PORT = 8000
    server = HTTPServer(('', PORT), requestHandler)
    print("Server running on port",PORT)
    server.serve_forever()
    for x in BLSlist:
        print(x)

if __name__ == '__main__':
    main()