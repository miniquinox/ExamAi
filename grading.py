import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin using the service account
part1 = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDTJyq9aT0aR24T\n6V/tk+7QC1nvxmLOKWDmJ8RDKTFYz86j"
part_11 = "nhMEoiXQXH0ubWLU6wabaeTibqGOACz0\nfjK3Na7m3d1UCrqt/IXzhZ+TkJirSVzfEys6bxk0Y8cDcyLJrrj2PqesXSlzEx/y\nMvNoiCBph9wwDFEZQ4zI/1DcU"
part_12 = "996zhk1Te0XlCuUfXIrm2a/kLraVS9cI2TWmPqH\nuJH7N7/ZnHzdc/XOL6tlWBHr11qZK3laMyHXExG2GvmBnJDXCr+UCbLnq5xDjEZ+\n3fKtbelmufdZQDqAuyqM6"
part2 = "33jAoZijS6o+TsDvFMJkyghKlTNDT/GnHgkWRlchrPP\n1VfcQprTAgMBAAECggEAVxw4cK3i7F19ly9XSO8XvbKBJv9EMeM2O506Ra7P0eDh\nUfTbybSPPxd4+V"
part_21 = "ddR5OyRRl5uMSFV8zQvwj1KUo3Xr03Gv3WKAMey+lbfQhRQ5Df\nhJQm6FN/JXLoXo74UhYH7mbIy74fZH8GVegZLQ3DuWW4PAZIytBoW1+hX1QmxUVT\naSvD6H"
part_22 = "3j9db6auHZihaDGBYPDwxNH0lMy0eoFFOpiH9KY4Lc4XYEIfQqk/peiUEE\n84P7f4QTfZkUWXguonVDwQQKzRPMyWLwFHCjqZec2VtPDH7yGDSTWKzQbYv+XmLy\ndoH"
part_23 = "pcbT+hD2Bn1XLgOA/abmhnjDvtGk71T57hq4UsQKBgQDz4kKrex56Sl0VE1HJ\n3rXfSTgL/MueJh3yIMCzG2LsB+767UR7pRYsAJ7p0x8zH9pTRBgwd/ITogLF"
part_24 = "wthC\nrvBMhOCuL5UP92xX3seyhiObhqZ88YSRRi14u8RCFhsRU7owmmn0BGlsCYvlFL6g\nkkWlZKOhBcHIz+TZIgytX7L62QKBgQDdpKHmRBxrT3UwhybZlN6iRt"
part_25 = "dmuI0+QIo4\nNAX+hKvIY5k8kHm04ZNSwlrAJmIGF20iv5UphktuJpwKx3t"
part3 = "2jX43k038Nxo2sNpy\npCHz5FX5hUph1haqr3lGeF2U89M+J+mpVBB+ly9f2Czaad70yfvWi7y4tVV7Ke7g\n0cLdK4E/iwKBgALGro+ZJS2rLwgQYjv0Bwn1oWexhvf"
part_31 = "T4z9gVBE13JhnNrcwgDkQ\nFgKGN0jeGFrSn/+WpNfYZa8HhxSNNTz9FMsqMAyLihzWaitN4+QKVtlsXPTLIwEs\nVVQsfv1plwFJfLMU7uPSMQkDys3ewJS/VX+"
part_32 = "ed6ZblGsewrIeCxrmHflxAoGBAMMT\n7fNPq3u/ubN2oPkMkE9f7qJYeOh7wavqDgSQHOoIz4yA1L4hdJt4uIs6vTgDUmkt\nGkosCyPuE5VhMgeMTbT4j8EXdpkAW"
part_33 = "6RfVgrlw84URP2LgvPD8gfWVPePCzQ/yObi\nOIpS4r2G9SNf336wcFnLL9WatJvssnVp6grkCaQ1AoGBAKbD8qiMG+x+Nd4/GWxW\n7Ahl1N+wgdsrn6VbTVNP7oA0"
part_34 = "ju7blRPZlLw7AuETULKl/LYT93aebdTax20Wo7/Q\nb9jn5Pfghiu/Z1De1ZdqZNxQSkKVTR2WHr1rgBtMg02yfaiSavibOIUVT1HEDyli\nKxpaNP3T4/7IZbjGiZ9"
part_35 = "hJOAb\n-----END PRIVATE KEY-----\n"

my_cred = {
  "type": "service_account",
  "project_id": "examai-0228",
  "private_key_id": "cb201016aa944bde90a2ab94f094a259cb63c2bd",
  "private_key": part1 + part_11 + part_12 + part2 + part_21 + part_22 + part_23 + part_24 + part_25 + part3 + part_31 + part_32 + part_33 + part_34 + part_35,
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

def ask_gpt(question):
    key1 = "sk-XXofCUszTzeSX"
    key2 = "8HeAy85T3BlbkFJe"
    key3 = "lhWc2AUBFmbhRzFvwJD"
    keys = key1 + key2 + key3
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keys}"
    }
    data = {
        # "model": "gpt-3.5-turbo",
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a college professor who will grade assignments based on student submissions and rubrics."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # This will raise an exception if the response contains an HTTP error status code
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content']
    return answer

# Function to load data from Firestore
def load_firebase(database):
    ref = db.collection(database)
    return [doc.to_dict() for doc in ref.get()]

# Process each student's data
exam_results = {
    "exam_id": "exam001",
    "students": []
}

professor_json = load_firebase("Professor")
midterm_questions = professor_json[0]["BAX 423 - Big Data Analytics"]["exams"]["MidTermExam"]["questions"]

students_json = load_firebase("Student")
for student_dict in students_json[0]["students"]:
    for student_id, answers in student_dict.items():
        student_result = {
            "student_id": student_id,
            "grades": [],
            "final_grade": 0
        }
        total_score = 0
        for question_dict in answers:
            for question_id, student_answer in question_dict.items():
                # print(question_id)
                student_question = next((item for item in midterm_questions if item['text'] == question_id), None)
                # print(student_question)
                if student_question and student_answer:
                    prompt = (
                        "Below you have a question and an answer from a student. "
                        "The question includes a set of rubrics and weights asigned to each rubric. "
                        "The answer includes both the question and the student's response. "
                        "Grade the student's answer based on the rubrics and weights provided in the question. "
                        "The output must be a json following this format, and using double quotes: "
                        '{"question_id": <insert the Question here>, "rubric_scores": [<score1>, <score2>, ...], "total_score": <sum of all rubrics scores>, "feedback": <Constructive feedback based on the students answer and how it could be improved>}'
                        "Add your graded scores per rubric in the rubric_scores list based on your best assessment."
                        "DO NOT DEVIATE FROM THIS FORMAT, DOING SO WILL HURT MY PROGRAM. Print everything in one line.\n\n"
                        f"Question: {question_id}\n\n"
                        f"Rubrics: {student_question['rubrics']}\n\n"
                        f"Answer: {student_answer}\n\n"
                        "Make sure the JSON is properly formatted and it has no syntax errors. Don't write code, just assess the student's answer."
                    )
                    # print(prompt, "\n\n")
                    graded_response = ask_gpt(prompt)
                    result_dict = json.loads(graded_response)
                    total_score += result_dict["total_score"]
                    student_result["grades"].append(result_dict)
        student_result["final_grade"] = total_score
        exam_results["students"].append(student_result)

# Output the final JSON
print(json.dumps(exam_results, indent=4))