from flask import Flask, render_template, request
from email.message import EmailMessage
import pandas as pd
import smtplib

app = Flask(__name__)

def send_email(to_email, subject, message, image_path=None, video_path=None):
    from_email = "unitedealstest01@gmail.com"  # Replace with your email
    password = "atjjtwbpalnvvgag"  # Replace with your email password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(message)

    if image_path:
        with open(image_path, 'rb') as file:
            image_data = file.read()

        msg.add_attachment(image_data, maintype='image', subtype='jpeg', filename='image.jpeg')

    if video_path:
        with open(video_path, 'rb') as file:
            video_data = file.read()

        msg.add_attachment(video_data, maintype='video', subtype='mp4', filename='video.mp4')

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv_file = request.files['csv-file']
        image_file = request.files['image-file']
        video_file = request.files['video-file']
        
        if csv_file:
            # Save the uploaded CSV file
            csv_path = 'Example.csv'
            csv_file.save(csv_path)

            # Read the CSV file containing name and email data
            data = pd.read_csv(csv_path)

            # Iterate through each row of the CSV data
            for _, row in data.iterrows():
                name = row['Name']
                email = row['Email']

                # Compose the email message
                subject = f"Hello, {name}!"
                message = f"Dear {name},\n\nThis is an automated email. Hope you are doing well.\n\nBest regards,\nYour Name"

                # Send the email with attachments (if provided)
                if image_file or video_file:
                    image_path = 'image.jpeg' if image_file else None
                    video_path = 'video.mp4' if video_file else None

                    if image_file:
                        image_file.save(image_path)

                    if video_file:
                        video_file.save(video_path)

                    send_email(email, subject, message, image_path=image_path, video_path=video_path)
                else:
                    send_email(email, subject, message)

            return 'Emails sent successfully!'
        else:
            return 'No CSV file provided.'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
