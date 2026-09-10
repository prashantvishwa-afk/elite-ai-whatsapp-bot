import os
import csv
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env file")
    exit()

client = OpenAI(api_key=api_key)

# Clinic information
with open("clinic_info.txt", "r", encoding="utf-8") as file:
    clinic_info = file.read()


# Create appointments.csv if it doesn't exist
csv_file = "appointments.csv"

if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time", "Phone"])


# Save appointment
def save_appointment(name, date, time, phone):
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, date, time, phone])


system_prompt = f"""
You are the AI assistant for Elite Spine & Joint.

Doctor: Dr. Ankit Desai

Your job is to help customers with:
- Clinic information
- Doctor information
- Services
- Working hours
- Location
- Appointment enquiries

Use only the clinic information provided below.
Do not invent information.

IMPORTANT:
- Do not diagnose medical conditions.
- Do not provide treatment instructions.
- Do not claim an appointment is confirmed.
- For appointments, the clinic staff must confirm the appointment.
- Be polite, short and helpful.
- You can understand both English and Hindi/Hinglish.

Clinic information:
{clinic_info}
"""


print("=" * 55)
print("Elite Spine & Joint - AI Assistant")
print("Appointment enquiry system: ON")
print("Type 'exit' to close the chatbot.")
print("=" * 55)


# Appointment conversation state
appointment_mode = False
appointment_step = 0

appointment_name = ""
appointment_date = ""
appointment_time = ""
appointment_phone = ""


while True:

    user_message = input("\nYou: ").strip()

    if user_message.lower() == "exit":
        print("Bot: Goodbye!")
        break


    # Start appointment flow
    if not appointment_mode and any(
        word in user_message.lower()
        for word in [
            "appointment",
            "appointment lena",
            "book appointment",
            "booking",
            "appoint"
        ]
    ):
        appointment_mode = True
        appointment_step = 1

        print("\nAI: Sure! Appointment enquiry ke liye aapka naam kya hai?")
        continue


    # Appointment flow
    if appointment_mode:

        if appointment_step == 1:
            appointment_name = user_message
            appointment_step = 2

            print("\nAI: Thank you! Aap kis date ko appointment lena chahenge?")
            continue


        if appointment_step == 2:
            appointment_date = user_message
            appointment_step = 3

            print("\nAI: Aapka preferred time kya hai?")
            continue


        if appointment_step == 3:
            appointment_time = user_message
            appointment_step = 4

            print("\nAI: Please apna phone number enter karein, jisse clinic staff aapse contact kar sake.")
            continue


        if appointment_step == 4:
            appointment_phone = user_message

            # Save appointment
            save_appointment(
                appointment_name,
                appointment_date,
                appointment_time,
                appointment_phone
            )

            print("\nAI: Thank you! Aapki appointment enquiry save ho gayi hai.")
            print(
                f"AI: Name: {appointment_name}, "
                f"Date: {appointment_date}, "
                f"Time: {appointment_time}"
            )
            print("AI: Clinic staff aapse confirmation ke liye contact karega.")

            # Reset appointment flow
            appointment_mode = False
            appointment_step = 0

            appointment_name = ""
            appointment_date = ""
            appointment_time = ""
            appointment_phone = ""

            continue


    # Normal AI conversation
    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=system_prompt,
            input=user_message
        )

        print("\nAI:", response.output_text)

    except Exception as error:
        print("\nError:", error)