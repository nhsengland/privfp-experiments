from streamlit_annotation_tools import text_labeler
import streamlit as st

fake_data = [
    "Clinical Note:\nPatient: Harris Fadel\nNHS Number: 5927778917\nDate of Birth: August 8, 2005\n\nPresentation: Acute bronchitis (disorder)\n\nSymptoms:\n\n* Cough\n* Chest tightness\n* Shortness of breath\n\nMedical History:\n\n* Recent respiratory infection\n\nReview of Systems:\n\n* No reported fever or chills\n* No cough productive of yellow or green mucus\n\nPlan:\n\n* Prescribe antibiotics for 7-10 days\n* Instruct patient to rest and avoid strenuous activities\n* Monitor patient's condition closely and adjust plan as needed.",
    "Clinical Note for Patient Wallace Tremblay:\n\n Patient with lime green curly hair presents with acute bronchitis, as confirmed by clinical evaluation and laboratory results. The patient is a 13-year-old male with a NHS number of 5693788113, born on June 13th, 2006. Symptoms include cough, chest tightness, and fever. Treatment plan includes antibiotics and bronchodilators as needed, as well as instructions for self-care and rest. Further evaluation and monitoring are necessary to ensure proper management of this condition.",
    'Certainly! Here is an example clinical note for Shayna VonRueden based on the provided information:\n\n"Patient presents with viral sinusitis. Date of birth: 11/28/2015. NHS number: 0939087782. Given name: Shayna. Family name: VonRueden. Diagnosis: Viral sinusitis (disorder)."\n\nI hope this meets your requirements! Let me know if you have any further questions.',
    "Clinical Note:\nPatient Name: Ramon Kohler\nNHS Number: 0169779904\nDate of Birth: May 9, 1973\n\nPresenting Complaint: Chronic pain in the left shoulder and arm, affecting daily activities.\n\nHistory of Present Illness: The patient experienced a fall two months ago resulting in a dislocation of the left shoulder. Since then, the patient has been experiencing persistent pain in the left shoulder and arm, which has worsened despite initial treatment with analgesics.\n\nReview of Systems: The patient reports difficulty sleeping due to pain and experiences numbness and tingling in the left arm. There is no history of trauma or injury to the left shoulder or arm.\n\nPlan: Further evaluation and imaging studies are necessary to determine the cause of chronic pain. In the meantime, the patient will be referred to physical therapy for non-invasive treatment options.",
    "Clinical Note:\n\nPatient Name: Tyesha Dach\nNHS Number: 3494867836\nDate of Birth: September 24, 1970\n\nDiagnosis: Childhood asthma\n\nChief Complaint: Wheezing and shortness of breath for the past week.\n\nHistory of Present Illness: The patient is a 5-year-old girl who presented to the clinic with a 2-day history of wheezing and shortness of breath. She was seen in the emergency room earlier in the week for similar symptoms, where she was diagnosed with asthma and prescribed an inhaler. However, her symptoms persisted, leading her parents to seek further evaluation.\n\nSystems Examination: The patient's breath sounds are adventitious, with a high-pitched wheezing sound on expiration. Her chest is slightly expanded, and there is minimal tactile fremitus. The patient's oxygen saturation is 90% on room air.\n\nRecommendations:\n\n* Continue prescribed inhaler therapy\n* Monitor symptoms closely and adjust medication as needed\n* Educate parents on proper use of inhaler and management of asthma symptoms",
    "Clinical Note:\nMr. Austin Morar, a 59-year-old male patient, presents to the clinic today with a 3-day history of cough and fever. He reports difficulty breathing and chest tightness. His NHS number is 7723641893 and he was born on April 7th, 1963. Based on his symptoms and medical history, I diagnose him with acute bronchitis. Further assessment and testing may be necessary to rule out any underlying conditions.",
    "Clinical Note:\nMs. Allison King, a 53-year-old woman, presented to the clinic for her scheduled prenatal appointment at 20 weeks gestation. She is in normal health and has no significant medical history. Her NHS number is 9877791390, she was born on April 6th, 1967, and her diagnosis is normal pregnancy.",
    "Clinical Note:\nPatient Name: Juanita Okuneva\nNHS Number: 5870122848\nDate of Birth: January 22, 1951\n\nChief Complaint: Acute bronchitis (disorder)\n\nHistory of Present Illness: Patient Juanita Okuneva, a 71-year-old female, presents with cough and fever for the past week. She reports difficulty breathing and chest tightness. No recent travel or exposure to sick individuals.\n\nAssessment: Based on patient's symptoms and medical history, acute bronchitis is a likely diagnosis. Further evaluation and diagnostic tests will be conducted to rule out other potential causes of respiratory distress.",
    "Clinical Note for Valda Morissette:\n\nMs. Morissette presents today with persistent perennial allergic rhinitis, characterized by nasal congestion, sneezing, and itchy eyes. She reports worsening symptoms throughout the spring and summer months, consistent with her seasonal allergy triggers. Her NHS number is 6393976098 and she was born on February 2nd, 1962.",
    "Clinical Note:\nMr. John Bosco, a 65-year-old male patient, was admitted to the hospital on March 18th with acute bronchitis. His NHS number is 1954287143 and he was born on March 16th, 1953. His diagnosis is acute bronchitis (disorder).",
]

# Initialize the session state once at the start of the app
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    for key in range(len(fake_data)):
        st.session_state[key] = []


def update():
    temp = st.session_state["temp"]
    st.session_state[temp["id"]] = temp["annotations"]


def annotation_tool(data):

    slider_id = st.slider(
        "Select Clinician Note",
        1,
        len(fake_data) - 1,
        on_change=update,
        key="my_slider",
    )

    string = data[slider_id - 1]
    labels = st.session_state[slider_id]

    annotations = text_labeler(string, labels)
    print(annotations)
    st.session_state["temp"] = {"id": slider_id, "annotations": annotations}

    # button = st.button("Submit Labels")
    # if button:
    #     st.session_state[slider_id] = annotations


annotation_tool(fake_data)

verbose = False
if verbose:
    st.write(st.session_state)
