'''Write a code to develop GUI application that
allows teachers to input student marks for various
 subjects, analyzes performance, and generates
 reports'''
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt


class PerformanceAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Analyzer")
        self.students = []

        # Input fields
        tk.Label(root, text="Student Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Marks:").grid(row=1, column=0)
        self.marks_entry = tk.Entry(root)
        self.marks_entry.grid(row=1, column=1)

        tk.Button(root, text="Add Student", command=self.add_student).grid(row=2, columnspan=2)
        tk.Button(root, text="Generate Report", command=self.generate_report).grid(row=3, columnspan=2)

    def add_student(self):
        name = self.name_entry.get()
        marks = self.marks_entry.get()
        if name and marks.isnumeric():
            self.students.append((name, int(marks)))
            self.name_entry.delete(0, tk.END)
            self.marks_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added {name} with {marks} marks!")
        else:
            messagebox.showerror("Error", "Invalid input!")

    def generate_report(self):
        if not self.students:
            messagebox.showwarning("Warning", "No students to report!")
            return

        df = pd.DataFrame(self.students, columns=["Name", "Marks"])
        average = df['Marks'].mean()
        df['Grade'] = pd.cut(df['Marks'], bins=[0, 50, 60, 70, 80, 90, 100],
                             labels=['F', 'D', 'C', 'B', 'A', 'A+'], right=False)

        # Generate report
        report = f"Average Marks: {average:.2f}\n\n{df}\n"
        messagebox.showinfo("Report", report)

        # Plotting
        df.plot(kind='bar', x='Name', y='Marks', legend=False)
        plt.title('Student Marks')
        plt.ylabel('Marks')
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = PerformanceAnalyzer(root)
    root.mainloop()