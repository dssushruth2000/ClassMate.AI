## This is perfect
# from flask import Flask, request, jsonify
# import google.generativeai as genai
# import json
# import time
# import os
# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables
# # 🔹 Load Google API Key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# app = Flask(__name__)

# # 🔹 Load Merged JSON File
# with open(r"D:\UWM_Classes\Sem_4\College_chatbot\datasets\cs_masters_regular_data.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # 🔹 Store chat history (resets when bot restarts)
# chat_history = []

# # 🔹 Function to Search Using Google Gemini and Restrict to JSON Data
# def search_gemini(user_query):
#     """Use Google Gemini AI for search while restricting it to JSON data."""
    
#     json_string = json.dumps(data, indent=2)  # Convert JSON to formatted text

#     # 🔹 Create a structured prompt for Gemini AI
#     prompt = f"""
#     You are an AI assistant that answers queries strictly based on the following dataset.
#     If the answer is not found in this dataset, reply with: "I could not find this information. Please feel free to vist the UWM Website https://uwm.edu/"

#     Here is the dataset:
#     {json_string}

#     Now, answer this user query using only the dataset above:
#     {user_query}
#     """

#     retries = 3  # Number of retries
#     delay = 2  # Initial delay for retries

#     for attempt in range(retries):
#         try:
#             model = genai.GenerativeModel("gemini-2.0-flash")  # Use Gemini AI model
#             response = model.generate_content(prompt)

#             if response.text:
#                 return {"response": response.text}
        
#         except Exception as e:
#             print(f"❌ Gemini API Error (Attempt {attempt+1}): {e}")

#             if "429" in str(e):  # Handle API rate limit
#                 print(f"⏳ Waiting {delay} seconds before retrying...")
#                 time.sleep(delay)
#                 delay *= 2  # Increase wait time exponentially (2s → 4s → 8s)
#             else:
#                 break  # If not a rate limit error, stop retrying

#     return {"response": "API quota exceeded. Please wait and try again later."}

# # 🔹 Flask API Route for Chatbot
# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     user_query = request.json.get("query", "").lower()
#     print(f"\nReceived Query: {user_query}")

#     # Step 1: Search with Google Gemini AI
#     matched_response = search_gemini(user_query)

#     if matched_response:
#         chat_history.append({"query": user_query, "response": matched_response["response"]})  # Store chat
#         print(f"Returning Google Gemini Response: {matched_response}")
#         return jsonify(matched_response)

#     print("❌ No match found in Gemini.")
#     return jsonify({"response": "I'm not sure. Try searching on the UWM website."})

# # 🔹 New API Endpoint to View Chat History (Session Only)
# @app.route("/chat_history", methods=["GET"])
# def get_chat_history():
#     """Retrieve chat history for the active session."""
#     return jsonify({"chat_history": chat_history})

# if __name__ == "__main__":
#     app.run(debug=True)


## In the below code im testing for multi-turn conversations - which works now
# from flask import Flask, request, jsonify
# import google.generativeai as genai
# import json
# import time
# import os
# from dotenv import load_dotenv
# from flask import render_template

# load_dotenv()  # Load environment variables
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# app = Flask(__name__)

# # 🔹 Load Merged JSON File (Dataset)
# with open(r"D:\UWM_Classes\Sem_4\College_chatbot\datasets\cs_masters_regular_data.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # 🔹 Store chat history (resets when bot restarts)
# chat_history = []

# def search_gemini(user_query, chat_memory):
#     """Use Google Gemini AI while ensuring responses come ONLY from the dataset."""

#     # 🔹 Convert dataset into a formatted JSON string
#     dataset_text = json.dumps(data, indent=2)

#     # 🔹 Convert chat history into a formatted text string
#     chat_history_text = "\n".join([f"User: {entry['query']}\nBot: {entry['response']}" for entry in chat_memory])

#     # 🔹 Construct the prompt to restrict responses to the dataset
#     prompt = f"""
#     You are an AI assistant that answers queries strictly based on the dataset provided below.
#     If the answer is not found in this dataset, reply with: "I could not find this information. Please feel free to visit the UWM Website https://uwm.edu/"

#     Previous conversation history:
#     {chat_history_text}

#     Dataset:
#     {dataset_text}

#     Now, continue the conversation and answer this user query using only the dataset above:
#     {user_query}
#     """

#     retries = 3
#     delay = 2

#     for attempt in range(retries):
#         try:
#             model = genai.GenerativeModel("gemini-2.0-flash")
#             response = model.generate_content(prompt)

#             if response.text:
#                 return {"response": response.text}
        
#         except Exception as e:
#             print(f"❌ Gemini API Error (Attempt {attempt+1}): {e}")

#             if "429" in str(e):
#                 print(f"⏳ Waiting {delay} seconds before retrying...")
#                 time.sleep(delay)
#                 delay *= 2
#             else:
#                 break

#     return {"response": "API quota exceeded. Please wait and try again later."}

# # 🔹 Flask API Route for Chatbot
# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     user_query = request.json.get("query", "").lower()
#     print(f"\nReceived Query: {user_query}")

#     # Step 1: Search with Google Gemini AI and pass chat history
#     matched_response = search_gemini(user_query, chat_history)

#     if matched_response:
#         chat_history.append({"query": user_query, "response": matched_response["response"]})  # Store chat
#         print(f"Returning Google Gemini Response: {matched_response}")
#         return jsonify(matched_response)

#     print("❌ No match found in Gemini.")
#     return jsonify({"response": "I'm not sure. Try searching on the UWM website."})

# # 🔹 New API Endpoint to View Chat History (Session Only)
# @app.route("/chat_history", methods=["GET"])
# def get_chat_history():
#     """Retrieve chat history for the active session."""
#     return jsonify({"chat_history": chat_history})

# #uncomment below code if you want to see the output in webpage
# @app.route("/")
# def chat_interface():
#     return render_template("chat.html")

# if __name__ == "__main__":
#     app.run(debug=True)


## In the below code im testing if there is a spelling mismatch or typos
# from flask import Flask, request, jsonify
# import google.generativeai as genai
# import json
# import time
# import os
# from dotenv import load_dotenv
# from flask import render_template

# load_dotenv()  # Load environment variables
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# app = Flask(__name__)

# # 🔹 Load Merged JSON File (Dataset)
# with open(r"D:\UWM_Classes\Sem_4\College_chatbot\datasets\cs_masters_regular_data.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # 🔹 Store chat history (resets when bot restarts)
# chat_history = []

# def search_gemini(user_query, chat_memory):
#     """Use Google Gemini AI while ensuring responses come ONLY from the dataset and correcting queries."""
    
#     # 🔹 Convert dataset into a formatted JSON string
#     dataset_text = json.dumps(data, indent=2)

#     # 🔹 Convert chat history into a formatted text string
#     chat_history_text = "\n".join([f"User: {entry['query']}\nBot: {entry['response']}" for entry in chat_memory])

#     # 🔹 Construct the prompt to:
#     #   ✅ Correct the query
#     #   ✅ Restrict responses to dataset
#     prompt = f"""
#     You are an AI assistant that answers queries strictly based on the dataset provided below.
#     If the user query contains spelling mistakes, typos, or unclear words, **first correct or clarify the query before searching**.
#     If the user query is already correct (e.g., "Hi", "Thank you", "Goodbye"), **respond naturally without saying "I believe..."**.
#     If the answer is not found in this dataset, reply with: "I could not find this information. Please feel free to visit the UWM Website https://uwm.edu/"

#     Previous conversation history:
#     {chat_history_text}

#     Dataset:
#     {dataset_text}

#     Step 1: If the user query is unclear or has typos, correct it.  
#     Step 2: Answer the corrected query using only the dataset above.  

#     User Query: {user_query}
#     """

#     retries = 3
#     delay = 2

#     for attempt in range(retries):
#         try:
#             model = genai.GenerativeModel("gemini-2.0-flash")
#             response = model.generate_content(prompt)

#             if response.text:
#                 return {"response": response.text}
        
#         except Exception as e:
#             print(f"❌ Gemini API Error (Attempt {attempt+1}): {e}")

#             if "429" in str(e):
#                 print(f"⏳ Waiting {delay} seconds before retrying...")
#                 time.sleep(delay)
#                 delay *= 2
#             else:
#                 break

#     return {"response": "API quota exceeded. Please wait and try again later."}

# # 🔹 Flask API Route for Chatbot
# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     user_query = request.json.get("query", "").lower()
#     print(f"\nReceived Query: {user_query}")

#     # Step 1: Send the query directly to Google Gemini AI
#     matched_response = search_gemini(user_query, chat_history)

#     # Store chat history
#     chat_history.append({"query": user_query, "response": matched_response["response"]})
#     print(f"Returning Response: {matched_response}")
    
#     return jsonify(matched_response)

# # 🔹 New API Endpoint to View Chat History (Session Only)
# @app.route("/chat_history", methods=["GET"])
# def get_chat_history():
#     """Retrieve chat history for the active session."""
#     return jsonify({"chat_history": chat_history})

# #uncomment below code if you want to see the output in webpage
# @app.route("/")
# def chat_interface():
#     return render_template("chat.html")

# if __name__ == "__main__":
#     app.run(debug=True)


## In the below code im improving this multi turn conversation - but the above code is perfect--- the below code is still perfect use below one
# from flask import Flask, request, jsonify
# import google.generativeai as genai
# import json
# import time
# import os
# from dotenv import load_dotenv
# from flask import render_template

# load_dotenv()  # Load environment variables
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# app = Flask(__name__)

# # 🔹 Load Merged JSON File (Dataset)
# with open(r"D:\UWM_Classes\Sem_4\College_chatbot\datasets\merged_data.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # # 🔹 Load and Merge Multiple JSON Files
# # json_files = [
# #     r"D:\UWM_Classes\Sem_4\College_chatbot\final_merging\combined_data.json",
# #     r"D:\UWM_Classes\Sem_4\College_chatbot\final_merging\cs_catalog.json",
# #     r"D:\UWM_Classes\Sem_4\College_chatbot\final_merging\professional_combined_data.json"
# # ]

# # data = {}  # Create an empty dictionary to merge JSON data

# # for file in json_files:
# #     with open(file, "r", encoding="utf-8") as f:
# #         json_data = json.load(f)
# #         data.update(json_data)  # Merge into a single dictionary


# # 🔹 Store chat history (resets when bot restarts)
# chat_history = []

# def search_gemini(user_query, chat_memory):
#     """Use Google Gemini AI while ensuring responses come ONLY from the dataset and correcting queries."""
    
#     # 🔹 Convert dataset into a formatted JSON string
#     dataset_text = json.dumps(data, indent=2)

#     # 🔹 Convert chat history into a formatted text string
#     chat_history_text = "\n".join([f"User: {entry['query']}\nBot: {entry['response']}" for entry in chat_memory])

#     # 🔹 Construct the prompt to:
#     #   ✅ Correct the query
#     #   ✅ Restrict responses to dataset
#     prompt = f"""
#     You are an AI assistant that answers queries strictly based on the dataset provided below.
#     If the user query contains spelling mistakes, typos, or unclear words, **first correct or clarify the query before searching**.
#     If the user query is already correct (e.g., "Hi", "Thank you", "Goodbye"), **respond naturally without saying "I believe..."**.
#     **Maintain conversation context:** If the user follows up, remember past exchanges.
#     **If the user asks a vague question (e.g., "What about AI?"), assume it refers to the previous topic.**
#     **If the user switches topics, prioritize the new question.**
#     If the answer is not found in this dataset, reply with: "I could not find this information. Please feel free to visit the UWM Website https://uwm.edu/"

#     Previous conversation history:
#     {chat_history_text}

#     Dataset:
#     {dataset_text}



#     User Query: {user_query}
#     """

#     retries = 3
#     delay = 2

#     for attempt in range(retries):
#         try:
#             model = genai.GenerativeModel("gemini-2.0-flash")
#             response = model.generate_content(prompt)

#             if response.text:
#                 return {"response": response.text}
        
#         except Exception as e:
#             print(f"❌ Gemini API Error (Attempt {attempt+1}): {e}")

#             if "429" in str(e):
#                 print(f"⏳ Waiting {delay} seconds before retrying...")
#                 time.sleep(delay)
#                 delay *= 2
#             else:
#                 break

#     return {"response": "API quota exceeded. Please wait and try again later."}

# # 🔹 Flask API Route for Chatbot
# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     user_query = request.json.get("query", "").lower()
#     print(f"\nReceived Query: {user_query}")

#     # Step 1: Send only the last 5 messages as context
#     matched_response = search_gemini(user_query, chat_history[-5:])

#     # Step 2: Store full chat history for frontend, but keep session memory short
#     chat_history.append({"query": user_query, "response": matched_response["response"]})

#     print(f"Returning Response: {matched_response}")
#     return jsonify(matched_response)



# # 🔹 New API Endpoint to View Chat History (Session Only)
# @app.route("/chat_history", methods=["GET"])
# def get_chat_history():
#     """Retrieve chat history for the active session."""
#     return jsonify({"chat_history": chat_history})

# #uncomment below code if you want to see the output in webpage
# @app.route("/")
# def chat_interface():
#     return render_template("chat.html")

# if __name__ == "__main__":
#     app.run(debug=True)




## In the below code i'm trying to act more like human -- done
from flask import Flask, request, jsonify, render_template, redirect, url_for
import google.generativeai as genai
import json
import time
import os
from dotenv import load_dotenv
import re
import markdown 
import csv
from datetime import datetime
from flask_mail import Mail, Message

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)


# 🔹 Load Merged JSON File (Dataset)
#with open(r"D:\UWM_Classes\Sem_4\College_chatbot\data_for_api\final_merged_data.json", "r", encoding="utf-8") as f:
with open("data_for_api/final_merged_data.json", "r", encoding="utf-8") as f:

    data = json.load(f)

# # 🔹 Load and Merge Multiple JSON Files
# json_files = [
#     r"D:\UWM_Classes\Sem_4\College_chatbot\final_merging\combined_data.json",
#     r"D:\UWM_Classes\Sem_4\College_chatbot\final_merging\cs_catalog.json",
#     r"D:\UWM_Classes\Sem_4\College_chatbot\final_merging\professional_combined_data.json"
# ]

# data = {}  # Create an empty dictionary to merge JSON data

# for file in json_files:
#     with open(file, "r", encoding="utf-8") as f:
#         json_data = json.load(f)
#         data.update(json_data)  # Merge into a single dictionary


# 🔹 Store chat history (resets when bot restarts)
chat_history = []

def search_gemini(user_query, chat_memory):
    """Use Google Gemini AI while ensuring responses come ONLY from the dataset and correcting queries."""
    
    # 🔹 Convert dataset into a formatted JSON string
    dataset_text = json.dumps(data, indent=2)

    # 🔹 Convert chat history into a formatted text string
    chat_history_text = "\n".join([f"User: {entry['query']}\nBot: {entry['response']}" for entry in chat_memory])

    # 🔹 Construct the prompt to:
    #   ✅ Correct the query
    #   ✅ Restrict responses to dataset
    #use this if you dont want below one "If the user asks a broad question, provide a structured response."
    prompt = f"""
    You are an AI assistant that answers queries based on the dataset provided below.
    If the user query contains spelling mistakes, typos, or unclear words, **first correct or clarify the query before searching**.
    If the user query is already correct (e.g., "Hi", "Thank you", "Goodbye"), **respond naturally without saying "I believe..."**.
    **Maintain conversation context:** If the user follows up, remember past exchanges.
    **If the user asks a vague question (e.g., "What about AI?"), assume it refers to the previous topic.**
    **If the user switches topics, prioritize the new question.**
    Instead of copying answers exactly, **summarize and explain them naturally** like a human.
    if the user asks a very broad question, politely ask what **specific aspect** they want to know.
    Respond in a **friendly and helpful tone**, as if you're talking to a student.
    Use **clear, simple explanations** instead of formal wording.
    **ALWAYS return a structured, clean response.**
    **DO NOT randomly change the structure** or rephrase in an inconsistent way.     
    **Use Markdown formatting (`**bold**`, `- bullets`, `[links](URL)`) to make responses clear.**
    Always Do NOT respond in JSON or code format.        
    If the answer is not found in this dataset, reply with: "I could not find this information. Please feel free to visit the UWM Website https://uwm.edu/"

    Previous conversation history:
    {chat_history_text}

    Dataset:
    {dataset_text}



    User Query: {user_query}
    """

    retries = 3
    delay = 2

    for attempt in range(retries):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            if response.text:
                return {"response": response.text}
            
        except Exception as e:
            print(f"❌ Gemini API Error (Attempt {attempt+1}): {e}")

            if "429" in str(e):
                print(f"⏳ Waiting {delay} seconds before retrying...")
                time.sleep(delay)
                delay *= 2
            else:
                break

    return {"response": "API quota exceeded. Please wait and try again later."}


#to send the appointment conformation email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USER')  # store in .env
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASS')  # store in .env
notify_email = os.getenv("NOTIFY_EMAIL")  # Load from .env

mail = Mail(app)


# 🔹 Flask API Route for Chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_query = request.json.get("query", "").lower()
    print(f"\nReceived Query: {user_query}")

    # Step 1: Send only the last 5 messages as context
    matched_response = search_gemini(user_query, chat_history[-5:])

    # Step 2: Store full chat history for frontend, but keep session memory short
    chat_history.append({"query": user_query, "response": matched_response["response"]})

    print(f"Returning Response: {matched_response}")
    return jsonify(matched_response)



# 🔹 New API Endpoint to View Chat History (Session Only)
@app.route("/chat_history", methods=["GET"])
def get_chat_history():
    """Retrieve chat history for the active session."""
    return jsonify({"chat_history": chat_history})

#uncomment below code if you want to see the output in webpage
@app.route("/")
def chat_interface():
    return render_template("index.html")

#to handle appointment form submissions
@app.route("/submit_appointment", methods=["POST"])
def submit_appointment():
    name = request.form.get("name")
    email = request.form.get("email")
    date = request.form.get("date")
    time_val = request.form.get("time")
    message = request.form.get("message")

    print("📅 Appointment Booked:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Date: {date}")
    print(f"Time: {time_val}")
    print(f"Message: {message}")

    # Append to a CSV file
    # with open('appointments/appointments.csv', mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([
    #         datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name, email, date, time_val, message
    #     ])

    csv_path = 'appointments/appointments.csv'
    file_exists = os.path.exists(csv_path)

    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Name", "Email", "Appointment Date", "Appointment Time", "Message"])
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            name, email, date, time_val, message
        ])
        print("Appointment Deatils Added to CSV File")

    # 🔹 Send confirmation email
    try:
        msg = Message("📅 New Appointment Booked!",
                sender=app.config['MAIL_USERNAME'],
                # recipients=[email])  # or use your own email to receive notification
                recipients=[email, notify_email]) #for both of them

        # msg.body = f"""
        # Hi {name},

        # Thank you for booking an appointment! Here are your details:

        # - 📅 Date: {date}
        # - 🕒 Time: {time_val}
        # - 💬 Message: {message}

        # We'll get back to you if needed. Have a great day!

        # – UWM Chatbot
        # """

        msg.html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; padding: 20px; background-color: #f9f9f9; border-radius: 8px;">
        <p>Hi <strong>{name}</strong>,</p>
        <p>Thanks for booking an appointment! Here's what we received:</p>
        <ul style="line-height: 1.6;">
            <li><strong>🗓️ Date:</strong> {date}</li>
            <li><strong>🕒 Time:</strong> {time_val}</li>
            <li><strong>💬 Message:</strong> {message}</li>
        </ul>
        <p style="margin-top: 10px;">We’ll get back to you if needed. Have a great day!</p>
        <p style="color: #555;">– <em>UWM Chatbot</em></p>
        </div>
        """

        mail.send(msg)
        print("✅ Email sent successfully to:", email)

    except Exception as e:
        print("❌ Error sending email:", str(e))

    # Optionally return a thank you message (or redirect)
    return "<script>alert('Appointment submitted successfully!'); window.history.back();</script>"

    


if __name__ == "__main__":
    app.run(debug=True)