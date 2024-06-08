import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Change the working directory to the Attendance directory
web_dir = os.path.join(os.path.dirname(__file__), 'AttendanceSystem/attendance')
os.chdir(web_dir)

# Start the HTTP server
server_address = ('', 8000)  # Serve on all available IP addresses, port 8000
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print("Serving HTTP on port 8000...")
httpd.serve_forever()
