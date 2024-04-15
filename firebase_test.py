import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
import base64

# from dotenv import load_dotenv


# Load the environment variables from the .env file
# load_dotenv('FIREBASE_CREDENTIALS_JSON.env')

# # Get the JSON string from the environment variable
# my_cred = os.getenv('FIREBASE_CREDENTIALS_JSON')

# # Parse the JSON string into a Python dictionary
# my_cred_dict = json.loads(my_cred)

# # Use the dictionary to create the credentials
# cred = credentials.Certificate(my_cred_dict)

# # Initialize Firebase Admin with the credentials
# firebase_admin.initialize_app(cred)

# db = firestore.client()


# Construct the dictionary from environment variables
service_account_info = {
    "type": os.getenv('FIREBASE_TYPE'),
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),  # Adjust newlines if needed
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
}

# Initialize Firebase with the reconstructed credentials
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to add or update student data in the exam
def add_student_to_exam(exam_id, student_data):
    # Reference to the specific exam in the 'Student' collection
    exam_ref = db.collection('Student').document(exam_id)

    # Check if the exam document exists
    exam = exam_ref.get()
    if exam.exists:
        # Update the exam document with the new student data
        exam_ref.update({
            f'students.{student_data["student_id"]}': student_data
        })
    else:
        # Create the exam document with the student data if it does not exist
        exam_ref.set({
            'students': {
                student_data['student_id']: student_data
            }
        })
    print(f'Added/Updated data for student {student_data["student_id"]} in exam {exam_id}.')

# Student data for stu005
student_data = {
    'student_id': 'stu001',
    'answers': [
        {"question_id": "Q1", "text": "Explanation for Q1 by stu005."},
        {"question_id": "Q2", "text": "Explanation for Q2 by stu005."},
        {"question_id": "Q3", "text": "Explanation for Q3 by stu005."}
    ]
}

# Add or update stu005 in Exam001
# add_student_to_exam('Exam001', student_data)


# Function to retrieve and save all data from the 'Student' collection
def save_and_print_all_students():
    students_ref = db.collection('Student')
    students = students_ref.get()

    all_students = [student.to_dict() for student in students]

    # Convert the data to a JSON string with indentation
    json_data = json.dumps(all_students, indent=4)

    # Print the JSON data
    print(json_data)

    # Save the JSON data to a file
    with open('student.json', 'w') as f:
        f.write(json_data)

# Call the function
save_and_print_all_students()