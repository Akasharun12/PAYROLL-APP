from flask import Flask, render_template, request
import pandas as pd
import mysql.connector

from textblob import TextBlob
import random
from googletrans import Translator
import os

app = Flask(__name__)

# Flask configuration for MySQL parameters
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'Akash@17')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'neura')

def translate_text(text, target_language='en'):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return connection
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result1', methods=['POST'])
def result():
    input_ename = request.form['ename']
    input_empid = int(request.form['empid'])

    # MySQL connection
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor(dictionary=True)

        # Query MySQL to get employee data based on ename and empid
        query = f"SELECT * FROM emp_modified WHERE ename = '{input_ename}' AND empid = {input_empid}"
        cursor.execute(query)
        result = cursor.fetchone()

        connection.close()

        if result:
            annincome_value = result['annincome']
            month_Jan = result['janms']
        
            month_Feb = result['febms']
            month_Mar = result['marms']
            month_Apr = result['aprms']
            month_May = result['mayms']
            month_Jun = result['junems']
            month_Jul = result['julyms']
            month_Aug = result['augms']
            month_Sep = result['sepms']
            month_Oct = result['octms']
            month_Nov = result['novms']
            month_Dec = result['decms']

            return render_template('result.html', ename=input_ename, annincome=annincome_value,
                                month_Jan=month_Jan, month_Feb=month_Feb, month_Mar=month_Mar,
                                month_Apr=month_Apr, month_May=month_May, month_Jun=month_Jun,
                                month_Jul=month_Jul, month_Aug=month_Aug, month_Sep=month_Sep,
                                month_Oct=month_Oct, month_Nov=month_Nov, month_Dec=month_Dec)
        else:
            return render_template('no_result1.html', ename=input_ename, empid=input_empid)
    else:
        return "Unable to establish MySQL connection."


@app.route('/ask_question', methods=['POST'])
def ask_question():
    input_ename = request.form['ename']
    annincome_value = float(request.form['annincome'])
    month_Jan = float(request.form['month_Jan'])
    month_Feb = float(request.form['month_Feb'])
    month_Mar = float(request.form['month_Mar'])
    month_Apr = float(request.form['month_Apr'])
    month_May = float(request.form['month_May'])
    month_Jun = float(request.form['month_Jun'])
    month_Jul = float(request.form['month_Jul'])
    month_Aug = float(request.form['month_Aug'])
    month_Sep = float(request.form['month_Sep'])
    month_Oct = float(request.form['month_Oct'])
    month_Nov = float(request.form['month_Nov'])
    month_Dec = float(request.form['month_Dec'])

    # Add similar assignments for other months
    
    #user_question = request.form['user_question']
    user_question = request.form['user_question'].encode('utf-8').decode('utf-8')
    user_question = str(TextBlob(user_question).correct()).lower()
    user_question = translate_text(user_question)

    positive_responses = [
    "Absolutely, I can help you with that.",
    "Yes, sure Im here to assist you.",
    "Certainly, you can view your salary using this information.",
    "Of course, Id be happy to guide you on that.",
    "Definitely, let me provide you with the necessary information.",
    "Sure thing! I can provide the information you need.",
    "Absolutely, consider it done. Im here to help.",
    "Yes, absolutely Im here to support you.",
    "Certainly, your inquiry is important, and I can help address it.",
    "Absolutely, your satisfaction is my priority.",
    "Yes, no doubt about it. I can provide the necessary information.",
    "Sure, count on me to guide you through the process.",
    "Absolutely, your request is well within my capabilities to assist.",
    "Yes, without a doubt. I can assist you with that inquiry.",
    "Yes, that's definitely something I can assist you with.",
    "Of course, Im more than happy to help with that.",
    "Certainly, Im well-equipped to help you with that.",
    "Yes, without hesitation, I can guide you through the necessary steps.",
    "Yes, I can certainly point you in the right direction for that.",
    "Certainly, Im here to assist you every step of the way.",
    "Absolutely, let me explain how you can easily view your salary.",
    "Yes, absolutely! Im here to make things easier for you.",
    "Of course, consider it done. Im here for your assistance.",
    "Sure thing! Im here to ensure your needs are met.",
    "Yes, no problem at all. I can help you with that.",
    "Certainly, Im at your service",
    "Certainly, I can guide you through the process of checking your salary.",
    "Yes, Im here to help, and here's how you can view your salary.",
    "Certainly, Im here to assist you. How may I help?",
]
    
    negative_responses = [
    "Im sorry, but I cant assist with that.",
    "Unfortunately, Im unable to provide help in this case.",
    "I apologize, but I cant offer assistance for that query.",
    "Regrettably, I dont have the information youre looking for.",
    "Im afraid I cant help with that specific request.",
    "Sorry, this is beyond the scope of my capabilities.",
    "I wish I could assist, but this is not within my abilities.",
    "Im sorry, but thats not something I can handle.",
    "Unfortunately, I dont have the necessary information for that.",
    "I apologize, but I cant fulfill that request.",
    "Sorry, I cant provide the information you're seeking.",
    "Regrettably, I'm not equipped to assist with that.",
    "Im afraid I cant generate the information you need.",
    "Unfortunately, I cant offer guidance on that matter.",
    "I apologize, but I dont have the capability to help with that.",
    "Sorry, but I dont possess the information required for that request.",
    "Im sorry, I cant provide the assistance youre looking for.",
    "Regrettably, thats not within my purview to address.",
    "Unfortunately, I cant generate the requested information.",
    "Im afraid I dont have the means to assist with that inquiry.",
    "Im sorry, but I cant fulfill that particular request.",
    "I apologize, but I don't have the necessary data for that.",
    "Regrettably, Im not able to provide help in this case.",
    "Im afraid I can't offer guidance on that specific matter.",
    "Sorry, I cant generate the information youre requesting.",
    "Unfortunately, Im not equipped to handle that query.",
    "Im sorry, but I cant provide the assistance youre seeking.",
    "Regrettably, that's outside the scope of my capabilities.",
    "Unfortunately, I dont have the information youre looking for.",
    "I apologize, but I cant fulfill that request.",
]



    if "annual salary" in user_question or "annual income" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your annual income is: {annincome_value}."

    elif "january salary" in user_question or "january month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your January month salary is: {month_Jan}."

    elif "february salary" in user_question or "february month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your February month salary is: {month_Feb}."

    elif "march salary" in user_question or "march month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your March month salary is: {month_Mar}."

    elif "april salary" in user_question or "april month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your April month salary is: {month_Apr}."

    elif "may salary" in user_question or "may month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your May month salary is: {month_May}."

    elif "june salary" in user_question or "june month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your June month salary is: {month_Jun}."
    
    elif "july salary" in user_question or "july month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your July month salary is: {month_Jul}."

    elif "august salary" in user_question or "august month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your August month salary is: {month_Aug}."

    elif "september salary" in user_question or "september month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your September month salary is: {month_Sep}."

    elif "october salary" in user_question or "october month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your October month salary is: {month_Oct}."

    elif "november salary" in user_question or "november month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your November month salary is: {month_Nov}."

    elif "december salary" in user_question or "december month salary" in user_question:
        response_prefix = random.choice(positive_responses)
        response = f"{response_prefix} Your December month salary is: {month_Dec}."


    else:
        response_prefix = random.choice(negative_responses)
        response = f"{response_prefix}"

    return render_template('result.html', ename=input_ename, annincome=annincome_value,
                       month_Jan=month_Jan, month_Feb=month_Feb, month_Mar=month_Mar,
                       month_Apr=month_Apr, month_May=month_May, month_Jun=month_Jun,
                       month_Jul=month_Jul, month_Aug=month_Aug, month_Sep=month_Sep,
                       month_Oct=month_Oct, month_Nov=month_Nov, month_Dec=month_Dec,
                       user_question=user_question, response=response)

if __name__ == '__main__':
    app.run(debug=True, port=8000)