import csv
import random
import speech_recognition as sr
import pyaudio
import numpy as np
from difflib import SequenceMatcher
import tkinter as tk

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Function to read questions from a local CSV file
def read_questions_from_csv(file_path):
    questions = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            questions.extend(row)
    return questions

# Function to read answers from a local CSV file
def read_answers_from_csv(file_path):
    answers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            answers.extend(row)
    return answers

# Function to generate a set of 8 random questions without repetition
def generate_random_questions_and_answers(questions, answers, num_questions=8):
    combined = list(zip(questions, answers))
    random.shuffle(combined)
    random_questions, random_answers = zip(*combined)
    return random_questions[:num_questions], random_answers[:num_questions]

# Function to record initial frequency
def record_initial_frequency(duration):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Calculate frequency using FFT
    fft_data = np.fft.fft(audio_array)
    freqs = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    idx = np.argmax(np.abs(fft_data))
    frequency = freqs[idx]

    return abs(frequency)

# Function to record and analyze frequency while giving answers
def record_and_analyze_frequency(duration, answer_frequency):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Calculate frequency using FFT
    fft_data = np.fft.fft(audio_array)
    freqs = np.fft.fftfreq(len(fft_data), 1.0/RATE)
    idx = np.argmax(np.abs(fft_data))
    frequency = freqs[idx]

    # Check if the frequency is within ±200 Hz from the answer frequency
    if abs(frequency - answer_frequency) > 200:
        return False
    else:
        return True

# Function to detect if two people are talking
def detect_multiple_voices(audio_data):
    fft_data = np.fft.fft(audio_data)
    amplitudes = np.abs(fft_data)

    # Calculate the mean amplitude
    mean_amplitude = np.mean(amplitudes)

    # Calculate the standard deviation of amplitudes
    std_amplitude = np.std(amplitudes)

    # Find peaks
    peaks = np.where(amplitudes > (mean_amplitude + 3 * std_amplitude))[0]

    # Check if the number of peaks exceeds a threshold
    if len(peaks) > 1:
        return True
    else:
        return False

# Function to recognize speech and compare with answers
def recognize_and_compare_answer(answer):
    with sr.Microphone(1) as source:
        r = sr.Recognizer()
        print("Listening... ")
        audio = r.listen(source)

    try:
        user_answer = r.recognize_google(audio)
        print(f"You said: {user_answer}")
        similarity_ratio = SequenceMatcher(None, user_answer.lower(), answer.lower()).ratio()
        return user_answer.lower(), similarity_ratio
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "", 0
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return "", 0

def close_window():
    root.destroy()

if __name__ == "__main__":
    duration = 5  # Recording duration in seconds

    # Interview loop with cheating detection
    # Initialize the speech recognition object
    r = sr.Recognizer()

    # Path to the CSV file containing the series of questions
    question_csv_file_path = "Questions.csv"  # Replace with your file path

    # Path to the CSV file containing the answers
    answer_csv_file_path = "Answers hai yeh.csv"  # Replace with your file path

    # Read questions and answers from the CSV files
    series_of_questions = read_questions_from_csv(question_csv_file_path)
    series_of_answers = read_answers_from_csv(answer_csv_file_path)

    # Initialize an index to keep track of the current question
    current_question_index = 0

    # Record initial frequency
    initial_frequency = record_initial_frequency(duration)
    print("Initial recorded frequency:", initial_frequency)

    total_score = 0
    total_questions = 0

    # Main loop to generate and print random questions
    while True:
        input("Press Enter to generate a set of 8 random questions...\n")

        # Check if all questions have been asked, if so, shuffle again
        if current_question_index >= len(series_of_questions):
            random.shuffle(series_of_questions)
            random.shuffle(series_of_answers)
            current_question_index = 0

        # Generate and print the set of 8 random questions
        random_questions, random_answers = generate_random_questions_and_answers(series_of_questions[current_question_index:], series_of_answers[current_question_index:])

        for i, (question, answer) in enumerate(zip(random_questions, random_answers)):
            print(f"Question {i + 1}: Can you explain in detail {question.lower()}?")

            # Record and analyze frequency after the answer
            while True:
                if not record_and_analyze_frequency(duration, initial_frequency):
                    print("Cheating detected! Suspicious frequency detected.\n")
                    break  # End the interview loop if cheating is detected

                # Check for multiple voices in the room
                with sr.Microphone(1) as source:
                    user_answer, similarity_ratio = recognize_and_compare_answer(answer)

                if user_answer:
                    if similarity_ratio >= 0.7:  # Adjust the threshold as needed
                        print("Correct answer! ", similarity_ratio)
                        total_score += similarity_ratio
                    else:
                        print("Incorrect answer. ", similarity_ratio)
                    total_questions += 1
                    break

        # Update the current question index
        current_question_index += len(random_questions)

        # Check if all questions are asked
        if current_question_index >= len(series_of_questions):
            average_score = total_score / total_questions if total_questions != 0 else 0
            print("Average Score:", average_score)

            # Create a GUI window
            root = tk.Tk()
            root.title("Interview Score")
            root.geometry("200x100")

            # Display average score
            score_label = tk.Label(root, text=f"Average Score: {average_score:.2f}")
            score_label.pack()

            # Button to close the window
            close_button = tk.Button(root, text="Close", command=close_window)
            close_button.pack()

            root.mainloop()
            break