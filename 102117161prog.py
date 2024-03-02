from flask import Flask, render_template, request, redirect
import subprocess
import zipfile
import os
import smtplib
from email.message import EmailMessage
import socket

app = Flask(__name__)

def check_open_ports():
    # Define the host and ports to check
    host = 'localhost'
    ports = [80, 443]  # HTTP and HTTPS ports
    
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    
    return open_ports

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        singer_name = request.form['singer_name']
        num_videos = int(request.form['num_videos'])
        duration_to_cut = int(request.form['duration_to_cut'])
        email = request.form['email']

        # Check for open HTTP ports
        open_ports = check_open_ports()
        if 80 not in open_ports:
            return 'Error: HTTP port (80) is not open'
        
        # Call your command line program with provided parameters using Popen
        process = subprocess.Popen(['python', '102117161.py', singer_name, str(num_videos), str(duration_to_cut), 'output.mp3'])
        process.wait()  # Wait for the process to finish

        # Check if output file exists
        if not os.path.exists('output.mp3'):
            return 'Error: Output file not generated'

        # Compress output file into a zip
        zip_file = f'{singer_name}_videos.zip'
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.write('output.mp3')

        # Send zip file to the provided email
        msg = EmailMessage()
        msg['Subject'] = 'Cut Videos Output'
        msg['From'] = 'chelsichopra04@gmail.com'  
        msg['To'] = email
        msg.set_content('Please find the attached zip file.')

        with open(zip_file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype='application', subtype='zip', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('chelsichopra04@gmail.com', 'qqcc gsiy gsqg tmie')  
            smtp.send_message(msg)

        os.remove(zip_file)  # Delete the zip file after sending
        os.remove('output.mp3')  # Delete the output file after sending
        return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
