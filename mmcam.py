import tkinter as tk
import csv
import random
import speech_recognition as sr
import pyaudio
import numpy as np
from difflib import SequenceMatcher
import threading
import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Holistic model
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.3, min_tracking_confidence=0.3)

# Initialize constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DURATION = 5

# Initialize global variables
total_score = 0
total_questions = 0
initial_frequency = 0

# Function to read questions from a CSV file
def read_questions_from_csv(file_path):
    questions = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            questions.extend(row)
    return questions

# Function to read answers from a CSV file
def read_answers_from_csv(file_path):
    answers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            answers.extend(row)
    return answers

# Function to generate random questions and answers
def generate_random_questions_and_answers(questions, answers, num_questions=8):
    combined = list(zip(questions, answers))
    random.shuffle(combined)
    random_questions, random_answers = zip(*combined)
    return random_questions[:num_questions], random_answers[:num_questions]

# Function to record initial frequency
def record_initial_frequency():
    global initial_frequency
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    fft_data = np.fft.fft(audio_array)
    freqs = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    idx = np.argmax(np.abs(fft_data))
    initial_frequency = abs(freqs[idx])
    return initial_frequency

# Function to record and analyze frequency while giving answers
def record_and_analyze_frequency(answer_frequency):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    fft_data = np.fft.fft(audio_array)
    freqs = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    idx = np.argmax(np.abs(fft_data))
    frequency = abs(freqs[idx])

    if abs(frequency - answer_frequency) > 200:
        return False
    else:
        return True

# Function to recognize speech and compare with answers
def recognize_and_compare_answer(answer):
    with sr.Microphone(1) as source:
        r = sr.Recognizer()
        label.config(text="Listening...")
        audio = r.listen(source)

    try:
        user_answer = r.recognize_google(audio)
        label.config(text=f"You said: {user_answer}")
        similarity_ratio = SequenceMatcher(None, user_answer.lower(), answer.lower()).ratio()
        return user_answer.lower(), similarity_ratio
    except sr.UnknownValueError:
        label.config(text="Could not understand audio")
        return "", 0
    except sr.RequestError:
        label.config(text="Could not request results from Google Speech Recognition service")
        return "", 0

# Function to start the interview process
def start_interview():
    global total_score, total_questions
    total_score = 0
    total_questions = 0

    # Read questions and answers from CSV files
    question_csv_file_path = r"questonaire.csv"  # Replace with your file path
    answer_csv_file_path = r"answers445.csv" # Replace with your file path
    series_of_questions = read_questions_from_csv(question_csv_file_path)
    series_of_answers = read_answers_from_csv(answer_csv_file_path)

    # Create scrolled text widget to display questions and answers
    question_answer_text.config(state=tk.NORMAL)
    question_answer_text.delete(1.0, tk.END)
    question_answer_text.insert(tk.END, "Checking environment audio...\n")
    question_answer_text.config(state=tk.DISABLED)

    root.update_idletasks()

    # Record initial frequency
    initial_frequency = record_initial_frequency()
    # Update label with initial frequency
    initial_frequency_label.config(text=f"Initial Frequency: {initial_frequency:.2f} Hz")

    # Hide start button and show retry button
    start_button.pack_forget()
    retry_button.pack()

    # Create scrolled text widget to display questions and answers
    question_answer_text.config(state=tk.NORMAL)
    question_answer_text.delete(1.0, tk.END)
    question_answer_text.insert(tk.END, "Interview Started...\n")
    question_answer_text.config(state=tk.DISABLED)

    root.update_idletasks()

    # Thread for asking questions
    def ask_questions_thread():
        global total_score, total_questions
        for i in range(len(series_of_questions)):
            question_answer_text.config(state=tk.NORMAL)
            question_answer_text.insert(tk.END, f"\n\nQuestion: {series_of_questions[i]}\n")
            root.update_idletasks()

            # Record and analyze frequency after the answer
            while True:
                if not record_and_analyze_frequency(initial_frequency):
                    question_answer_text.insert(tk.END, "Cheating Detected! Suspicious frequency detected.\n")
                    return

                user_answer, similarity_ratio = recognize_and_compare_answer(series_of_answers[i])

                if user_answer:
                    question_answer_text.insert(tk.END, f"Your Answer:  {user_answer}\n")
                    similarity_ratio_formatted = "{:.2f}".format(similarity_ratio)
                    if similarity_ratio >= 0.7:  # Adjust the threshold as needed
                        question_answer_text.insert(tk.END, f"Evaluation: Correct answer! Similarity ratio: {similarity_ratio_formatted}\n")
                        total_score += similarity_ratio
                    else:
                        question_answer_text.insert(tk.END, f"Evaluation: Incorrect answer. Similarity ratio: {similarity_ratio_formatted}\n")
                    total_questions += 1
                    break

            question_answer_text.config(state=tk.DISABLED)
            root.update_idletasks()

    # Start a new thread for asking questions
    threading.Thread(target=ask_questions_thread).start()

# Function to check if the user is looking at the camera
def is_looking_at_camera(face_landmarks):
    left_eye = [face_landmarks.landmark[n] for n in [33, 133, 157, 158, 159, 160, 161]]
    right_eye = [face_landmarks.landmark[n] for n in [263, 362, 386, 387, 388, 466, 467]]

    left_eye_center = (sum([landmark.x for landmark in left_eye]) / len(left_eye),
                       sum([landmark.y for landmark in left_eye]) / len(left_eye))
    right_eye_center = (sum([landmark.x for landmark in right_eye]) / len(right_eye),
                        sum([landmark.y for landmark in right_eye]) / len(right_eye))

    eye_vector = (right_eye_center[0] - left_eye_center[0], right_eye_center[1] - left_eye_center[1])
    eye_direction = (math.atan2(eye_vector[1], eye_vector[0]) * 180 / math.pi) % 360

    if 180 >= eye_direction >= 0:
        return True  # Looking at the camera
    else:
        return False  # Not looking at the camera

# Function to check if there is any significant eye movement detected
def check_eye_movement(curr_landmarks, prev_landmarks):
    if prev_landmarks is None:
        return False

    for curr_landmark, prev_landmark in zip(curr_landmarks.landmark, prev_landmarks.landmark):
        if curr_landmark.visibility > 0.5 and prev_landmark.visibility > 0.5:
            if abs(curr_landmark.x - prev_landmark.x) > 0.01 or abs(curr_landmark.y - prev_landmark.y) > 0.01:
                return True

    return False


# Function to check if there is any significant face movement detected
def check_movement(curr_landmarks, prev_landmarks):
    if prev_landmarks is None:
        return False

    for idx, landmark in enumerate(curr_landmarks.landmark):
        if landmark.visibility > 0.5:
            if abs(landmark.x - prev_landmarks.landmark[idx].x) > 0.05 or \
               abs(landmark.y - prev_landmarks.landmark[idx].y) > 0.05:
                return True

    return False

# Function to detect other persons in the room
def detect_other_persons(results):
    num_faces = 0
    if hasattr(results, 'multi_face_landmarks') and results.multi_face_landmarks is not None:
        num_faces = len(results.multi_face_landmarks)
    return num_faces > 1

# Variable to track the main user's face position
main_user_pos = None

# Initialize variables for movement detection
prev_face_landmarks = None

# Function to start webcam feed and perform face detection
# Function to start webcam feed and perform face detection
def start_webcam_feed(prev_face_landmarks):
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Get the dimensions of the video feed
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the dimensions and position of the imaginary box
    box_width = 250
    box_height = 250
    box_x = (frame_width - box_width) // 2
    box_y = (frame_height - box_height) // 2

    # Define the coordinates of the imaginary box
    box_top_left = (box_x, box_y)
    box_bottom_right = (box_x + box_width, box_y + box_height)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face landmarks, hand landmarks, and pose landmarks
        results = holistic.process(frame_rgb)

        # Draw face landmarks, hand landmarks, and pose landmarks on the frame
        if results.face_landmarks:
            mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)

            # Check if the user is looking at the camera
            if not is_looking_at_camera(results.face_landmarks):
                cv2.putText(frame, "Cheating!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Check for eye movement
            if check_eye_movement(results.face_landmarks, prev_face_landmarks):
                cv2.putText(frame, "Cheating!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Check for face movement
            if check_movement(results.face_landmarks, prev_face_landmarks):
                cv2.putText(frame, "Cheating!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Check if the face is within the imaginary box
        if results.face_landmarks:
            for landmark in results.face_landmarks.landmark:
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if box_x < x < box_x + box_width and box_y < y < box_y + box_height:
                    main_user_pos = (x, y)
                    break
            else:
                print("Face out of the box. Movement detected.")
                main_user_pos = None

        # Detect other persons in the room
        if detect_other_persons(results):
            print("Another person detected in the room!")

        # Update previous landmarks
        prev_face_landmarks = results.face_landmarks

        # Draw the imaginary box on the frame
        cv2.rectangle(frame, box_top_left, box_bottom_right, (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Start threads for interview and webcam feed
prev_face_landmarks = None
threading.Thread(target=start_webcam_feed, args=(prev_face_landmarks,)).start()

# Create GUI
root = tk.Tk()
root.title("Interview Application")
root.attributes("-fullscreen", True)  # Set full screen
root.overrideredirect(True)  # Hide the window title bar
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Adjust geometry to fit the screen

# Label to display status
label = tk.Label(root, text="", font=("Arial", 12))
label.pack()

# Label to display initial frequency
initial_frequency_label = tk.Label(root, text="", font=("Arial", 12))
initial_frequency_label.place(x=root.winfo_screenwidth() - 200, y=10)

# Frame to hold text widget
frame = tk.Frame(root)
frame.pack(pady=20)

# Scrolled text widget to display questions and answers
question_answer_text = tk.Text(frame, width=70, height=15, wrap=tk.WORD, font=("Arial", 12))
question_answer_text.pack(side=tk.LEFT)

# Scrollbar for text widget
scrollbar = tk.Scrollbar(frame, command=question_answer_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
question_answer_text.config(yscrollcommand=scrollbar.set)

# Button to start the interview
start_button = tk.Button(root, text="Start Your Interview", command=start_interview, bg="#1f7da3", fg="white", font=("Arial", 14, "bold"), padx=10, pady=5)

# Button for retry
retry_button = tk.Button(root, text="Retry", command=start_interview, bg="#1f7da3", fg="white", font=("Arial", 14, "bold"), padx=10, pady=5)

start_button.pack()

# Start threads for interview and webcam feed
threading.Thread(target=start_webcam_feed).start()

root.mainloop()
