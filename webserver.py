from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

BLSlist = []
BLSlist_name = []
BLSlist_dash = []

with open("BLSlists.txt","r") as data_file:
    BLSlist = data_file.read().splitlines()

with open("BLSlists_name.txt","r") as data_file:
    BLSlist_name = data_file.read().splitlines()

with open("BLSlists_dash.txt","r") as data_file:
    BLSlist_dash = data_file.read().splitlines()

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
            output += '<h3> Current Healthcare Query DashBoards </h3>'
            for i in range(len(BLSlist)):
                output += '<a href='+BLSlist_dash[i]+' target="_blank">'+BLSlist_name[i]+'</a>'
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


            output += '<form method="POST" enctype="multipart/form-data" action="/BLSlist/new">'
            output += '<input name="task_name" type="text" placeholder="Add new link name">'
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
                new_task_name = fields.get('task_name')

                BLSlist_name.append(new_task_name[0])
                BLSlist.append(new_task[0])

                file = open("BLSlists.txt", "a")
                file.writelines(new_task[0] + "\n")
                file.close()

                file = open("BLSlists_name.txt", "a")
                file.writelines(new_task_name[0] + "\n")
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
