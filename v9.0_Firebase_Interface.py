import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Using secrets for Firebase credentials
cred = credentials.Certificate({
    "type": st.secrets["FIREBASE_TYPE"],
    "project_id": st.secrets["FIREBASE_PROJECT_ID"],
    "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace('\\n', '\n'),
    "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
    "client_id": st.secrets["FIREBASE_CLIENT_ID"],
    "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
    "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_PROVIDER_CERT_URL"],
    "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_CERT_URL"]
})

# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://fix-medsense--interface-default-rtdb.firebaseio.com/' 
# })

# Check if the default Firebase app already exists before initializing it
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://fix-medsense--interface-default-rtdb.firebaseio.com/'
    })

# Function to save data to Firebase
def save_to_firebase(data, phase):
    ref = db.reference(f'responses/{phase}')
    ref.push(data)

# Function to read data from Firebase
def read_from_firebase(phase):
    ref = db.reference(f'responses/{phase}')
    return ref.get()

# Initialize language in session state if not already initialized
if 'language' not in st.session_state:
    st.session_state.language = "English"  # Default language

# Place the language selection directly in the main script
language = st.sidebar.selectbox("Select Language", ["English", "Bahasa Indonesia"], key="language_selectbox")
st.session_state.language = language

# Load data from the provided Excel file based on selected language
@st.cache
def load_data(language):
    file_path = "Re_Answers_Prompts_ChatGPT4.xlsx"
    data = pd.read_excel(file_path, sheet_name="Sheet1")
    
    if language == "English":
        data = data.rename(columns={
            "Formula name": "scenario_category",
            "English Prompt Scenario": "scenario",
            "English_Answers": "answer",
            "Added_Question_Scenario_English": "additional_question",
            "Added_Question_Answers_English": "additional_answer"
        })
    else:
        data = data.rename(columns={
            "Formula name": "scenario_category",
            "Indonesia Prompt Scenario": "scenario",
            "Indonesia_Answers": "answer",
            "Added_Question_Scenario_Indonesia": "additional_question",
            "Added_Question_Answers_Indonesia": "additional_answer"
        })
    return data

data = load_data(st.session_state.language)
all_scenarios = data.to_dict(orient='records')

# Initialize session state variables if not already initialized
if 'selected_prompts' not in st.session_state:
    st.session_state.selected_prompts = random.sample(all_scenarios, 5)
if 'phase_3_prompts' not in st.session_state:
    st.session_state.phase_3_prompts = random.sample([s for s in all_scenarios if s not in st.session_state.selected_prompts], 5)

def translate_text(text, language):
    translations = {
        "English": {
            "Sign-Up": "Sign-Up",
            "Name": "Name",
            "Username": "Username",
            "Password": "Password",
            "Sign Up": "Sign Up",
            "Please fill all the fields": "Please fill all the fields",
            "Welcome": "Welcome",
            "Phase 1: Initial Prompt Evaluation": "Phase 1: Initial Prompt Evaluation",
            "Scenario Category": "Scenario Category",
            "Example of the Scenario": "Example of the Scenario",
            "Enter your initial prompt question": "Enter your initial prompt question",
            "Enter your response/answers for the initial prompt": "Enter your response/answers for the initial prompt",
            "Submit Initial Response": "Submit Initial Response",
            "Initial response submitted": "Initial response submitted",
            "Phase 2: Evaluate Randomized Scenarios": "Phase 2: Evaluate Randomized Scenarios",
            "Original Question": "Original Question",
            "Original Answer": "Original Answer",
            "Rate the original answer": "Rate the original answer",
            "Your Answer on the original prompt (The answer supposed to be)": "Your Answer on the original prompt (The answer supposed to be)",
            "Additional Question": "Additional Question",
            "Additional Answer": "Additional Answer",
            "Rate the additional answer": "Rate the additional answer",
            "Your Answer on the additional prompt (The answer supposed to be)": "Your Answer on the additional prompt (The answer supposed to be)",
            "Next Scenario": "Next Scenario",
            "Thank you for completing all scenarios": "Thank you for completing all scenarios",
            "Phase 3: Create Prompts for New Scenarios": "Phase 3: Create Prompts for New Scenarios",
            "Enter your prompt question for this scenario": "Enter your prompt question for this scenario",
            "Enter your response to the prompt": "Enter your response to the prompt",
            "Next Scenario (Phase 3)": "Next Scenario (Phase 3)",
            "General feedback on the scenarios": "General feedback on the scenarios",
            "Overall satisfaction with the process": "Overall satisfaction with the process",
            "Submit Feedback": "Submit Feedback",
            "Thank you for your feedback": "Thank you for your feedback",
            "You have input": "You have input",
            "inputs.": "inputs.",
            "You have": "You have",
            "inputs left.": "inputs left."
        },
        "Bahasa Indonesia": {
            "Sign-Up": "Daftar",
            "Name": "Nama",
            "Username": "Nama Pengguna",
            "Password": "Kata Sandi",
            "Sign Up": "Daftar",
            "Please fill all the fields": "Silakan isi semua bidang",
            "Welcome": "Selamat datang",
            "Phase 1: Initial Prompt Evaluation": "Fase 1: Evaluasi Prompt Awal",
            "Scenario Category": "Kategori Skenario",
            "Example of the Scenario": "Contoh Skenario",
            "Enter your initial prompt question": "Masukkan pertanyaan prompt awal Anda",
            "Enter your response/answers for the initial prompt": "Masukkan jawaban Anda untuk prompt awal",
            "Submit Initial Response": "Kirim Tanggapan Awal",
            "Initial response submitted": "Tanggapan awal dikirim",
            "Phase 2: Evaluate Randomized Scenarios": "Fase 2: Evaluasi Skenario Acak",
            "Original Question": "Pertanyaan Asli",
            "Original Answer": "Jawaban Asli",
            "Rate the original answer": "Beri nilai jawaban asli",
            "Your Answer on the original prompt (The answer supposed to be)": "Jawaban Anda pada prompt asli (Jawaban seharusnya)",
            "Additional Question": "Pertanyaan Tambahan",
            "Additional Answer": "Jawaban Tambahan",
            "Rate the additional answer": "Beri nilai jawaban tambahan",
            "Your Answer on the additional prompt (The answer supposed to be)": "Jawaban Anda pada prompt tambahan (Jawaban seharusnya)",
            "Next Scenario": "Skenario Berikutnya",
            "Thank you for completing all scenarios": "Terima kasih telah menyelesaikan semua skenario",
            "Phase 3: Create Prompts for New Scenarios": "Fase 3: Buat Prompt untuk Skenario Baru",
            "Enter your prompt question for this scenario": "Masukkan pertanyaan prompt Anda untuk skenario ini",
            "Enter your response to the prompt": "Masukkan jawaban Anda",
            "Next Scenario (Phase 3)": "Skenario Berikutnya (Fase 3)",
            "General feedback on the scenarios": "Umpan balik umum pada skenario",
            "Overall satisfaction with the process": "Kepuasan keseluruhan dengan proses",
            "Submit Feedback": "Kirim Umpan Balik",
            "Thank you for your feedback": "Terima kasih atas umpan balik Anda",
            "You have input": "Anda telah menginput",
            "inputs.": "input.",
            "You have": "Anda memiliki",
            "inputs left.": "input tersisa."
        }
    }
    return translations[language].get(text, text)

# Navigation and session state management
st.sidebar.title(translate_text("Navigation", st.session_state.language))

# Sign-Up Session
def render_sign_up():
    st.title(translate_text("Medsense Survey Interface Rating from Doctor", st.session_state.language))
    st.subheader(translate_text("Sign-Up", st.session_state.language))
    name = st.text_input(translate_text("Name", st.session_state.language))
    username = st.text_input(translate_text("Username", st.session_state.language))
    password = st.text_input(translate_text("Password", st.session_state.language), type="password")
    
    if st.button(translate_text("Sign Up", st.session_state.language), key="sign_up_button"):
        if not name or not username or not password:
            st.error(translate_text("Please fill all the fields", st.session_state.language))
        else:
            st.session_state.user = {"name": name, "username": username, "password": password}
            st.success(f"{translate_text('Welcome', st.session_state.language)}, {name}, . You can go to the phase 1 page!")
            st.session_state.page = 'phase_1'

# Phase 1: Initial Prompt Generation
def render_phase_1():
    st.subheader(translate_text("Phase 1: Initial Prompt Evaluation", st.session_state.language))
    selected_scenario = st.session_state.selected_prompts[len(st.session_state.get('initial_responses', []))]  # Get the current scenario
    st.info(f"**{translate_text('Scenario Category', st.session_state.language)}:** {selected_scenario['scenario_category']}")
    prompt_question = st.text_input(translate_text("Enter your initial prompt question", st.session_state.language))
    prompt_response = st.text_area(translate_text("Enter your response/answers for the initial prompt", st.session_state.language))

    num_responses = len(st.session_state.get('initial_responses', []))
    st.info(f"{translate_text('You have input', st.session_state.language)} {num_responses} {translate_text('inputs.', st.session_state.language)}")
    st.info(f"{translate_text('You have', st.session_state.language)} {5 - num_responses} {translate_text('inputs left.', st.session_state.language)}")

    if st.button(translate_text('Submit Initial Response', st.session_state.language)):
        st.session_state.initial_responses = st.session_state.get('initial_responses', [])
        st.session_state.initial_responses.append({
            'user': st.session_state.user['username'],
            'phase': 'Phase 1',
            'scenario': selected_scenario['scenario'],
            'prompt_question': prompt_question,
            'prompt_response': prompt_response,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_to_firebase(st.session_state.initial_responses[-1], "Phase_1")
        st.success(translate_text('Initial response submitted!', st.session_state.language))
        
        if len(st.session_state.initial_responses) >= 5:  # 5 submissions per Phase 1
            st.session_state.page = 'phase_2'
        else:
            st.experimental_rerun()

# # Phase 2: Evaluate Randomized Scenarios
# def render_phase_2():
#     st.subheader(translate_text("Phase 2: Evaluate Randomized Scenarios", st.session_state.language))
#     if 'current_scenario_index' not in st.session_state:
#         st.session_state.current_scenario_index = 0
#         st.session_state.responses = []

#     prompt = st.session_state.selected_prompts[st.session_state.current_scenario_index]

#     if st.session_state.language == 'English':
#         answer_key = 'answer'
#         additional_question_key = 'additional_question'
#         additional_answer_key = 'additional_answer'
#     else:
#         answer_key = 'answer'
#         additional_question_key = 'additional_question'
#         additional_answer_key = 'additional_answer'

#     with st.container():
#         st.info(f"**{translate_text('Original Question', st.session_state.language)}:** {prompt['scenario']}")
#         st.info(f"**{translate_text('Original Answer', st.session_state.language)}:** {prompt[answer_key]}")
#         rating_orig = st.slider(translate_text('Rate the original answer', st.session_state.language), 1, 5, key=f"rating_orig_{prompt['scenario']}")
#         response_orig = st.text_area(translate_text("Your Answer on the original prompt (The answer supposed to be)", st.session_state.language), key=f"response_orig_{prompt['scenario']}")

#         st.info(f"**{translate_text('Additional Question', st.session_state.language)}:** {prompt[additional_question_key]}")
#         st.info(f"**{translate_text('Additional Answer', st.session_state.language)}:** {prompt[additional_answer_key]}")
#         rating_add = st.slider(translate_text('Rate the additional answer', st.session_state.language), 1, 5, key=f"rating_add_{prompt['scenario']}")
#         response_add = st.text_area(translate_text("Your Answer on the additional prompt (The answer supposed to be)", st.session_state.language), key=f"response_add_{prompt['scenario']}")

#     num_responses = len(st.session_state.responses)
#     st.info(f"{translate_text('You have input', st.session_state.language)} {num_responses} {translate_text('inputs.', st.session_state.language)}")
#     st.info(f"{translate_text('You have', st.session_state.language)} {5 - num_responses} {translate_text('inputs left.', st.session_state.language)}")

#     if st.button(translate_text('Next Scenario', st.session_state.language)):
#         st.session_state.responses.append({
#             'user': st.session_state.user['username'],
#             'scenario': prompt['scenario'],
#             'original_rating': rating_orig,
#             'original_response': response_orig,
#             'additional_rating': rating_add,
#             'additional_response': response_add,
#             'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         })

#         if st.session_state.current_scenario_index < len(st.session_state.selected_prompts) - 1:
#             st.session_state.current_scenario_index += 1
#         else:
#             save_to_firebase(st.session_state.responses, "Phase_2")
#             st.success(translate_text("Thank you for completing all scenarios, please go to next phase", st.session_state.language))
#             st.session_state.page = 'phase_3'


# # Phase 2: Evaluate Randomized Scenarios
# def render_phase_2():
#     st.subheader(translate_text("Phase 2: Evaluate Randomized Scenarios", st.session_state.language))
    
#     # Initialize current_scenario_index and responses if not already initialized
#     if 'current_scenario_index' not in st.session_state:
#         st.session_state.current_scenario_index = 0
#         st.session_state.responses = []

#     # Select the current prompt based on the scenario index
#     prompt = st.session_state.selected_prompts[st.session_state.current_scenario_index]

#     # Determine the correct keys based on language
#     if st.session_state.language == 'English':
#         answer_key = 'answer'
#         additional_question_key = 'additional_question'
#         additional_answer_key = 'additional_answer'
#     else:
#         # Adjust the keys if using Indonesian data (ensure the column names are correct)
#         answer_key = 'Indonesia_Answers'  # Modify this according to data
#         additional_question_key = 'Added_Question_Scenario_Indonesia'
#         additional_answer_key = 'Added_Question_Answers_Indonesia'
#         # answer_key = 'answer'
#         # additional_question_key = 'additional_question'
#         # additional_answer_key = 'additional_answer'


#     with st.container():
#         # Display scenario category and original question
#         st.info(f"**{translate_text('Original Question', st.session_state.language)}:** {prompt['scenario']}")

#         # Check if 'answer_key' exists in the prompt before accessing it
#         if answer_key in prompt:
#             st.info(f"**{translate_text('Original Answer', st.session_state.language)}:** {prompt[answer_key]}")
#         else:
#             st.warning(f"**{translate_text('Original Answer', st.session_state.language)} not found in this prompt.**")
        
#         # User input for rating and response for the original answer
#         rating_orig = st.slider(translate_text('Rate the original answer', st.session_state.language), 1, 5, key=f"rating_orig_{prompt['scenario']}")
#         response_orig = st.text_area(translate_text("Your Answer on the original prompt (The answer supposed to be)", st.session_state.language), key=f"response_orig_{prompt['scenario']}")

#         # Check if 'additional_question_key' exists in the prompt before accessing it
#         if additional_question_key in prompt:
#             st.info(f"**{translate_text('Additional Question', st.session_state.language)}:** {prompt[additional_question_key]}")
#             st.info(f"**{translate_text('Additional Answer', st.session_state.language)}:** {prompt[additional_answer_key]}")
#         else:
#             st.warning(f"**{translate_text('Additional Question', st.session_state.language)} not found in this prompt.**")
        
#         # User input for rating and response for the additional answer
#         rating_add = st.slider(translate_text('Rate the additional answer', st.session_state.language), 1, 5, key=f"rating_add_{prompt['scenario']}")
#         response_add = st.text_area(translate_text("Your Answer on the additional prompt (The answer supposed to be)", st.session_state.language), key=f"response_add_{prompt['scenario']}")

#     # Show how many inputs are left
#     num_responses = len(st.session_state.responses)
#     st.info(f"{translate_text('You have input', st.session_state.language)} {num_responses} {translate_text('inputs.', st.session_state.language)}")
#     st.info(f"{translate_text('You have', st.session_state.language)} {5 - num_responses} {translate_text('inputs left.', st.session_state.language)}")

#     # Save the responses and go to the next scenario when "Next Scenario" is clicked
#     if st.button(translate_text('Next Scenario', st.session_state.language)):
#         st.session_state.responses.append({
#             'user': st.session_state.user['username'],
#             'scenario': prompt['scenario'],
#             'original_rating': rating_orig,
#             'original_response': response_orig,
#             'additional_rating': rating_add,
#             'additional_response': response_add,
#             'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         })

#         # Check if there are more scenarios to evaluate
#         if st.session_state.current_scenario_index < len(st.session_state.selected_prompts) - 1:
#             st.session_state.current_scenario_index += 1
#         else:
#             # Save all responses to Firebase
#             save_to_firebase(st.session_state.responses, "Phase_2")
#             st.success(translate_text("Thank you for completing all scenarios, please go to next phase", st.session_state.language))
#             st.session_state.page = 'phase_3'


def render_phase_2():
    st.subheader(translate_text("Phase 2: Evaluate Randomized Scenarios", st.session_state.language))

    # Ensure the current_scenario_index and responses are initialized
    if 'current_scenario_index' not in st.session_state:
        st.session_state.current_scenario_index = 0
        st.session_state.responses = []

    prompt = st.session_state.selected_prompts[st.session_state.current_scenario_index]

    # Select keys based on language
    if st.session_state.language == 'English':
        answer_key = 'English_Answer'
        additional_question_key = 'additional_question'
        additional_answer_key = 'additional_answer'
    else:
        answer_key = 'Indonesia_Answer'
        additional_question_key = 'Added_Question_Scenario_Indonesia'
        additional_answer_key = 'Added_Question_Answers_Indonesia'

    with st.container():
        # Display scenario category and original question
        st.info(f"**{translate_text('Original Question', st.session_state.language)}:** {prompt['scenario']}")

        # Check if 'answer' exists in the prompt
        if answer_key in prompt:
            st.info(f"**{translate_text('Original Answer', st.session_state.language)}:** {prompt[answer_key]}")
        else:
            st.warning(f"{translate_text('Original Answer not found in this prompt', st.session_state.language)}")

        # Rating and response for the original answer
        rating_orig = st.slider(translate_text('Rate the original answer', st.session_state.language), 1, 5, key=f"rating_orig_{prompt['scenario']}")
        response_orig = st.text_area(translate_text("Your Answer on the original prompt (The answer supposed to be)", st.session_state.language), key=f"response_orig_{prompt['scenario']}")

        # Check if additional question exists in the prompt
        if additional_question_key in prompt:
            st.info(f"**{translate_text('Additional Question', st.session_state.language)}:** {prompt[additional_question_key]}")
            st.info(f"**{translate_text('Additional Answer', st.session_state.language)}:** {prompt[additional_answer_key]}")
        else:
            st.warning(f"{translate_text('Additional Question not found in this prompt', st.session_state.language)}")

        # Rating and response for the additional answer
        rating_add = st.slider(translate_text('Rate the additional answer', st.session_state.language), 1, 5, key=f"rating_add_{prompt['scenario']}")
        response_add = st.text_area(translate_text("Your Answer on the additional prompt (The answer supposed to be)", st.session_state.language), key=f"response_add_{prompt['scenario']}")

    # Show input count and remaining inputs
    num_responses = len(st.session_state.responses)
    st.info(f"{translate_text('You have input', st.session_state.language)} {num_responses} {translate_text('inputs.', st.session_state.language)}")
    st.info(f"{translate_text('You have', st.session_state.language)} {5 - num_responses} {translate_text('inputs left.', st.session_state.language)}")

    # Handle the submission of responses and switching to the next scenario
    if st.button(translate_text('Next Scenario', st.session_state.language)):
        st.session_state.responses.append({
            'user': st.session_state.user['username'],
            'scenario': prompt['scenario'],
            'original_rating': rating_orig,
            'original_response': response_orig,
            'additional_rating': rating_add,
            'additional_response': response_add,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Move to the next scenario or complete phase 2
        if st.session_state.current_scenario_index < len(st.session_state.selected_prompts) - 1:
            st.session_state.current_scenario_index += 1
        else:
            save_to_firebase(st.session_state.responses, "Phase_2")
            st.success(translate_text("Thank you for completing all scenarios, please go to the next phase", st.session_state.language))
            st.session_state.page = 'phase_3'



# Phase 3: Similar to Phase 1 but with different scenarios
def render_phase_3():
    st.subheader(translate_text("Phase 3: Create Prompts for New Scenarios", st.session_state.language))
    if 'current_phase_3_index' not in st.session_state:
        st.session_state.current_phase_3_index = 0
        st.session_state.phase_3_responses = []

    prompt = st.session_state.phase_3_prompts[st.session_state.current_phase_3_index]
    st.info(f"**{translate_text('Scenario Category', st.session_state.language)}:** {prompt['scenario_category']}")
    prompt_question = st.text_input(translate_text("Enter your prompt question for this scenario", st.session_state.language), key=f"prompt_question_phase3_{prompt['scenario']}")
    prompt_response = st.text_area(translate_text("Enter your response to the prompt", st.session_state.language), key=f"prompt_response_phase3_{prompt['scenario']}")

    num_responses = len(st.session_state.phase_3_responses)
    st.info(f"{translate_text('You have input', st.session_state.language)} {num_responses} {translate_text('inputs.', st.session_state.language)}")
    st.info(f"{translate_text('You have', st.session_state.language)} {5 - num_responses} {translate_text('inputs left.', st.session_state.language)}")

    if st.button(translate_text('Next Scenario (Phase 3)', st.session_state.language)):
        st.session_state.phase_3_responses.append({
            'user': st.session_state.user['username'],
            'scenario': prompt['scenario'],
            'prompt_question': prompt_question,
            'prompt_response': prompt_response,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        if st.session_state.current_phase_3_index < len(st.session_state.phase_3_prompts) - 1:
            st.session_state.current_phase_3_index += 1
        else:
            save_to_firebase(st.session_state.phase_3_responses, "Phase_3")
            st.success(translate_text("Thank you for completing all scenarios", st.session_state.language))
            st.session_state.page = 'completed'

    feedback = st.text_area(translate_text("General feedback on the scenarios", st.session_state.language))
    satisfaction = st.slider(translate_text("Overall satisfaction with the process", st.session_state.language), 1, 5, 3)

    if st.button(translate_text("Submit Feedback", st.session_state.language)):
        feedback_data = {
            'user': st.session_state.user['username'],
            'phase': 'Phase 3',
            'feedback': feedback,
            'satisfaction': satisfaction,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_to_firebase(feedback_data, "Feedback")
        st.success(translate_text("Thank you for your feedback", st.session_state.language))

# Navigation and session state management
if 'page' not in st.session_state:
    st.session_state.page = 'sign_up'

st.sidebar.button(translate_text("Sign Up", st.session_state.language), on_click=lambda: st.session_state.update({"page": "sign_up"}), key="sidebar_sign_up_button")
st.sidebar.button(translate_text("Go to Phase 1", st.session_state.language), on_click=lambda: st.session_state.update({"page": "phase_1"}), key="sidebar_phase_1_button")
st.sidebar.button(translate_text("Go to Phase 2", st.session_state.language), on_click=lambda: st.session_state.update({"page": "phase_2"}), key="sidebar_phase_2_button")
st.sidebar.button(translate_text("Go to Phase 3", st.session_state.language), on_click=lambda: st.session_state.update({"page": "phase_3"}), key="sidebar_phase_3_button")

if st.session_state.page == 'sign_up':
    render_sign_up()
elif st.session_state.page == 'phase_1':
    render_phase_1()
elif st.session_state.page == 'phase_2':
    render_phase_2()
elif st.session_state.page == 'phase_3':
    render_phase_3()
else:
    st.write(translate_text("Thank you for participating in the study!", st.session_state.language))

