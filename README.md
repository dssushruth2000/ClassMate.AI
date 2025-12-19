===========================================================================================
   UWM Chatbot: An LLM Assistant for the Computer Science Website - README (LOCAL USE)
===========================================================================================

Project: AI Chatbot for UWM Computer Science Department  
Developer: Sushruth Danivasa Sridhar  
Advisor: Prof. Rohit Kate  
Program: MS in Computer Science, University of Wisconsin–Milwaukee

-----------------------------------------------------
Disclaimer
-----------------------------------------------------
This is a demo chatbot website project created for educational purposes only. It mimics the style and layout of the University of Wisconsin-Milwaukee's official website for practice and demonstration.

-----------------------------------------------------
PROJECT OVERVIEW
-----------------------------------------------------
This is a fully functional AI chatbot designed to assist students with queries related to the Computer Science programs at UWM. 

The bot is powered by Google Gemini API and is trained using structured JSON data extracted via custom-built web scrapers from UWM websites, including:

- CS Master's (Regular + Professional Track)
- CS Accelerated Master's
- CS Bachelor's
- CS Catalog
- Faculty and FAQ pages

Features:
- Chatbot answers queries based only on UWM CS web data
- Real-time chat with animations, avatars, Markdown formatting
- In-chat appointment booking form
- Appointment data saved in CSV and email confirmations sent
- Admin dashboard to monitor appointment bookings

-----------------------------------------------------
HOW TO RUN THE WEBSCRAPING MODULES
-----------------------------------------------------

If you wish to regenerate the dataset from UWM websites using the scraping scripts, follow these steps:

All the structured JSON data used by the chatbot was generated using the notebook:
📁 Web_scraping_from_website.ipynb

To regenerate the data:
1. Open the notebook in VS Code.
2. Run each code cell **in top-down order**.
3. This will scrape content from the UWM CS program websites and produce merged files inside:
   - `datasets/` (intermediate JSONs)
   - `final_merging/` (cleaned, final JSONs)
   - `data_for_api/final_merged_data.json` (used by the chatbot)

Note: Ensure you are connected to the internet while scraping.

This will generate `final_merged_data.json` inside the `data_for_api/` folder, which is then used by the chatbot.

-----------------------------------------------------
HOW TO RUN LOCALLY
-----------------------------------------------------

1. Clone or download the project folder.

2. (Optional) Create a virtual environment:

   On Mac/Linux:
     python3 -m venv venv
     source venv/bin/activate

   On Windows:
     python -m venv venv
     venv\Scripts\activate

3. Install Python dependencies:
   pip install -r requirements.txt

   If requirements.txt is missing:
   pip install flask flask-mail python-dotenv google-generativeai beautifulsoup4 requests

4. Set up the .env file in the root folder with the following:

   GEMINI_API_KEY=your_gemini_api_key  
   GMAIL_USER=your_email@gmail.com  
   GMAIL_PASS=your_app_password  
   NOTIFY_EMAIL=admin_email@gmail.com

   (Note: Use Gmail App Password if 2FA is enabled.)

5. Ensure these folders exist:
   - appointments/
   - data_for_api/
   - static/avatar/
   - static/sounds/
   - static/uploads/

   Place the required avatar images, sound effects, and video assets in the correct `static` subfolders. (if not already present.)

6. Run the application:
   python apiapp.py

7. Open the app in your browser:
   http://127.0.0.1:5000/

8. To access the Admin Appointment Dashboard:
   http://127.0.0.1:5000/admin/dashboard  
   Password: chatbot123

	The main backend entry point is: `apiapp.py`  
	The main frontend file is: `templates/index.html`

-----------------------------------------------------
OPTIONAL: AZURE HOSTED VERSION
-----------------------------------------------------
This chatbot is also hosted on Microsoft Azure for demonstration purposes.

You can optionally try the **Live Demo** here:  
https://college-chatbot-gde7a6atdygbd0da.centralus-01.azurewebsites.net/

(Note: Some features like email may be restricted in the demo.)

-----------------------------------------------------
NOTES
-----------------------------------------------------
- The chatbot uses structured prompting to guide Gemini Flash to stay grounded in the JSON dataset.
- All data used is publicly available on UWM’s Computer Science websites.
- This project is for academic use and is not affiliated with UWM officially.
- Do not use this codebase for any commercial or public-facing deployment without appropriate rights or permissions.

---
© The original design and assets are credited to the University of Wisconsin-Milwaukee.