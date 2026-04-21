from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample Data: College Knowledge Base
COLLEGE_DATA = {
    "admission": "Admissions are open from June to August. You can apply via the online portal.",
    "courses": "We offer B.Tech in CSE, ECE, Mechanical, and Civil Engineering, as well as MBA and MCA programs.",
    "library": "The central library is open from 8:00 AM to 10:00 PM on weekdays.",
    "placement": "Our top recruiters include TCS, AWS, and Accenture. The average CTC is 6.5 LPA.",
    "hostel": "We have separate hostels for boys and girls with 24/7 Wi-Fi and mess facilities.",
    "contact": "You can reach the administration office at admin@college.edu or +91 1234567890."
}

def get_response(user_input):
    user_input = user_input.lower()
    for key in COLLEGE_DATA:
        if key in user_input:
            return COLLEGE_DATA[key]
    return "I'm sorry, I don't have information on that. Please try asking about admissions, courses, or placements."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    response = get_response(user_message)
    return jsonify({"reply": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)