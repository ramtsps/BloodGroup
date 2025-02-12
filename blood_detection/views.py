from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import  redirect
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
from django.http import JsonResponse
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from reportlab.pdfgen import canvas
from django.contrib import messages
import logging



logger = logging.getLogger(__name__)




# Load the trained model
model = load_model('model_blood_group_detection_resnet.h5')

# Define blood group labels
labels = {0: 'A+', 1: 'A-', 2: 'AB+', 3: 'AB-', 4: 'B+', 5: 'B-', 6: 'O+', 7: 'O-'}






def upload_image(request):
    """Render the upload page."""
    return render(request, 'upload.html')


# def predict_blood_group(request):
#     """Handle image upload and return blood group prediction."""
#     if request.method == 'POST' and request.FILES.get('image'):
#         img_file = request.FILES['image']
#         file_path = default_storage.save(f"uploads/{img_file.name}", img_file)

#         # Load and preprocess the image
#         img = image.load_img(file_path, target_size=(256, 256))
#         x = image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         x = preprocess_input(x)

#         # Predict using the model
#         result = model.predict(x)
#         predicted_class = np.argmax(result)
#         predicted_label = labels[predicted_class]
#         confidence = float(result[0][predicted_class]) * 100

#         # Delete the uploaded file after processing
#         os.remove(file_path)

#         # Return the result as JSON
#         return JsonResponse({"predicted_label": predicted_label, "confidence": confidence})

#     return JsonResponse({"error": "Invalid request"}, status=400)





from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from datetime import datetime

def generate_pdf_report(name, age, mobile, email, predicted_label, confidence, fingerprint_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    report_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Timestamp for the report

    # Ensure all icons exist
    icon_paths = {
        "email": os.path.join(BASE_DIR, "icons/email_icon.png"),
        "phone": os.path.join(BASE_DIR, "icons/phone_icon.png"),
        "blood": os.path.join(BASE_DIR, "icons/blood_icon.png"),
    }

    for key, path in icon_paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing icon file: {path}")

    # # Load Images
    # email_icon = ImageReader(icon_paths["email"])
    # phone_icon = ImageReader(icon_paths["phone"])
    # blood_icon = ImageReader(icon_paths["blood"])

    # Verify fingerprint file exists
    if not os.path.exists(fingerprint_path):
        raise FileNotFoundError(f"Fingerprint image not found: {fingerprint_path}")

    fingerprint_img = ImageReader(fingerprint_path)  # Load fingerprint image

    # PDF Path
    pdf_path = f"media/reports/{name}_blood_report.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Create PDF Canvas
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # 🔴 HEADER (Red Banner)
    c.setFillColor(colors.red)
    c.rect(0, height - 80, width, 80, fill=1)  # Red Header
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, "Blood Group Prediction Report")

    # 🕒 Test Date & Time
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.white)
    c.drawRightString(width - 20, height - 60, f"Date: {report_time}")  # Timestamp on top-right

    # 📌 USER DETAILS BOX (Blue Background)
    c.setFillColor(colors.lightblue)
    c.roundRect(50, height - 280, 500, 120, 10, fill=1)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)

    # 🔹 Name
    # c.drawImage(blood_icon, 60, height - 210, 20, 20)
    c.drawString(90, height - 205, f"Name: {name}")

    # 🔹 Age
    c.drawString(350, height - 205, f"Age: {age}")

    # 🔹 Mobile
    # c.drawImage(phone_icon, 60, height - 230, 20, 20)
    c.drawString(90, height - 225, f"Mobile: {mobile}")

    # 🔹 Email
    # c.drawImage(email_icon, 60, height - 250, 20, 20)
    c.drawString(90, height - 245, f"Email: {email}")

    # 🩸 PREDICTION RESULT BOX (Dark Blue)
    c.setFillColor(colors.darkblue)
    c.roundRect(50, height - 400, 500, 90, 10, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 350, f"Predicted Blood Group: {predicted_label}")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 375, f"Confidence Score: {confidence:.2f}%")

     # Fingerprint Section Background
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 600, "Fingerprint Sample")

    # 📸 Add Fingerprint Image
    c.drawImage(fingerprint_img, 180, height - 550, 250, 100, preserveAspectRatio=True, anchor='c') # Position the fingerprint image

    # ⚠️ FOOTER (Disclaimer)
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, 50, "This is an AI-generated prediction. Please confirm with a medical test.")

    c.save()
    return pdf_path


def send_email_with_report(email, pdf_path):
    """Send the blood group prediction report to the user's email with HTML design."""
    subject = "🔬 Your Blood Group Prediction Report is Ready!"
    
    message = """
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #d32f2f; text-align: center;">🩸 Blood Group Prediction Report</h2>
                <p style="color: #333; font-size: 16px;">
                    Dear Valued User,<br><br>
                    We are pleased to share your <b>Blood Group Prediction Report</b> generated by our <b>AI-powered system</b>.
                    Your fingerprint has been successfully analyzed, and the results are attached to this email.<br><br>
                </p>
                <hr style="border: 0; height: 1px; background: #ddd;">
                <h3 style="color: #1976d2;">📄 What’s Inside?</h3>
                <ul style="color: #555; font-size: 16px;">
                    <li>✔️ Your predicted blood group</li>
                    <li>✔️ Confidence score of the prediction</li>
                    <li>✔️ Additional insights about the AI model used</li>
                </ul>
                <hr style="border: 0; height: 1px; background: #ddd;">
                <p style="color: #333; font-size: 16px;">
                    Thank you for using our <b>AI Blood Detection System</b>! If you have any questions or require further assistance, feel free to contact us.
                </p>
                <p style="text-align: center; margin-top: 20px;">
                    <a href="mailto:support@aiblooddetection.com" 
                       style="background-color: #d32f2f; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">
                        Contact Support
                    </a>
                </p>
                <p style="text-align: center; color: #888; font-size: 14px; margin-top: 20px;">
                    Regards,<br>
                    <b>AI Blood Detection Team</b><br>
                    📧 support@aiblooddetection.com
                </p>
            </div>
        </body>
    </html>
    """

    email_msg = EmailMessage(subject, message, "parasuramtsps6@gmail.com", [email])
    email_msg.content_subtype = "html"  # Set the email content type to HTML
    email_msg.attach_file(pdf_path)
    email_msg.send()



def predict_blood_group(request):
    """Handle image upload, predict blood group, generate report, and send email."""
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            name = request.POST.get('name')
            age = request.POST.get('age')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            
            img_file = request.FILES['image']
            file_path = default_storage.save(f"uploads/{img_file.name}", img_file)

            # Load and preprocess the image
            img = image.load_img(file_path, target_size=(256, 256))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Predict using the model
            result = model.predict(x)
            if result is None or len(result) == 0:
                raise ValueError("Model returned an empty result.")

            predicted_class = np.argmax(result)
            predicted_label = labels.get(predicted_class, "Unknown")
            confidence = float(result[0][predicted_class]) * 100

            if predicted_label == "Unknown":
                raise ValueError("Invalid prediction output.")

            # Generate and send the report
            pdf_path = generate_pdf_report(name, age, mobile, email, predicted_label, confidence,file_path)
            send_email_with_report(email, pdf_path)

            return JsonResponse({"predicted_label": predicted_label, "confidence": confidence})
        
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return JsonResponse({"error": "Error in image processing. Please try again."}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render

def home(request):
    features = [
        {
            "icon": "https://cdn-icons-png.flaticon.com/512/2913/2913975.png",
            "title": "AI-Powered Detection",
            "description": "Utilizing state-of-the-art CNN architectures to detect blood groups from fingerprint images.",
        },
        {
            "icon": "https://cdn-icons-png.flaticon.com/512/6134/6134760.png",
            "title": "Dataset & Training",
            "description": "Trained on a dataset of 6,000–7,000 fingerprint images categorized by blood groups.",
        },
        {
            "icon": "https://cdn-icons-png.flaticon.com/512/2731/2731929.png",
            "title": "Performance Metrics",
            "description": "Accuracy and validation results stored for easy comparison of model performance.",
        },
    ]
    return render(request, "home.html", {"features": features})


def upload(request):
    return render(request, 'upload.html')

def result(request):
    return render(request, 'result.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        admin_email = 'admin@example.com'  # Replace with your actual admin email
        subject = f"New Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(subject, body, email, [admin_email])
            messages.success(request, "✅ Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "❌ Failed to send the message. Please try again later.")

        return redirect('contact')  # Redirect to the contact page

    return render(request, "contact.html")