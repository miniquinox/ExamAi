import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Initialize Firebase Admin using the service account
part1 = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDTJyq9aT0aR24T\n6V/tk+7QC1nvxmLOKWDmJ8RDKTFYz86jnhMEoiXQXH0ubWLU6wabaeTibqGOACz0\nfjK3Na7m3d1UCrqt/IXzhZ+TkJirSVzfEys6bxk0Y8cDcyLJrrj2PqesXSlzEx/y\nMvNoiCBph9wwDFEZQ4zI/1DcU996zhk1Te0XlCuUfXIrm2a/kLraVS9cI2TWmPqH\nuJH7N7/ZnHzdc/XOL6tlWBHr11qZK3laMyHXExG2GvmBnJDXCr+UCbLnq5xDjEZ+\n3fKtbelmufdZQDqAuyqM6"
part2 = "33jAoZijS6o+TsDvFMJkyghKlTNDT/GnHgkWRlchrPP\n1VfcQprTAgMBAAECggEAVxw4cK3i7F19ly9XSO8XvbKBJv9EMeM2O506Ra7P0eDh\nUfTbybSPPxd4+VddR5OyRRl5uMSFV8zQvwj1KUo3Xr03Gv3WKAMey+lbfQhRQ5Df\nhJQm6FN/JXLoXo74UhYH7mbIy74fZH8GVegZLQ3DuWW4PAZIytBoW1+hX1QmxUVT\naSvD6H3j9db6auHZihaDGBYPDwxNH0lMy0eoFFOpiH9KY4Lc4XYEIfQqk/peiUEE\n84P7f4QTfZkUWXguonVDwQQKzRPMyWLwFHCjqZec2VtPDH7yGDSTWKzQbYv+XmLy\ndoHpcbT+hD2Bn1XLgOA/abmhnjDvtGk71T57hq4UsQKBgQDz4kKrex56Sl0VE1HJ\n3rXfSTgL/MueJh3yIMCzG2LsB+767UR7pRYsAJ7p0x8zH9pTRBgwd/ITogLFwthC\nrvBMhOCuL5UP92xX3seyhiObhqZ88YSRRi14u8RCFhsRU7owmmn0BGlsCYvlFL6g\nkkWlZKOhBcHIz+TZIgytX7L62QKBgQDdpKHmRBxrT3UwhybZlN6iRtdmuI0+QIo4\nNAX+hKvIY5k8kHm04ZNSwlrAJmIGF20iv5UphktuJpwKx3t"
part3 = "2jX43k038Nxo2sNpy\npCHz5FX5hUph1haqr3lGeF2U89M+J+mpVBB+ly9f2Czaad70yfvWi7y4tVV7Ke7g\n0cLdK4E/iwKBgALGro+ZJS2rLwgQYjv0Bwn1oWexhvfT4z9gVBE13JhnNrcwgDkQ\nFgKGN0jeGFrSn/+WpNfYZa8HhxSNNTz9FMsqMAyLihzWaitN4+QKVtlsXPTLIwEs\nVVQsfv1plwFJfLMU7uPSMQkDys3ewJS/VX+ed6ZblGsewrIeCxrmHflxAoGBAMMT\n7fNPq3u/ubN2oPkMkE9f7qJYeOh7wavqDgSQHOoIz4yA1L4hdJt4uIs6vTgDUmkt\nGkosCyPuE5VhMgeMTbT4j8EXdpkAW6RfVgrlw84URP2LgvPD8gfWVPePCzQ/yObi\nOIpS4r2G9SNf336wcFnLL9WatJvssnVp6grkCaQ1AoGBAKbD8qiMG+x+Nd4/GWxW\n7Ahl1N+wgdsrn6VbTVNP7oA0ju7blRPZlLw7AuETULKl/LYT93aebdTax20Wo7/Q\nb9jn5Pfghiu/Z1De1ZdqZNxQSkKVTR2WHr1rgBtMg02yfaiSavibOIUVT1HEDyli\nKxpaNP3T4/7IZbjGiZ9hJOAb\n-----END PRIVATE KEY-----\n"

my_cred = {
  "type": "service_account",
  "project_id": "examai-0228",
  "private_key_id": "cb201016aa944bde90a2ab94f094a259cb63c2bd",
  "private_key": part1 + part2 + part3,
  "client_email": "firebase-adminsdk-cxdcl@examai-0228.iam.gserviceaccount.com",
  "client_id": "105408726183895905662",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-cxdcl%40examai-0228.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(my_cred)
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