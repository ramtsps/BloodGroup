# Blood Group Detection from Fingerprints

A deep learning-based web application that detects blood groups from fingerprint images using Convolutional Neural Networks (CNN).

## Project Overview

This application uses advanced CNN models to analyze fingerprint images and determine blood groups with high accuracy. The system is built with Django and TensorFlow, providing a user-friendly interface for blood group detection.

## Features

- **AI-Powered Detection**: Utilizes state-of-the-art CNN architectures to detect blood groups from fingerprint images
- **Dataset & Training**: Trained on a dataset of 6,000–7,000 fingerprint images categorized by blood groups
- **Performance Metrics**: Accuracy and validation results stored for easy comparison of model performance
- **PDF Report Generation**: Creates detailed reports with detection results
- **User-Friendly Interface**: Simple and intuitive UI designed for ease of use

## System Flowchart

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  User uploads   │────▶│  Image pre-     │────▶│  CNN model      │
│  fingerprint    │     │  processing     │     │  prediction     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
┌─────────────────┐     ┌─────────────────┐     ┌────────▼────────┐
│                 │     │                 │     │                 │
│  Email sent     │◀────│  PDF report     │◀────│  Blood group    │
│  to user        │     │  generation     │     │  classification │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## How It Works

1. **Upload Your Fingerprint**: Provide a clear fingerprint image for analysis
2. **AI-Powered Analysis**: Our deep learning model processes your fingerprint
3. **Instant Blood Group Detection**: Receive your blood group result in seconds

## Detailed Process Flow

1. User uploads a fingerprint image through the web interface
2. The image is preprocessed (resized to 256x256 pixels and normalized)
3. The preprocessed image is fed into the ResNet CNN model
4. The model predicts the blood group with a confidence score
5. A detailed PDF report is generated with the prediction results
6. The report is emailed to the user's provided email address
7. Results are displayed on the web interface

## Technology Stack

- **Backend**: Django, Python
- **Machine Learning**: TensorFlow, Keras
- **Frontend**: HTML, CSS, Bootstrap
- **Deployment**: Gunicorn, Whitenoise

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/blood-group-detection.git
   cd blood-group-detection
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```
   python manage.py migrate
   ```

4. Collect static files:

   ```
   python manage.py collectstatic
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

## Deployment

This project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration.

## Dataset Structure

The model is trained on a dataset of over 6,000 fingerprint images organized into 8 blood group categories.

## License

This project uses various open-source components:

- Font Awesome icons under SIL OFL 1.1
- Various JavaScript libraries under MIT License

## Contact

For more information, please visit the contact page on the application.
