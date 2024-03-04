from flask import Flask, render_template, request, redirect
import subprocess
import zipfile
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Function to check if ffmpeg is installed
def is_ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        # Check if ffmpeg is installed
        if not is_ffmpeg_installed():
            return 'Error: ffmpeg is not installed or not accessible'

        singer_name = request.form['singer_name']
        num_videos = int(request.form['num_videos'])
        duration_to_cut = int(request.form['duration_to_cut'])
        email = request.form['email']

        zip_file = ''  # Default value for zip_file

        try:
            # Call your command line program with provided parameters using Popen
            process = subprocess.Popen(['python', '102117161.py', singer_name, str(num_videos), str(duration_to_cut), 'output.mp3'])
            return_code = process.wait()  # Wait for the process to finish

            # Check if the command line program executed successfully and output file was generated
            if return_code != 0 or not os.path.exists('output.mp3'):
                raise Exception('Failed to generate output file')

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

        except Exception as e:
            print(f'Error during processing: {str(e)}')  # Log the error
            return f'Error: {str(e)}'

        finally:
            if os.path.exists(zip_file):
                os.remove(zip_file)  # Delete the zip file after sending
            if os.path.exists('output.mp3'):
                os.remove('output.mp3')  # Delete the output file after sending

        return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
