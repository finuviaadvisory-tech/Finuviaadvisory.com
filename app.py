from flask import Flask, render_template, request, jsonify

import csv

import os



app = Flask(__name__)



# File path for storing inquiries

DATA_FILE = 'inquiries.csv'



# Ensure the CSV has headers if it doesn't exist

if not os.path.exists(DATA_FILE):

    with open(DATA_FILE, mode='w', newline='') as f:

        writer = csv.writer(f)

        writer.writerow(['Name','service','email id', 'Message'])

       



@app.route('/')

def home():

    return render_template('index.html')



@app.route('/gst')

def gst_page():

    return render_template('gst.html')



@app.route('/income')

def tax_page():

    return render_template('income.html')



@app.route('/msme')

def msme_page():

    return render_template('msme.html')



# Add 'REVIEWS_FILE' near your other file path

REVIEWS_FILE = 'reviews.csv'



# Ensure the Reviews CSV has headers

if not os.path.exists(REVIEWS_FILE):

    with open(REVIEWS_FILE, mode='w', newline='') as f:

        writer = csv.writer(f)

        writer.writerow(['Name', 'Rating', 'Comments'])



# --- NEW ROUTE: SUBMIT REVIEW ---

@app.route('/submit_review', methods=['POST'])

def receive_review():

    try:

        data = request.get_json()

        name = data.get('name') or "Anonymous"

        rating = data.get('rating')

        comments = data.get('comments')



        with open(REVIEWS_FILE, mode='a', newline='') as f:

            writer = csv.writer(f)

            writer.writerow([name, rating, comments])



        return jsonify({"status": "success"}), 200

    except Exception as e:

        return jsonify({"status": "error", "message": str(e)}), 500



# --- NEW ROUTE: GET ALL REVIEWS ---

@app.route('/get_reviews', methods=['GET'])

def get_reviews():

    reviews = []

    if os.path.exists(REVIEWS_FILE):

        with open(REVIEWS_FILE, mode='r') as f:

            reader = csv.DictReader(f)

            for row in reader:

                reviews.append(row)

    return jsonify(reviews)



@app.route('/submit_contact', methods=['POST'])

def receive_contact():

    try:

        data = request.get_json()

        name = data.get('name')

        email = data.get('email')

        message = data.get('message')



        # Log to terminal for visibility

        print(f"New Contact: {name} - {email}")



        # Save to CSV file

        with open(DATA_FILE, mode='a', newline='') as f:

            writer = csv.writer(f)

            writer.writerow([name, email, message])



        return jsonify({"status": "success"}), 200

   

    except Exception as e:

        print(f"Error saving data: {e}")

        return jsonify({"status": "error"}), 500

   



if __name__ == '__main__':

    app.run(debug=True)

   