import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from enum import Enum
from dataclasses import dataclass, field

from tk_scrolled_listbox import ScrolledListbox
from cep_manager import Cep_manager, ConnectionError

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

@dataclass
class Symptoms:
    life_threat: int = None
    consciousness: int = None
    haemorrhage: int = None
    temperature: float = 36.1
    pain_level: int = None
    specific: list = field(default_factory=list)

@dataclass
class Patient_unit:
    patient: Patient
    symptoms: Symptoms
    published: Symptoms
    row: list

class Triage(ctk.CTk):
    def __init__(self):

        try:
            self.cep_manager = Cep_manager()
        except ConnectionError as e:
            print("Could not connect to RabbitMQ. Please start the server and try again.")
            exit()

        # These symptoms are only for mental, palpitations, asthma, allergy and diarrhea and vomit emergencies. The complete list of symptoms is in the Manchester Triage handbook.
        self.specific_symptoms = {
            "High risk of self-harm": "self-harm high risk",
            "High risk of harming others": "other-harm high risk",
            "Violence": "violence",
            "Moderate risk of self-harm": "self-harm moderate risk",
            "Moderate risk of harming others": "other-harm moderate risk",
            "Significant distress": "significant distress",
            "Significant psychiatric history": "significant psychiatric history",
            "Agressive demeanor": "agressive demeanor",
            "Crying easily": "crying easily",
            "Recent risk of self-harm": "recent self-harm risk",
            "Recent risk of harming others": "recent other-harm risk",
            "Moderate distress": "moderate distress",
            "Disruptive demeanor": "disruptive demeanor",
            "Crying": "crying",
            "Abnormal pulse": "abnormal pulse",
            "Intoxication history": "intoxication history",
            "Chest pain": "chest pain",
            "Palpitations": "palpitations",
            "Significant cardiac history": "significant cardiac history",
            "Relative cardiac history": "relative cardiac history",
            "Difficulty speaking": "difficulty speaking",
            "Abnormal pulse": "abnormal pulse",
            "Significant respiratory history": "significant respiratory history",
            "Chest pain": "chest pain",
            "Sunken ribs": "sunken ribs",
            "Ineffective medication": "ineffective medication",
            "Nostril flare": "nostril flare",
            "Dry cough": "dry cough",
            "Wet cough": "wet cough",
            "Difficulty speaking": "difficulty speaking",
            "Swollen face": "swollen face",
            "Abnormal pulse": "abnormal pulse",
            "Skin rash": "skin rash",
            "Swollen hands": "swollen hands",
            "Localized swelling": "localized swelling",
            "Recent swelling": "recent swelling",
            "Severe thirst": "severe thirst",
            "Slenderness": "slenderness",
            "Blood vomit": "blood vomit",
            "Rectal bleeding leakage": "rectal bleeding leakage",
            "Blood vomit history": "blood vomit history",
            "Red or black deposition": "red or black deposition",
            "Dehidration signs": "dehidration signs",
            "Frequent deposition": "frequent deposition",
            "Vomiting": "vomiting",
            "Anorexia": "anorexia",
            "Nausea": "nausea",
            "Thrist": "thrist",
            "Abdominal pain": "abdominal pain"
        }
        self.inverse_specific_symptoms_options = {v: k for k, v in self.specific_symptoms.items()}

        self.life_threat_options = {
            "-": None,
            "Shock": 2,
            "Compromised": 0,
            "Inadequate": 1,
            "Difficult": 3
        }
        self.inverse_life_threat_options = {v: k for k, v in self.life_threat_options.items()}

        self.consciousness_options = {
            "-": None,
            "Fitting": 0,
            "Unresponsive": 1,
            "Alt. Responsive": 2,
            "History": 3
        }
        self.inverse_consciousness_options = {v: k for k, v in self.consciousness_options.items()}

        self.haemorrhage_options = {
            "-": None,
            "Extreme": 0,
            "Major": 1,
            "Minor": 2
        }
        self.inverse_haemorrhage_options = {v: k for k, v in self.haemorrhage_options.items()}

        self.pain_level_options = {
            "-": None,
            "Severe": 0,
            "Moderate": 1,
            "Mild Pain": 2,
            "Mild Itch": 3
        }
        self.inverse_pain_level_options = {v: k for k, v in self.pain_level_options.items()}

        self.patients = []
        self.next_patient_id = 0
        self.selected_patient_idx = None

        self.create_tk()
        self.clear_edit()

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
        self.tk_life_threat_selector = ctk.CTkSegmentedButton(self.tk_edit_patient_frame, fg_color=light_widget_color, text_color=subheader_font_color, values=list(self.life_threat_options.keys()), variable=self.tk_life_threat_var)
        self.tk_life_threat_selector.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_consciousness_var = tk.StringVar(value="-")
        self.tk_consciousness_selector = ctk.CTkSegmentedButton(self.tk_edit_patient_frame, fg_color=vlight_widget_color, text_color=subheader_font_color, values=list(self.consciousness_options.keys()), variable=self.tk_consciousness_var)
        self.tk_consciousness_selector.grid(row=2, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_haemorrhage_var = tk.StringVar(value="-")
        self.tk_haemorrhage_selector = ctk.CTkSegmentedButton(self.tk_edit_patient_frame, fg_color=light_widget_color, text_color=subheader_font_color, values=list(self.haemorrhage_options.keys()), variable=self.tk_haemorrhage_var)
        self.tk_haemorrhage_selector.grid(row=3, column=1, sticky="nsew", padx=1, pady=1)

        self.tk_temperature_frame = ctk.CTkFrame(self.tk_edit_patient_frame, fg_color=vlight_widget_color)
        self.tk_temperature_frame.grid(row=4, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_temperature_frame.grid_rowconfigure(0, weight=1)
        self.tk_temperature_frame.grid_columnconfigure(0, weight=1)
        self.tk_temperature_frame.grid_columnconfigure(1, weight=8)
        self.tk_temperature_var = tk.StringVar(value="36.1ºC")
        self.tk_temperature_label = ctk.CTkLabel(self.tk_temperature_frame, textvariable=self.tk_temperature_var, bg_color=vlight_widget_color, text_color=subheader_font_color)
        self.tk_temperature_label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.tk_temperature_slider = ctk.CTkSlider(self.tk_temperature_frame, from_=30.0, to=45.0, command=self.on_temperature_slider_changed)
        self.tk_temperature_slider.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)

        self.tk_pain_level_var = tk.StringVar(value="-")
        self.tk_pain_level_selector = ctk.CTkSegmentedButton(self.tk_edit_patient_frame, fg_color=light_widget_color, text_color=subheader_font_color, values=list(self.pain_level_options.keys()), variable=self.tk_pain_level_var)
        self.tk_pain_level_selector.grid(row=5, column=1, sticky="nsew", padx=1, pady=1)
        self.tk_specific_var = tk.StringVar(value="-")
        self.tk_specific_selector = ScrolledListbox(self.tk_edit_patient_frame, listvariable=sorted(self.specific_symptoms.keys()), selectmode=tk.MULTIPLE)
        self.tk_specific_selector.grid(row=6, column=1, sticky="nsew", padx=1, pady=1)

        self.tk_delete_button = ctk.CTkButton(self.tk_edit_patient_frame, text="Delete\nPatient", fg_color=dark_widget_color, command=lambda: self.remove_patient_row(self.selected_patient_idx), width=10, border_width=2, border_color=dark_widget_color)
        self.tk_delete_button.grid(row=1, column=2, sticky="nsew", rowspan=2, padx=5, pady=3)
        self.tk_submit_button = ctk.CTkButton(self.tk_edit_patient_frame, text="Submit\nChanges", fg_color=button_color, command=self.submit_patient_changes, width=10, border_width=2, border_color=dark_widget_color)
        self.tk_submit_button.grid(row=3, column=2, sticky="nsew", rowspan=5, padx=5, pady=3)

    def on_temperature_slider_changed(self, value):
        self.tk_temperature_var.set(str(round(value,1))+u"ºC")

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

        patient_unit = Patient_unit(patient=patient, symptoms=Symptoms(), published=Symptoms(), row=patient_row)
        self.patients.append(patient_unit)

        self.cep_manager.publish_patient(patient_unit.patient)

        self.next_patient_id += 1

    def patient_selected(self, id):
        print("Patient " + str(id) + " selected.")

        self.selected_patient_idx = None
        for idx, patient in enumerate(self.patients):
            row = patient.row
            row[0].configure(fg_color=button_color)

            if row[0].cget("text") == str(id):
                self.selected_patient_idx = idx

        self.patients[self.selected_patient_idx].row[0].configure(fg_color=button_highlight_color)

        self.clear_edit()
        self.activate_edit(self.patients[self.selected_patient_idx])

    def remove_patient_row(self, idx):
        self.patients.pop(idx)
        for widget in self.tk_patients_list_frame.children.values():
            widget.grid_forget()

        self.set_patients_header_grid()
        for row, patient in enumerate(self.patients):
            for column, i in enumerate(patient.row):
                i.grid(row=row+1, column=column, sticky="nsew")

        self.tk_patients_list_frame.update_idletasks()

        if self.selected_patient_idx == idx:
            self.selected_patient_idx = None
            self.clear_edit()
        elif self.selected_patient_idx > idx:
            self.selected_patient_idx -= 1

    def clear_edit(self):
        self.tk_life_threat_var.set("-")
        self.tk_consciousness_var.set("-")
        self.tk_haemorrhage_var.set("-")
        self.tk_temperature_var.set("36.1ºC")
        self.tk_pain_level_var.set("-")

        # Disable all frame buttons
        for widget in self.tk_edit_patient_frame.winfo_children():
            if type(widget) in (ctk.CTkSegmentedButton, ctk.CTkButton):
                widget.configure(state="disabled")

        self.tk_temperature_slider.set(36.1)
        self.tk_temperature_slider.configure(state="disabled")
        self.tk_specific_selector.clear_selected()
        self.tk_specific_selector.disable_list()

    def activate_edit(self, patient):
        for widget in self.tk_edit_patient_frame.winfo_children():
            if type(widget) in (ctk.CTkSegmentedButton, ctk.CTkButton):
                widget.configure(state="normal")

        self.tk_temperature_slider.configure(state="normal")
        self.tk_specific_selector.activate_list()

        if patient.symptoms.life_threat:
            self.tk_life_threat_var.set(self.inverse_life_threat_options[patient.symptoms.life_threat])
        if patient.symptoms.consciousness:
            self.tk_consciousness_var.set(self.inverse_consciousness_options[patient.symptoms.consciousness])
        if patient.symptoms.haemorrhage:
            self.tk_haemorrhage_var.set(self.inverse_haemorrhage_options[patient.symptoms.haemorrhage])
        self.tk_temperature_slider.set(patient.symptoms.temperature)
        self.tk_temperature_var.set(str(patient.symptoms.temperature) + "ºC")
        if patient.symptoms.pain_level:
            self.tk_pain_level_var.set(self.inverse_pain_level_options[patient.symptoms.pain_level])
        if patient.symptoms.specific:
            self.tk_specific_selector.set_selected([self.inverse_specific_symptoms_options[i] for i in patient.symptoms.specific])

    def submit_patient_changes(self):
        life_threat = self.tk_life_threat_var.get()
        consciousness = self.tk_consciousness_var.get()
        haemorrhage = self.tk_haemorrhage_var.get()
        temperature = float(self.tk_temperature_var.get()[:-2])
        pain_level = self.tk_pain_level_var.get()

        if life_threat == "-": life_threat = None
        if consciousness == "-": consciousness = None
        if haemorrhage == "-": haemorrhage = None
        if pain_level == "-": pain_level = None

        symptoms_container = self.patients[self.selected_patient_idx].symptoms
        symptoms_container.life_threat = self.life_threat_options.get(life_threat)
        symptoms_container.consciousness = self.consciousness_options.get(consciousness)
        symptoms_container.haemorrhage = self.haemorrhage_options.get(haemorrhage)
        symptoms_container.temperature = temperature
        symptoms_container.pain_level = self.pain_level_options.get(pain_level)
        symptoms_container.specific = list(map(self.specific_symptoms.get, self.tk_specific_selector.get_selected()))

        self.publish_to_cep(self.patients[self.selected_patient_idx])

    def publish_to_cep(self, patient_unit):
        patient = patient_unit.patient
        symptoms = patient_unit.symptoms
        published = patient_unit.published

        if symptoms.life_threat is not None and symptoms.life_threat != published.life_threat:
            self.cep_manager.publish_life_threat(patient.id, symptoms.life_threat)
            published.life_threat = symptoms.life_threat
        if symptoms.consciousness is not None and symptoms.consciousness != published.consciousness:
            self.cep_manager.publish_consciousness(patient.id, symptoms.consciousness)
            published.consciousness = symptoms.consciousness
        if symptoms.haemorrhage is not None and symptoms.haemorrhage != published.haemorrhage:
            self.cep_manager.publish_haemorrhage(patient.id, symptoms.haemorrhage)
            published.haemorrhage = symptoms.haemorrhage
        if symptoms.temperature is not None and symptoms.temperature != published.temperature:
            self.cep_manager.publish_temperature(patient.id, symptoms.temperature)
            published.temperature = symptoms.temperature
        if symptoms.pain_level is not None and symptoms.pain_level != published.pain_level:
            self.cep_manager.publish_pain_level(patient.id, symptoms.pain_level)
            published.pain_level = symptoms.pain_level
        if symptoms.specific:
            for symptom in symptoms.specific:
                if symptom not in published.specific:
                    self.cep_manager.publish_specific_symptom(patient.id, symptom)
            published.specific = symptoms.specific


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
