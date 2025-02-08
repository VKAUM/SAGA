import tkinter as tk
import subprocess
from tkinter import messagebox, filedialog
from tkhtmlview import HTMLLabel
import pymongo

# MongoDB Atlas connection URI
MONGO_URI = "mongodb+srv://Vishi:vishi@cluster0.25t03hn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB client
client = pymongo.MongoClient(MONGO_URI)

# Database name
db = client.mydatabase

# Collection name for user accounts
users_collection = db.users

# Collection name for user account details
account_details_collection = db.myaccountdetails  # Define the collection for user account details

class PRAGYANApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PRAGYAN")
        self.geometry("800x600")
        self.current_screen = None
        self.create_layout()

    def create_layout(self):
        # Welcome Screen Frame
        self.welcome_frame = tk.Frame(self)
        self.welcome_frame.pack(fill="both", expand=True)

        label = tk.Label(self.welcome_frame, text="Welcome to PRAGYAN", font=("Helvetica", 20))
        label.pack(pady=20)

        next_button = tk.Button(self.welcome_frame, text="Next", command=self.show_signup_login_screen)
        next_button.pack()

        # Signup/Login Screen Frame
        self.signup_login_frame = tk.Frame(self)
        # Define layout for Signup/Login screen

        # Terms and Conditions Screen Frame
        self.terms_conditions_frame = tk.Frame(self)
        # Define layout for Terms and Conditions screen

        # Personal Details Screen Frame
        self.personal_details_frame = tk.Frame(self)
        # Define layout for Personal Details screen

        # Test Screen Frame
        self.test_frame = tk.Frame(self)
        # Define layout for Test screen

    def show_frame(self, frame):
        if self.current_screen:
            self.current_screen.pack_forget()  # Hide the current screen
        self.current_screen = frame
        self.current_screen.pack(fill="both", expand=True)

    def show_signup_login_screen(self):
        self.show_frame(self.signup_login_frame)

    def show_terms_conditions_screen(self):
        self.show_frame(self.terms_conditions_frame)

    def show_personal_details_screen(self):
        self.show_frame(self.personal_details_frame)

    def show_test_screen(self):
        self.show_frame(self.test_frame)

class WelcomeScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PRAGYAN")
        self.geometry("400x200")
        self.center_window()

        label = tk.Label(self, text="Welcome to PRAGYAN", font=("Helvetica", 20))
        label.pack(pady=20)

        next_button = tk.Button(self, text="Next", command=self.show_signup_login_screen)
        next_button.pack()

    def center_window(self):
        # Calculate the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2

        # Set the window position
        self.geometry(f"400x200+{x}+{y}")

    def show_signup_login_screen(self):
        self.withdraw()  # Hide the welcome screen
        signup_login_screen = SignupLoginScreen(self)
        signup_login_screen.mainloop()

class SignupLoginScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("PRAGYAN")
        self.geometry("400x200")
        self.center_window()

        signup_button = tk.Button(self, text="Sign Up", command=self.show_signup_screen)
        signup_button.pack(pady=20)

        login_button = tk.Button(self, text="Login", command=self.show_login_screen)
        login_button.pack()

    def center_window(self):
        # Calculate the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2

        # Set the window position
        self.geometry(f"400x200+{x}+{y}")

    def show_signup_screen(self):
        self.withdraw()  # Hide the signup/login screen
        signup_screen = SignupScreen(self)
        signup_screen.mainloop()

    def show_login_screen(self):
        self.withdraw()  # Hide the signup/login screen
        login_screen = LoginScreen(self)
        login_screen.mainloop()

class SignupScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("PRAGYAN")
        self.geometry("400x300")
        self.center_window()

        username_label = tk.Label(self, text="Username:")
        username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        email_label = tk.Label(self, text="Email:")
        email_label.pack()

        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        password_label = tk.Label(self, text="Password:")
        password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        signup_button = tk.Button(self, text="Signup", command=self.signup)
        signup_button.pack(pady=20)

        self.message_label = tk.Label(self, text="", fg="red")
        self.message_label.pack()

    def center_window(self):
        # Calculate the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2

        # Set the window position
        self.geometry(f"400x300+{x}+{y}")

    def signup(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and email and password:
            if users_collection.find_one({'username': username}):
                self.message_label.config(text="Username already exists")
            else:
                users_collection.insert_one({'username': username, 'email': email, 'password': password})
                self.message_label.config(text="Signup successful")
                self.master.withdraw()  # Hide the signup window after successful signup
                open_terms_and_conditions()  # Open terms and conditions directly after signup
        else:
            self.message_label.config(text="Please fill in all fields")

class LoginScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("PRAGYAN")
        self.geometry("400x200")
        self.center_window()

        username_label = tk.Label(self, text="Username:")
        username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        password_label = tk.Label(self, text="Password:")
        password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=20)

        self.message_label = tk.Label(self, text="", fg="red")
        self.message_label.pack()

    def center_window(self):
        # Calculate the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2

        # Set the window position
        self.geometry(f"400x200+{x}+{y}")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and password:
            user = users_collection.find_one({'username': username, 'password': password})
            if user:
                self.message_label.config(text="Login successful")
                open_terms_and_conditions()  # Open terms and conditions directly after login
            else:
                self.message_label.config(text="Invalid username or password")
        else:
            self.message_label.config(text="Please fill in all fields")

class TermsAndConditionsApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("PRAGYAN")
        self.geometry("800x600")  # Adjust the geometry as needed
        self.center_window()

        self.display_terms()

    def display_terms(self):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Interview Proctoring Terms and Conditions</title>
        </head>
        <body>
            <div class="container">
                <h1>Interview Proctoring Terms and Conditions</h1>
                <div id="terms">
                    <p>Welcome to the interview proctoring service. Before you proceed, please read and agree to the following terms and conditions:</p>
                    <ol>
                        <li>This interview proctoring service utilizes facial recognition technology to verify the identity of the user during the interview.</li>
                        <li>The proctoring system may monitor and record your screen, webcam feed, and audio throughout the duration of the interview.</li>
                        <li>Your interview session may be reviewed by authorized personnel to ensure compliance with interview guidelines and prevent any misconduct.</li>
                        <li>You agree to use this service in a quiet, well-lit environment with a stable internet connection to ensure accurate proctoring.</li>
                        <li>Any attempt to tamper with or circumvent the proctoring system, including but not limited to using external devices or software, will result in disqualification from the interview process.</li>
                        <li>By proceeding, you consent to the collection, storage, and processing of your personal data for the purpose of interview proctoring, in accordance with our privacy policy.</li>
                        <li>The interview proctoring service and its administrators reserve the right to terminate your interview session at any time if there are suspicions of cheating, misconduct, or violation of these terms and conditions.</li>
                    </ol>
                    <p>Please note that by agreeing to these terms, you acknowledge and accept the conditions under which the interview proctoring service operates.</p>
                </div>
                <label for="agree">
                    <input type="checkbox" id="agree">
                    I have read and agree to the terms and conditions
                </label>

                <button id="submitBtn" disabled>PROCEED</button>
            </div>
        </body>
        </html>
        """

        # Create an HTMLLabel widget to display the HTML content
        html_label = HTMLLabel(self, html=html_content)
        html_label.pack(expand=True, fill=tk.BOTH)

        # Checkbox button
        self.agree_var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(self, text="I have read and agree to the terms and conditions", variable=self.agree_var, command=self.toggle_button_state)
        checkbox.pack()

        # Proceed button
        self.proceed_button = tk.Button(self, text="PROCEED", command=self.proceed, state="disabled")
        self.proceed_button.pack()

    def center_window(self):
        # Calculate the screen width and height 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2

        # Set the window position
        self.geometry(f"800x600+{x}+{y}")

    def toggle_button_state(self):
        if self.agree_var.get():
            self.proceed_button.config(state="normal")
        else:
            self.proceed_button.config(state="disabled")

    def proceed(self):
        # Hide the terms and conditions window
        self.master.withdraw()
        # Open the "Enter Your Personal Details" screen
        PersonalDetailsScreen()

def open_terms_and_conditions():
    root = tk.Toplevel()  # Use Toplevel instead of Tk
    app = TermsAndConditionsApp(root)
    root.mainloop()

class PersonalDetailsScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PRAGYAN")
        self.root.attributes('-fullscreen', True)  # Set fullscreen mode
        self.root.configure(background='white')  # Set background color to white

        label = tk.Label(self.root, text="Enter Your Personal Details", font=("Helvetica", 16), bg='white')
        label.pack(pady=20)

        # Create frames for organizing entries
        personal_info_frame = tk.Frame(self.root, bg='white')
        personal_info_frame.pack(pady=(0, 20), padx=20, anchor='center')

        academic_info_frame = tk.Frame(self.root, bg='white')
        academic_info_frame.pack(pady=(0, 20), padx=20, anchor='center')

        resume_photo_frame = tk.Frame(self.root, bg='white')
        resume_photo_frame.pack(pady=(0, 20), padx=20, anchor='center')

        # Personal Information Section
        name_label = tk.Label(personal_info_frame, text="Name:", bg='white')
        name_label.grid(row=0, column=0, padx=(20, 10), pady=5, sticky="e")
        self.name_entry = tk.Entry(personal_info_frame)
        self.name_entry.grid(row=0, column=1, padx=(10, 20), pady=5, sticky="w")

        email_label = tk.Label(personal_info_frame, text="Email:", bg='white')
        email_label.grid(row=1, column=0, padx=(20, 10), pady=5, sticky="e")
        self.email_entry = tk.Entry(personal_info_frame)
        self.email_entry.grid(row=1, column=1, padx=(10, 20), pady=5, sticky="w")

        phone_label = tk.Label(personal_info_frame, text="Phone:", bg='white')
        phone_label.grid(row=2, column=0, padx=(20, 10), pady=5, sticky="e")
        self.phone_entry = tk.Entry(personal_info_frame)
        self.phone_entry.grid(row=2, column=1, padx=(10, 20), pady=5, sticky="w")

        address_label = tk.Label(personal_info_frame, text="Address:", bg='white')
        address_label.grid(row=3, column=0, padx=(20, 10), pady=5, sticky="e")
        self.address_entry = tk.Entry(personal_info_frame)
        self.address_entry.grid(row=3, column=1, padx=(10, 20), pady=5, sticky="w")

        # Academic Information Section
        grade_10_label = tk.Label(academic_info_frame, text="10th Grade:", bg='white')
        grade_10_label.grid(row=0, column=0, padx=(20, 10), pady=5, sticky="e")
        self.grade_10_entry = tk.Entry(academic_info_frame)
        self.grade_10_entry.grid(row=0, column=1, padx=(10, 20), pady=5, sticky="w")

        grade_12_label = tk.Label(academic_info_frame, text="12th Grade:", bg='white')
        grade_12_label.grid(row=1, column=0, padx=(20, 10), pady=5, sticky="e")
        self.grade_12_entry = tk.Entry(academic_info_frame)
        self.grade_12_entry.grid(row=1, column=1, padx=(10, 20), pady=5, sticky="w")

        college_degree_label = tk.Label(academic_info_frame, text="College and Degree:", bg='white')
        college_degree_label.grid(row=2, column=0, padx=(20, 10), pady=5, sticky="e")
        self.college_degree_entry = tk.Entry(academic_info_frame)
        self.college_degree_entry.grid(row=2, column=1, padx=(10, 20), pady=5, sticky="w")

        skills_label = tk.Label(academic_info_frame, text="Skills:", bg='white')
        skills_label.grid(row=3, column=0, padx=(20, 10), pady=5, sticky="e")
        self.skills_entry = tk.Entry(academic_info_frame)
        self.skills_entry.grid(row=3, column=1, padx=(10, 20), pady=5, sticky="w")

        # Resume and Photo Section
        resume_button = tk.Button(resume_photo_frame, text="Upload Resume", command=self.upload_resume)
        resume_button.grid(row=0, column=0, padx=(20, 10), pady=5, sticky="e")
        self.resume_label = tk.Label(resume_photo_frame, text="Resume: No file selected", bg='white')
        self.resume_label.grid(row=0, column=1, padx=(10, 20), pady=5, sticky="w")

        profile_photo_button = tk.Button(resume_photo_frame, text="Upload Profile Photo", command=self.upload_profile_photo)
        profile_photo_button.grid(row=1, column=0, padx=(20, 10), pady=5, sticky="e")
        self.profile_photo_label = tk.Label(resume_photo_frame, text="Profile Photo: No file selected", bg='white')
        self.profile_photo_label.grid(row=1, column=1, padx=(10, 20), pady=5, sticky="w")

        # Professional Field of Study Section
        field_of_study_label = tk.Label(self.root, text="Professional Field of Study:", bg='white')
        field_of_study_label.pack(pady=(0, 20), padx=20, anchor='center')
        self.field_of_study_entry = tk.Entry(self.root)
        self.field_of_study_entry.pack(pady=(0, 20), padx=20, anchor='center')

        # Submit Button
        submit_button = tk.Button(self.root, text="Submit", command=self.submit_details)
        submit_button.pack(pady=(0, 20), padx=20, anchor='center')

        self.root.mainloop()

    def upload_resume(self):
        resume_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Documents", "*.doc *.docx")])
        if resume_file:
            self.resume_label.config(text=f"Resume: {resume_file}")
            account_details_collection.update_one({}, {"$set": {"resume_path": resume_file}}, upsert=True)

    def upload_profile_photo(self):
        profile_photo_file = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if profile_photo_file:
            self.profile_photo_label.config(text=f"Profile Photo: {profile_photo_file}")
            account_details_collection.update_one({}, {"$set": {"profile_photo_path": profile_photo_file}}, upsert=True)

    def submit_details(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        grade_10 = self.grade_10_entry.get()
        grade_12 = self.grade_12_entry.get()
        college_degree = self.college_degree_entry.get()
        skills = self.skills_entry.get()
        field_of_study = self.field_of_study_entry.get()

        details = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "grade_10": grade_10,
            "grade_12": grade_12,
            "college_degree": college_degree,
            "skills": skills,
            "field_of_study": field_of_study
        }
        account_details_collection.insert_one(details)

        messagebox.showinfo("Success", "Personal details submitted successfully!")

        self.show_proceed_button()

    def show_proceed_button(self):
        proceed_button = tk.Button(self.root, text="Proceed", command=self.proceed_to_test_screen)
        proceed_button.pack(pady=(10, 20), padx=20, anchor='center')

    def proceed_to_test_screen(self):
        self.root.withdraw()
        TestScreen()

class TestScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("PRAGYAN")
        self.attributes('-fullscreen', True)  # Set fullscreen mode
        self.configure(background='white')  # Set background color to white
        self.center_window()

        label = tk.Label(self, text="TEST SCREEN COMING UP", font=("Helvetica", 20), bg='cyan')
        label.pack(pady=20)

        # Call the function to start the camera after 2 seconds
        self.after(2000, self.start_camera_and_microphone)

    def center_window(self):
        # Calculate the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2

        # Set the window position
        self.geometry(f"400x200+{x}+{y}")

    def start_camera_and_microphone(self):
        try:
            # Start camera5.py
            subprocess.Popen(['python', 'camera 5.py'])
            # Start microphone.py
            subprocess.Popen(['python', 'microphone.py'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera and microphone: {str(e)}")
# Your remaining code for WelcomeScreen, SignupLoginScreen, etc.

if __name__ == "__main__":
    app = WelcomeScreen()
    app.mainloop()
