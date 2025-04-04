import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import random

# Function to generate the CSV with random data
def generate_csv():
    # Sample student names and subjects
    names = ["Mani", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ian", "Jack"]
    subjects = ["Maths", "Science", "English", "History", "Geography", "Physics", "Chemistry", "Biology"]

    # Create and write to the CSV file
    with open("scores.csv", mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Name", "Subject", "Marks"])

        # Generate 50 random student records
        for i in names:
            for j in subjects:
                name = i
                subject = j
                marks = random.randint(60, 100)
                writer.writerow([name, subject, marks])

    st.success("Random student data has been generated and saved in 'scores.csv'.")

# Function to assign grades based on marks
def assign_grade(marks):
    if 100 >= marks >= 90:
        return "A"
    elif 89 >= marks >= 80:
        return "B"
    elif 79 >= marks >= 70:
        return "C"
    elif 69 >= marks >= 60:
        return "D"
    else:
        return "F"

# Streamlit App Interface
st.title('Student Grade and Insights Generator')

# Button to generate random student data
if st.button('Generate Random Student Data'):
    generate_csv()

# Upload student CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Assign grades based on marks
    df["Grade"] = df["Marks"].apply(assign_grade)

    # Total Marks per Student
    total = df.groupby("Name")["Marks"].sum().sort_values(ascending=False).reset_index()

    # Display total marks per student
    st.subheader("Total Marks per Student")
    st.write(total)

    # Bar plot for total marks per student
    st.subheader("Bar Plot: Total Marks per Student")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=total["Name"], y=total["Marks"], hue=total["Name"])
    plt.title("Total Marks per Student")
    plt.xticks(rotation=90)
    plt.xlabel("Name")
    plt.ylabel("Total Marks")
    st.pyplot()

    # Average Marks per Student
    avg_marks = df.groupby("Name")["Marks"].mean().sort_values(ascending=False).reset_index()

    # Display average marks per student
    st.subheader("Average Marks per Student")
    st.write(avg_marks)

    # Bar plot for average marks per student
    st.subheader("Bar Plot: Average Marks per Student")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_marks["Name"], y=avg_marks["Marks"], hue=avg_marks["Name"])
    plt.title("Average Marks per Student")
    plt.xticks(rotation=90)
    plt.xlabel("Name")
    plt.ylabel("Average Marks")
    st.pyplot()

    # Grade Distribution Pie Chart
    st.subheader("Grade Distribution")
    grade_dist = df['Grade'].value_counts()
    grade_dist.plot(kind="pie", autopct='%1.1f%%', startangle=90, title="Grade Distribution")
    plt.ylabel("")  # Hide the y-label
    st.pyplot()

    # Rank based on total marks
    total_marks = df.groupby("Name")["Marks"].sum().reset_index()
    total_marks['Rank'] = total_marks['Marks'].rank(ascending=False, method="min")
    total_marks_sorted = total_marks.sort_values("Marks", ascending=False)

    # Display total marks and rank information
    st.subheader("Rank Based on Total Marks")
    st.write(total_marks_sorted)

    # Bar plot for total marks and ranks
    st.subheader("Bar Plot: Total Marks per Student (Ranked)")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Marks", y="Name", data=total_marks_sorted, palette="viridis")
    plt.title("Total Marks per Student (Ranked)")
    plt.xlabel("Total Marks")
    plt.ylabel("Student Name")
    st.pyplot()

