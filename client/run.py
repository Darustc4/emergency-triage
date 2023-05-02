import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from enum import Enum
from dataclasses import dataclass

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

header_label_color = "#327ab3"
header_font_color = "#DCE4EE"
subheader_background_color = "#a9b3bc"
light_widget_color = "#b8bfc7"
vlight_widget_color = "#c3c9cf"
vvlight_widget_color = "#ced3d8"
dark_widget_color = "#5a6672"
vdark_widget_color = "#4f5964"
subheader_font_color = "#22272b"
container_background_color = "#f0f0f0"

button_color = "#3b8ed0"
button_highlight_color = "#225177"

class EmergencyType(Enum):
    Generic = 0
    Mental = 1
    Palpitations = 2
    Asthma = 3
    Allergy = 4
    DiarrVom = 5

@dataclass
class Patient:
    id: int
    ssn: str
    age: int
    is_male: bool
    longitude: float = None
    latitude: float = None
    emergency_level: int = 0
    emergency_category: EmergencyType = EmergencyType.Generic

    def get_sex(self):
        return "Male" if self.is_male else "Female"

class Triage(ctk.CTk):
    def __init__(self):

        # These symptoms are only for mental, palpitations, asthma, allergy and diarrhea and vomit emergencies. The complete list of symptoms is in the Manchester Triage handbook.
        self.specific_symptoms = {"self-harm high risk", "other-harm high risk", "violence", "self-harm moderate risk", "other-harm moderate risk", "significant distress", "significant psychiatric history", "agressive demeanor", "crying easily", "recent self-harm risk", "recent other-harm risk", "moderate distress", "disruptive demeanor", "crying", "abnormal pulse", "intoxication history", "chest pain", "palpitations", "significant cardiac history", "relative cardiac history", "difficulty speaking", "abnormal pulse", "significant respiratory history", "chest pain", "sunken ribs", "ineffective medication", "nostril flare", "dry cough", "wet cough", "difficulty speaking", "swollen face", "abnormal pulse", "skin rash", "swollen hands", "localized swelling", "recent swelling", "severe thirst", "slenderness", "blood vomit", "rectal bleeding leakage", "blood vomit history", "red or black deposition", "dehidration signs", "frequent deposition", "vomiting", "anorexia", "nausea", "thrist", "abdominal pain"}

        self.patients = []
        self.next_patient_id = 0

        self.create_tk()

    def create_tk(self):
        super().__init__()

        self.title("Emergency Triage")
        self.geometry("600x800")

        self.create_frames()
        self.create_widgets()

    def create_frames(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Add Patient Frame
        self.grid_rowconfigure(1, weight=1) # Patients Frame
        self.grid_rowconfigure(2, weight=0) # Edit Patient Frame

        # Add Patient Frame
        self.tk_add_patient_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=vvlight_widget_color)
        self.tk_add_patient_frame.grid(row=0, column=0, sticky="nsew")

        self.tk_add_patient_frame.grid_columnconfigure(0, weight=1)
        self.tk_add_patient_frame.grid_columnconfigure(1, weight=1)
        self.tk_add_patient_frame.grid_columnconfigure(2, weight=1)
        self.tk_add_patient_frame.grid_columnconfigure(3, weight=1)
        self.tk_add_patient_frame.grid_columnconfigure(4, weight=1)
        self.tk_add_patient_frame.grid_columnconfigure(5, weight=0)
        self.tk_add_patient_frame.grid_rowconfigure(0, weight=0)
        self.tk_add_patient_frame.grid_rowconfigure(1, weight=0)
        self.tk_add_patient_frame.grid_rowconfigure(2, weight=0)

        # Patients Frame
        self.tk_patients_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=vvlight_widget_color)
        self.tk_patients_frame.grid(row=1, column=0, sticky="nsew")

        self.tk_patients_frame.grid_columnconfigure(0, weight=1)
        self.tk_patients_frame.grid_columnconfigure(1, weight=0)
        self.tk_patients_frame.grid_rowconfigure(0, weight=0)
        self.tk_patients_frame.grid_rowconfigure(1, weight=1)

        # Edit Patient Frame
        self.tk_edit_patient_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=vvlight_widget_color)
        self.tk_edit_patient_frame.grid(row=2, column=0, sticky="nsew")

        self.tk_edit_patient_frame.grid_columnconfigure(0, weight=0)
        self.tk_edit_patient_frame.grid_columnconfigure(1, weight=1)
        self.tk_edit_patient_frame.grid_columnconfigure(2, weight=0)
        self.tk_edit_patient_frame.grid_rowconfigure(0, weight=0)
        self.tk_edit_patient_frame.grid_rowconfigure(1, weight=0)
        self.tk_edit_patient_frame.grid_rowconfigure(2, weight=0)
        self.tk_edit_patient_frame.grid_rowconfigure(3, weight=0)
        self.tk_edit_patient_frame.grid_rowconfigure(4, weight=0)
        self.tk_edit_patient_frame.grid_rowconfigure(5, weight=0)
        self.tk_edit_patient_frame.grid_rowconfigure(6, weight=1)

    def create_widgets(self):
        # Add Patient Frame
        self.tk_add_patient_label = ctk.CTkLabel(self.tk_add_patient_frame, text="Add Patient", bg_color=header_label_color, text_color=header_font_color)
        self.tk_add_patient_label.grid(row=0, column=0, sticky="nsew", columnspan=6)

        self.tk_add_patient_ssn_label = ctk.CTkLabel(self.tk_add_patient_frame, text="SSN", bg_color=vlight_widget_color, text_color=subheader_font_color)
        self.tk_add_patient_ssn_label.grid(row=1, column=0, sticky="nsew")
        self.tk_add_patient_age_label = ctk.CTkLabel(self.tk_add_patient_frame, text="Age", bg_color=vlight_widget_color, text_color=subheader_font_color)
        self.tk_add_patient_age_label.grid(row=1, column=1, sticky="nsew")
        self.tk_add_patient_sex_label = ctk.CTkLabel(self.tk_add_patient_frame, text="Sex", bg_color=vlight_widget_color, text_color=subheader_font_color)
        self.tk_add_patient_sex_label.grid(row=1, column=2, sticky="nsew")
        self.tk_add_patient_longitude_label = ctk.CTkLabel(self.tk_add_patient_frame, text="Longitude", bg_color=vlight_widget_color, text_color=subheader_font_color)
        self.tk_add_patient_longitude_label.grid(row=1, column=3, sticky="nsew")
        self.tk_add_patient_latitude_label = ctk.CTkLabel(self.tk_add_patient_frame, text="Latitude", bg_color=vlight_widget_color, text_color=subheader_font_color)
        self.tk_add_patient_latitude_label.grid(row=1, column=4, sticky="nsew")

        self.tk_add_patient_ssn_entry = ctk.CTkEntry(self.tk_add_patient_frame)
        self.tk_add_patient_ssn_entry.grid(row=2, column=0, sticky="nsew", padx=1)
        self.tk_add_patient_age_entry = ctk.CTkEntry(self.tk_add_patient_frame)
        self.tk_add_patient_age_entry.grid(row=2, column=1, sticky="nsew", padx=1)
        self.tk_add_patient_sex_var = tk.StringVar(value="Male")
        self.tk_add_patient_sex_entry = ctk.CTkOptionMenu(self.tk_add_patient_frame, values=["Male", "Female"], variable=self.tk_add_patient_sex_var, fg_color=light_widget_color, button_color=dark_widget_color, text_color=subheader_font_color)
        self.tk_add_patient_sex_entry.grid(row=2, column=2, sticky="nsew", padx=1)
        self.tk_add_patient_longitude_entry = ctk.CTkEntry(self.tk_add_patient_frame)
        self.tk_add_patient_longitude_entry.grid(row=2, column=3, sticky="nsew", padx=1)
        self.tk_add_patient_latitude_entry = ctk.CTkEntry(self.tk_add_patient_frame)
        self.tk_add_patient_latitude_entry.grid(row=2, column=4, sticky="nsew", padx=1)

        self.tk_add_patient_button = ctk.CTkButton(self.tk_add_patient_frame, text="Add Patient", command=self.add_patient, border_width=2, border_color=dark_widget_color, fg_color=button_color)
        self.tk_add_patient_button.grid(row=1, column=5, sticky="nsew", rowspan=2, padx=5, pady=5)

        self.tk_add_patient_separator = ttk.Separator(self.tk_add_patient_frame, orient=tk.HORIZONTAL)
        self.tk_add_patient_separator.grid(row=3, column=0, sticky="nsew", columnspan=6, padx=5, pady=5)

        # Patients Frame

        self.tk_patients_label = ctk.CTkLabel(self.tk_patients_frame, text="Patients", bg_color=header_label_color, text_color=header_font_color)
        self.tk_patients_label.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.tk_patients_canvas = tk.Canvas(self.tk_patients_frame, bg=vvlight_widget_color)
        self.tk_patients_canvas.grid(row=1, column=0, sticky="nsew")

        self.tk_patients_scrollbar = ctk.CTkScrollbar(self.tk_patients_frame, orientation="vertical", command=self.tk_patients_canvas.yview)
        self.tk_patients_scrollbar.grid(row=1, column=1, sticky="ns")
        self.tk_patients_canvas.configure(yscrollcommand=self.tk_patients_scrollbar.set)

        self.tk_patients_list_frame = ctk.CTkFrame(self.tk_patients_canvas, fg_color=light_widget_color)
        self.tk_patients_list_frame.grid(row=0, column=0, sticky="nsew")
        self.tk_patients_list_frame.grid_columnconfigure(0, weight=1)
        self.tk_patients_list_frame.grid_columnconfigure(1, weight=1)
        self.tk_patients_list_frame.grid_columnconfigure(2, weight=1)
        self.tk_patients_list_frame.grid_columnconfigure(3, weight=1)
        self.tk_patients_list_frame.grid_columnconfigure(4, weight=1)
        self.tk_patients_list_frame.grid_columnconfigure(5, weight=1)
        self.tk_patients_list_frame.grid_columnconfigure(6, weight=1)
        self.tk_patients_list_frame.grid_columnconfigure(7, weight=1)
        self.tk_patients_list_frame.grid_rowconfigure(0, weight=0)

        self.tk_patients_id_label = ctk.CTkLabel(self.tk_patients_list_frame, text="ID", bg_color=vdark_widget_color, text_color=header_font_color)
        self.tk_patients_ssn_label = ctk.CTkLabel(self.tk_patients_list_frame, text="SSN", bg_color=dark_widget_color, text_color=header_font_color)
        self.tk_patients_age_label = ctk.CTkLabel(self.tk_patients_list_frame, text="Age", bg_color=vdark_widget_color, text_color=header_font_color)
        self.tk_patients_sex_label = ctk.CTkLabel(self.tk_patients_list_frame, text="Sex", bg_color=dark_widget_color, text_color=header_font_color)
        self.tk_patients_longitude_label = ctk.CTkLabel(self.tk_patients_list_frame, text="Longitude", bg_color=vdark_widget_color, text_color=header_font_color)
        self.tk_patients_latitude_label = ctk.CTkLabel(self.tk_patients_list_frame, text="Latitude", bg_color=dark_widget_color, text_color=header_font_color)
        self.tk_patients_emergency_level_label = ctk.CTkLabel(self.tk_patients_list_frame, text="Emergency Lvl.", bg_color=vdark_widget_color, text_color=header_font_color)
        self.tk_patients_emergency_class_label = ctk.CTkLabel(self.tk_patients_list_frame, text="Classification", bg_color=dark_widget_color, text_color=header_font_color)
        self.set_patients_header_grid()

        self.tk_patients_canvas_frame =  self.tk_patients_canvas.create_window((0,0), window=self.tk_patients_list_frame, anchor="nw")
        self.tk_patients_list_frame.bind("<Configure>", self.on_patients_list_frame_configure)
        self.tk_patients_canvas.bind("<Configure>", self.on_patients_canvas_configure)

        self.tk_patients_separator = ttk.Separator(self.tk_patients_frame, orient=tk.HORIZONTAL)
        self.tk_patients_separator.grid(row=2, column=0, sticky="nsew", columnspan=2, padx=5, pady=5)

        # Edit Patient Frame

        self.tk_edit_patient_label = ctk.CTkLabel(self.tk_edit_patient_frame, text="Edit Patient", bg_color=header_label_color, text_color=header_font_color)
        self.tk_edit_patient_label.grid(row=0, column=0, sticky="nsew", columnspan=3)

        self.tk_life_threat_label = ctk.CTkLabel(self.tk_edit_patient_frame, text="Life Threat", bg_color=vdark_widget_color, text_color=header_font_color)
        self.tk_life_threat_label.grid(row=1, column=0, sticky="nsew")
        self.tk_consciousness_label = ctk.CTkLabel(self.tk_edit_patient_frame, text="Consciousness", bg_color=dark_widget_color, text_color=header_font_color)
        self.tk_consciousness_label.grid(row=2, column=0, sticky="nsew")
        self.tk_haemorrhage_label = ctk.CTkLabel(self.tk_edit_patient_frame, text="Haemorrhage", bg_color=vdark_widget_color, text_color=header_font_color)
        self.tk_haemorrhage_label.grid(row=3, column=0, sticky="nsew")
        self.tk_temperature_label = ctk.CTkLabel(self.tk_edit_patient_frame, text="Temperature", bg_color=dark_widget_color, text_color=header_font_color)
        self.tk_temperature_label.grid(row=4, column=0, sticky="nsew")
        self.tk_pain_level_label = ctk.CTkLabel(self.tk_edit_patient_frame, text="Pain Level", bg_color=vdark_widget_color, text_color=header_font_color)
        self.tk_pain_level_label.grid(row=5, column=0, sticky="nsew")
        self.tk_specific_label = ctk.CTkLabel(self.tk_edit_patient_frame, text="Specific", bg_color=dark_widget_color, text_color=header_font_color)
        self.tk_specific_label.grid(row=6, column=0, sticky="nsew")

        self.tk_life_threat_var = tk.StringVar(value="-")
        self.tk_life_threat_frame = ctk.CTkOptionMenu(self.tk_edit_patient_frame, fg_color=light_widget_color, text_color=subheader_font_color, button_color=dark_widget_color, values=["-", "Shock", "Compromised", "Inadequate", "Difficult"], variable=self.tk_life_threat_var)
        self.tk_life_threat_frame.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_consciousness_var = tk.StringVar(value="-")
        self.tk_consciousness_frame = ctk.CTkOptionMenu(self.tk_edit_patient_frame, fg_color=vlight_widget_color, text_color=subheader_font_color, button_color=vdark_widget_color, values=["-", "Fitting", "Unresponsive", "Responsive", "History"], variable=self.tk_consciousness_var)
        self.tk_consciousness_frame.grid(row=2, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_haemorrhage_var = tk.StringVar(value="-")
        self.tk_haemorrhage_frame = ctk.CTkOptionMenu(self.tk_edit_patient_frame, fg_color=light_widget_color, text_color=subheader_font_color, button_color=dark_widget_color, values=["-", "Extreme", "Major", "Minor"], variable=self.tk_haemorrhage_var)
        self.tk_haemorrhage_frame.grid(row=3, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_temperature_var = tk.StringVar(value="-")
        self.tk_temperature_frame = ctk.CTkOptionMenu(self.tk_edit_patient_frame, fg_color=vlight_widget_color, text_color=subheader_font_color, button_color=vdark_widget_color, values=["-", "V. Hot", "Hot", "Warm", "Cold"], variable=self.tk_temperature_var)
        self.tk_temperature_frame.grid(row=4, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_pain_level_var = tk.StringVar(value="-")
        self.tk_pain_level_frame = ctk.CTkOptionMenu(self.tk_edit_patient_frame, fg_color=light_widget_color, text_color=subheader_font_color, button_color=dark_widget_color, values=["-", "Severe", "Moderate", "Mild Pain", "Mild Itch"], variable=self.tk_pain_level_var)
        self.tk_pain_level_frame.grid(row=5, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_specific_frame = ctk.CTkFrame(self.tk_edit_patient_frame, bg_color=vdark_widget_color)
        self.tk_specific_frame.grid(row=6, column=1, sticky="nsew", padx=1, pady=1)

        self.tk_submit_button = ctk.CTkButton(self.tk_edit_patient_frame, text="Submit", fg_color=button_color, command=self.submit_patient_changes, width=10, border_width=2, border_color=dark_widget_color)
        self.tk_submit_button.grid(row=1, column=2, sticky="nsew", rowspan=7, padx=5, pady=5)

    def add_patient(self):
        ssn = self.tk_add_patient_ssn_entry.get()
        age = self.tk_add_patient_age_entry.get()
        sex = self.tk_add_patient_sex_entry.get()
        longitude = self.tk_add_patient_longitude_entry.get()
        latitude = self.tk_add_patient_latitude_entry.get()

        patient = Patient(id=self.next_patient_id, ssn=ssn, age=age, is_male=True if sex == "Male" else False, longitude=longitude, latitude=latitude)

        row = len(self.patients)+1

        ssn = str(patient.ssn) if patient.ssn else "-"
        age = str(patient.age) if patient.age else "-"
        longitude = str(patient.longitude) if patient.longitude else "-"
        latitude = str(patient.latitude) if patient.latitude else "-"
        emergency_level = str(patient.emergency_level) if patient.emergency_level else "-"
        classification = patient.classification.name if patient.emergency_level > 0 else "-"

        patient_row = [None, None, None, None, None, None, None, None]
        patient_row[0] = ctk.CTkButton(self.tk_patients_list_frame, text=str(patient.id), command=lambda: self.patient_selected(patient.id), width=5, border_width=2, border_color=dark_widget_color, fg_color=button_color)
        patient_row[0].grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
        patient_row[1] = ctk.CTkLabel(self.tk_patients_list_frame, text=ssn, bg_color=vlight_widget_color, text_color=subheader_font_color)
        patient_row[1].grid(row=row, column=1, sticky="nsew")
        patient_row[2] = ctk.CTkLabel(self.tk_patients_list_frame, text=age, bg_color=light_widget_color, text_color=subheader_font_color)
        patient_row[2].grid(row=row, column=2, sticky="nsew")
        patient_row[3] = ctk.CTkLabel(self.tk_patients_list_frame, text=patient.get_sex(), bg_color=vlight_widget_color, text_color=subheader_font_color)
        patient_row[3].grid(row=row, column=3, sticky="nsew")
        patient_row[4] = ctk.CTkLabel(self.tk_patients_list_frame, text=longitude, bg_color=light_widget_color, text_color=subheader_font_color)
        patient_row[4].grid(row=row, column=4, sticky="nsew")
        patient_row[5] = ctk.CTkLabel(self.tk_patients_list_frame, text=latitude, bg_color=vlight_widget_color, text_color=subheader_font_color)
        patient_row[5].grid(row=row, column=5, sticky="nsew")
        patient_row[6] = ctk.CTkLabel(self.tk_patients_list_frame, text=emergency_level, bg_color=light_widget_color, text_color=subheader_font_color)
        patient_row[6].grid(row=row, column=6, sticky="nsew")
        patient_row[7] = ctk.CTkLabel(self.tk_patients_list_frame, text=classification, bg_color=vlight_widget_color, text_color=subheader_font_color)
        patient_row[7].grid(row=row, column=7, sticky="nsew")
        self.patients.append(patient_row)

        self.next_patient_id += 1

    def patient_selected(self, id):
        print("Patient " + str(id) + " selected.")

        self.selected_idx = None
        for idx, patient in enumerate(self.patients):
            patient[0].configure(fg_color=button_color)

            if patient[0].cget("text") == str(id):
                self.selected_idx = idx

        self.patients[self.selected_idx][0].configure(fg_color=button_highlight_color)

    def remove_patient_row(self, idx):
        self.patients.pop(idx)
        for widget in self.tk_patients_list_frame.children.values():
            widget.grid_forget()

        self.set_patients_header_grid()
        for row, patient in enumerate(self.patients):
            for column, i in enumerate(patient):
                i.grid(row=row+1, column=column, sticky="nsew")

        self.tk_patients_list_frame.update_idletasks()

        if self.selected_idx == idx:
            self.selected_idx = None
            self.clear_edit()
        elif self.selected_idx > idx:
            self.selected_idx -= 1

    def clear_edit(self):
        pass

    def submit_patient_changes(self):
        pass

    def set_patients_header_grid(self):
        self.tk_patients_id_label.grid(row=0, column=0, sticky="nsew")
        self.tk_patients_ssn_label.grid(row=0, column=1, sticky="nsew")
        self.tk_patients_age_label.grid(row=0, column=2, sticky="nsew")
        self.tk_patients_sex_label.grid(row=0, column=3, sticky="nsew")
        self.tk_patients_longitude_label.grid(row=0, column=4, sticky="nsew")
        self.tk_patients_latitude_label.grid(row=0, column=5, sticky="nsew")
        self.tk_patients_emergency_level_label.grid(row=0, column=6, sticky="nsew")
        self.tk_patients_emergency_class_label.grid(row=0, column=7, sticky="nsew")

    def on_patients_list_frame_configure(self, event):
        self.tk_patients_canvas.configure(scrollregion=self.tk_patients_canvas.bbox("all"))

    def on_patients_canvas_configure(self, event):
        self.tk_patients_canvas.itemconfigure(self.tk_patients_canvas_frame, width=event.width)

if __name__ == "__main__":
    app = Triage()
    app.mainloop()
