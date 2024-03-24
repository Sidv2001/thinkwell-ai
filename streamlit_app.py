import streamlit as st
from anthropic import Anthropic
import re
import os

# Assuming you have the OPENAI_API_KEY set in your Streamlit secrets
client = Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"],
)

# Hardcoded user credentials (use environment variables or a more secure method in production)
USER_ID = "admin"
PASSWORD = "password"

files_dir = "data"

module_texts = {}


filenames = [
    "Module - 2 Non specific factors (therapeutic relationship).txt",
    "Module 1- Intro to cbt.txt",
    "Module 4 - Case Conceptualization.txt",
    "Module 5- Orienting the Paitent to CBT.txt",
    "Module 6 - Goal Setting.txt",
    "Module 7 - Agenda Setting.txt",
    "Module 9 - Identifying Maladaptive Thoughts and Beliefs.txt",
    "Module 10- Challenging Maladaptive thoughts and Beliefs.txt",
    "Module 11- behavioral Activation.txt",
    "Module 12 - Problem Solving.txt",
    "Module 13 - Relaxation.txt",
]

# Adjust extraction logic and re-process files
for filename in filenames:
    # Extract module number more accurately
    # This regex captures digits following the word "Module" taking into account possible variations in naming
    match = re.search(r"Module\s*[-\s]\s*(\d+)", filename, re.IGNORECASE)
    if match:
        module_number = match.group(1)
    else:
        module_number = "Unknown"

    # Full path to the file
    file_path = os.path.join(files_dir, filename)

    # Read RTF content again
    with open(file_path, "r", encoding="utf-16") as file:
        txt_content = file.read()
    # Store the corrected text content in the dictionary
    module_texts[module_number] = txt_content
file_path = os.path.join(files_dir, "Plan Examples.txt")
# Read RTF content again
with open(file_path, "r", encoding="utf-16") as file:
    txt_content = file.read()
module_texts["Plan Examples"] = txt_content


def ordinal(number):
    """
    Convert an integer into its ordinal representation.
    """
    # Determine the suffix to use based on English grammar rules
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    # Check for 11-13 because they follow different rule patterns
    if 10 <= number % 100 <= 13:
        suffix = "th"
    else:
        # Numbers ending in 1, 2, or 3 will use the corresponding suffix from the dictionary
        suffix = suffixes.get(number % 10, "th")
    return f"{number}{suffix}"


def string_to_dict(s):
    """
    Convert a string representation of a dictionary back into a Python dictionary.

    Parameters:
    s (str): The string representation of the dictionary.

    Returns:
    dict: The Python dictionary obtained from the string.
    """
    # Using eval with caution, considering it can execute arbitrary code.
    # It's assumed the input is trusted. For untrusted input, a safer parsing method should be used.
    return eval(s)


def dict_to_string(d):
    """
    Convert a dictionary into a string where each key-value pair is separated by a colon
    and each pair is on a new line.

    Parameters:
    d (dict): The dictionary to convert.

    Returns:
    str: The string representation of the dictionary with key-value pairs.
    """
    return "\n".join([f"{key}: {value}" for key, value in d.items()])


def list_of_dicts_to_string(lst):
    """
    Convert a list of dictionaries into a string in the same format as Python's print, except with a new line
    between each element of the list.

    Parameters:
    lst (list): The list of dictionaries to convert.

    Returns:
    str: The string representation of the list with each dictionary on a new line.
    """
    return "[\n" + ",\n".join([str(d) for d in lst]) + "\n]"


def list_of_lists_of_dicts_to_string_with_keys(lst_of_lst):
    """
    Convert a list of lists of dictionaries into a string, applying list_of_dicts_to_string to each list in the
    original list. Instead of adding list brackets next to each list, add a key titled 'session i' where i is the
    position of the list in the overarching list plus 1.

    Parameters:
    lst_of_lst (list): The list of lists of dictionaries to convert.

    Returns:
    str: The string representation with each list of dictionaries under a 'session i' key.
    """
    # Create a string representation with 'session i' keys
    sessions_str = ",\n".join(
        [
            f"'session {i+1}': {list_of_dicts_to_string(lst)}"
            for i, lst in enumerate(lst_of_lst)
        ]
    )
    return "{\n" + sessions_str + "\n}"


def initiate_session_1():
    """
    This function is for starting session 1 of the therapy.
    """
    return (
        f"In this scenario, you are going to be a therapist performing Cognitive Behavioral Therapy (CBT) to help the patient. "
        f"I have attached an educational module detailing what CBT is and how to work with it from the perspective of a therapist: "
        f"{module_texts['1']} "
        "You have just met the patient and need to understand why they came for therapy and construct a case. "
        f"I have attached another module on Case Conceptualization and Treatment Planning for CBT: "
        f"{module_texts['4']} "
        "Keep in mind that the effectiveness of therapy is often based on Non-Specific factors such as a strong Therapeutic Relationship. "
        f"I have attached a module on navigating this as well. "
        f"{module_texts['2']} "
        "Additionally, I have added documentation about the different aspects and techniques of CBT for you to use when planning out what you are going to say: "
        f"Module 5 Orienting the Paitent to CBT: {module_texts['5']},\n Module 6 Goal Setting: {module_texts['6']},\n Module 7 Agenda Setting: {module_texts['7']},\n Module 9 Identifying Maladaptive Thoughts and Beliefs: {module_texts['9']}"
        f",\n Module 10 Challenging Maladaptive thoughts and Beliefs: {module_texts['10']},\n Module 11 Behavioral Activation: {module_texts['11']},\n Module 12 Problem Solving: {module_texts['12']},\n Module 13 Relaxation: {module_texts['13']} "
        "You are now going to initiate a conversation with the patient. Generate an opening introduction to both yourself "
        "(you are an AI therapist) and a brief introduction to CBT and ask the user to then introduce themselves and why they have come for therapy."
        "Remember you are having a conversation with the patient. You are the therapist and should behave like the therapist. You are meeting the patient for the first time and need to introduce yourself and get started with the session."
        "Do not add comments describing what you are going to say. Just say it. Additionally this is an over text therapy session. Do not type out gestures such as 'clears throat' because a human would not do that in a text chat."
        "Finally you are a therapist and your name is Thinkwell"
    )


def continue_session_1(user_prompt, transcript):
    """
    This function continues session 1 of the therapy after it has started.
    """
    return (
        f"In this scenario, you are currently a therapist performing Cognitive Behavioral Therapy (CBT) to help a patient. "
        f"I have attached an educational module detailing what CBT is and how to work with it from the perspective of a therapist: "
        f"{module_texts['1']} "
        "You currently talking to the patient and need to understand why they came for therapy and construct a case. "
        f"I have attached another module on Case Conceptualization and Treatment Planning for CBT: "
        f"{module_texts['4']} "
        "Your goal is to get a deeper understanding of the patient's problems using the guidelines in the documents attached above, while also answering any questions the patient might have about CBT. "
        "However, try to keep the patient on track with regard to giving more details about their situation. "
        "Keep in mind that the effectiveness of therapy is often based on Non-Specific factors such as a strong Therapeutic Relationship. "
        f"I have attached a module on navigating this as well. "
        f"{module_texts['2']} "
        "Additionally, I have added documentation about the different aspects and techniques of CBT for you to use when planning out what you are going to say: "
        f"Module 5 Orienting the Paitent to CBT: {module_texts['5']},\n Module 6 Goal Setting: {module_texts['6']},\n Module 7 Agenda Setting: {module_texts['7']},\n Module 9 Identifying Maladaptive Thoughts and Beliefs: {module_texts['9']}"
        f",\n Module 10 Challenging Maladaptive thoughts and Beliefs: {module_texts['10']},\n Module 11 Behavioral Activation: {module_texts['11']},\n Module 12 Problem Solving: {module_texts['12']},\n Module 13 Relaxation: {module_texts['13']} "
        "You are currently chatting with the patient and attached is the transcript of the conversation that has happened in the past. "
        f"{transcript} "
        f"This is what the patient has just said: "
        f"{user_prompt} "
        "Construct a response that achieves the goals described above as well as the goals of the initial session of cognitive behavioral therapy that also maintains the flow of conversation with the patient. Use the documentation about CBT techniques to determine what you should say to achieve the goals of the session, and help the patient. When you believe you have collected the information needed to construct your case, or if the patient needs to leave, you can start bringing the conversation to a natural end and ask the patient if they have any feedback on the process."
        "Remember you are having a conversation with the patient. You are the therapist and should behave like the therapist. "
        "Do not add comments describing what you are going to say. Just say it. Additionally this is an over text therapy session do not type out actions people might do while talking, such as clears throat."
        "Finally you are a therapist and your name is Thinkwell"
    )


def end_session_1(transcript):
    """
    This function ends session 1 of the therapy, constructs a case summary and a plan for the next sessions.
    """
    return (
        "In this scenario, you are currently a therapist performing Cognitive Behavioral Therapy (CBT) to help a patient. "
        "I have attached an educational module detailing what CBT is and how to work with it from the perspective of a therapist: "
        f"{module_texts['1']} "
        "You were just talking to the patient intending to understand why they came for therapy and construct a case. "
        "I have attached another module on Case Conceptualization and Treatment Planning for CBT: "
        f"{module_texts['4']} "
        "Additionally, to assist you with your tasks, we have provided you with all the documentation about the different CBT techniques below: "
        f"Module 5 Orienting the Paitent to CBT: {module_texts['5']},\n Module 6 Goal Setting: {module_texts['6']},\n Module 7 Agenda Setting: {module_texts['7']},\n Module 9 Identifying Maladaptive Thoughts and Beliefs: {module_texts['9']}"
        f",\n Module 10 Challenging Maladaptive thoughts and Beliefs: {module_texts['10']},\n Module 11 Behavioral Activation: {module_texts['11']},\n Module 12 Problem Solving: {module_texts['12']},\n Module 13 Relaxation: {module_texts['13']} "
        "You have just finished your first session with the user. Attached is the transcript from this conversation. "
        f"{transcript} "
        "Now you need to do the following things: "
        "1. Construct a case summary of the patient based on this transcript based on the guidelines from the CBT documentation provided. "
        "2. Based on the case, construct a plan for the next 7 sessions taking into account the different techniques available in CBT as well as the guidelines for what these sessions should look like. "
        "For the second task, we have additionally given you 2 different examples as to how such a plan can be created: "
        f"{module_texts['Plan Examples']} "
        "Fill this information out into a JSON in the following format: "
        '{"Case Summary": "<Case Summary from Part 1>", "Session Plan": "<Plan for the next 7 sessions from Part 2>"}'
    )


def start_followup_session(session_results, previous_transcripts):
    """
    Starts a follow-up therapy session after the first one.
    """
    session_id = st.session_state["session_id"]
    return (
        "In this scenario, you are going to be a therapist performing Cognitive Behavioral Therapy (CBT) to help the patient. "
        f"I have attached an educational module detailing what CBT is and how to work with it from the perspective of a therapist: "
        f"{module_texts['1']} "
        f"You have met the patient in the past and this is now your {ordinal(session_id)} session with the patient. "
        f"Attached is the transcripts from the previous sessions: {list_of_lists_of_dicts_to_string_with_keys(previous_transcripts)} "
        "In the previous sessions, you have iterated on a case summary and plan for the upcoming sessions. "
        "Attached are the patient case summary and your plan for this and future sessions. "
        f"Document: \n {session_results} "
        f"I have attached another module on Case Conceptualization and Treatment Planning for CBT to help you interpret this: "
        f"{module_texts['4']} "
        "Keep in mind that the effectiveness of therapy is often based on Non-Specific factors such as a strong Therapeutic Relationship. "
        f"I have attached a module on navigating this as well. {module_texts['2']} "
        "Additionally, I have added documentation about the different aspects and techniques of CBT for you to use when planning out what you are going to say: "
        f"Module 5 Orienting the Paitent to CBT: {module_texts['5']},\n Module 6 Goal Setting: {module_texts['6']},\n Module 7 Agenda Setting: {module_texts['7']},\n Module 9 Identifying Maladaptive Thoughts and Beliefs: {module_texts['9']}"
        f",\n Module 10 Challenging Maladaptive thoughts and Beliefs: {module_texts['10']},\n Module 11 Behavioral Activation: {module_texts['11']},\n Module 12 Problem Solving: {module_texts['12']},\n Module 13 Relaxation: {module_texts['13']} "
        "You are now going to initiate a conversation with the patient to start this session given the context from the previous sessions. "
        f"Module 7 on the agenda setting is a good reference to use to decide how to start the session. {module_texts['7']}"
        "Remember you are having a conversation with the patient. You are the therapist and should behave like the therapist. "
        "Do not add comments describing what you are going to say. Just say it. Additionally this is an over text therapy session do not type out actions people might do while talking, such as clears throat."
        "Finally you are a therapist and your name is Thinkwell"
    )


def continue_followup_session(
    user_response, transcript, session_results, previous_transcripts
):
    """
    Continues the conversation in a follow-up therapy session.
    """
    session_id = st.session_state["session_id"]
    return (
        "In this scenario, you are going to be a therapist performing Cognitive Behavioral Therapy (CBT) to help the patient. "
        f"I have attached an educational module detailing what CBT is and how to work with it from the perspective of a therapist: "
        f"{module_texts['1']} "
        f"You have met the patient in the past and this is now your {ordinal(session_id)} session with the patient. "
        f"Attached are the transcripts from the previous sessions: {list_of_lists_of_dicts_to_string_with_keys(previous_transcripts)} "
        "In the previous sessions, you have iterated on a case summary and plan for the upcoming sessions. "
        "Attached are the patient case summary and your plan for this and future sessions. "
        f"Document: \n {session_results} "
        f"I have attached another module on Case Conceptualization and Treatment Planning for CBT to help you interpret this: "
        f"{module_texts['4']} "
        "Keep in mind that the effectiveness of therapy is often based on Non-Specific factors such as a strong Therapeutic Relationship. "
        f"I have attached a module on navigating this as well. {module_texts['2']} "
        "Additionally, I have added documentation about the different aspects and techniques of CBT for you to use when planning out what you are going to say: "
        f"Module 5 Orienting the Paitent to CBT: {module_texts['5']},\n Module 6 Goal Setting: {module_texts['6']},\n Module 7 Agenda Setting: {module_texts['7']},\n Module 9 Identifying Maladaptive Thoughts and Beliefs: {module_texts['9']}"
        f",\n Module 10 Challenging Maladaptive thoughts and Beliefs: {module_texts['10']},\n Module 11 Behavioral Activation: {module_texts['11']},\n Module 12 Problem Solving: {module_texts['12']},\n Module 13 Relaxation: {module_texts['13']} "
        "You are currently chatting with the patient and attached is the transcript of the conversation for this session. "
        f"{transcript} "
        f"This is what the patient has just said: "
        f"{user_response} "
        "Construct a response that achieves the goals described in the session plan for this particular session (session {session_id}) "
        "that also maintains the flow of conversation with the patient. Use the documentation about CBT techniques to determine what you should say to achieve the goals of the session, and help the patient."
        "Remember you are having a conversation with the patient. You are the therapist and should behave like the therapist. "
        "Do not add comments describing what you are going to say. Just say it. Additionally this is an over text therapy session do not type out actions people might do while talking, such as clears throat."
        "Finally you are a therapist and your name is Thinkwell"
    )


def end_followup_session(transcript, session_results, previous_transcripts):
    """
    Ends a follow-up therapy session, updates the case summary and the session plan based on the new information from the session.
    """
    # Retrieve the session ID from the session state
    session_id = st.session_state["session_id"]

    # Determine the number of sessions left after this one
    remaining_sessions = 8 - session_id

    # Construct the end of session text
    end_session_text = (
        "In this scenario, you are currently a therapist performing Cognitive Behavioral Therapy (CBT) to help a patient. "
        f"I have attached an educational module detailing what CBT is and how to work with it from the perspective of a therapist: {module_texts['1']} "
        f"You have met the patient in the past and this is now your {ordinal(session_id)} session with the patient. "
        "You have just finished talking to the patient."
        f"Attached is the transcripts from the previous sessions: {list_of_lists_of_dicts_to_string_with_keys(previous_transcripts)} "
        "In the previous sessions, you have iterated on a case summary and plan for the upcoming sessions. "
        "Attached are the patient case summary and your plan for this and future sessions: "
        f"\n {dict_to_string(session_results)} "
        f"I have attached another module on Case Conceptualization and Treatment Planning for CBT to help you interpret this and as a reference for your future tasks: {module_texts['4']} "
        "Additionally, to assist you with your tasks we have provided you with all the documentation about the different CBT techniques below: "
        f"Module 5 Orienting the Paitent to CBT: {module_texts['5']},\n Module 6 Goal Setting: {module_texts['6']},\n Module 7 Agenda Setting: {module_texts['7']},\n Module 9 Identifying Maladaptive Thoughts and Beliefs: {module_texts['9']}"
        f",\n Module 10 Challenging Maladaptive thoughts and Beliefs: {module_texts['10']},\n Module 11 Behavioral Activation: {module_texts['11']},\n Module 12 Problem Solving: {module_texts['12']},\n Module 13 Relaxation: {module_texts['13']} "
        f"You have just finished your {session_id}th session with the user. Attached is the transcript from this conversation: {transcript} "
        "Now you need to do the following things:\n"
        "1. Update the current case summary of the patient based on whatever has happened in this session to include any new information unearthed in this session. \n"
        f"2. Based on the updated case, update your plan for the next {remaining_sessions} sessions (session {session_id + 1} to session 8) taking into account the different techniques available in CBT as well as the guidelines for what these sessions should look like. "
        f"For the second task, we have additionally given you 2 different examples of how such a plan can be designed: {module_texts['Plan Examples']} "
        "Generate the results for the following tasks this information out into a JSON in the following format: "
        '{"Case Summary": "<Case Summary from Part 1>", "Session Plan": "<Plan for the next {remaining_sessions} sessions from Part 2>"}'
    )

    # Here you would implement the logic to generate the updated case summary and session plan.
    # The placeholders "<Case Summary from Part 1>" and "<Plan for the next {remaining_sessions} sessions from Part 2>"
    # would be replaced with the actual summaries.

    # Return the end of session text
    return end_session_text


# --------------------------------------------------------------Streamlit here---------------------


def login_page():
    st.title("Login Page")
    user_id = st.text_input("User ID", value="", max_chars=50)
    password = st.text_input("Password", value="", type="password", max_chars=50)

    if st.button("Login"):
        if user_id == USER_ID and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.session_state["session_id"] += 1
            st.rerun()
        else:
            st.error("Incorrect User ID or Password")


def chat_interface():
    st.title("Thinkwell-AI" + str(st.session_state["session_id"]))

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_results" not in st.session_state:
        st.session_state.session_results = ""
    if "previous_transcripts" not in st.session_state:
        st.session_state.previous_transcripts = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if st.session_state.messages == []:
        with st.chat_message("assistant"):
            if st.session_state["session_id"] == 1:
                init_prompt = initiate_session_1()
            else:
                init_prompt = start_followup_session(
                    st.session_state.session_results,
                    st.session_state.previous_transcripts,
                )
            with client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": init_prompt}],
                model="claude-2.1",
            ) as stream:
                print(init_prompt)
                response = st.write_stream(stream.text_stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

    if prompt := st.chat_input("Please type in your response here"):

        with st.chat_message("user"):
            st.markdown(prompt)
        if st.session_state["session_id"] == 1:
            continue_prompt = continue_session_1(
                prompt, list_of_dicts_to_string(st.session_state.messages)
            )
        else:
            continue_prompt = continue_followup_session(
                prompt,
                list_of_dicts_to_string(st.session_state.messages),
                st.session_state.session_results,
                st.session_state.previous_transcripts,
            )

        with st.chat_message("assistant"):
            with client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": continue_prompt}],
                model="claude-2.1",
            ) as stream:
                response = st.write_stream(stream.text_stream)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})


def logout_button():
    with st.sidebar:
        if st.button("Logout"):
            # for key in list(st.session_state.keys()):
            #     del st.session_state[key]
            if st.session_state["session_id"] == 1:
                fin_prompt = end_session_1(
                    list_of_dicts_to_string(st.session_state.messages)
                )
            else:
                fin_prompt = end_followup_session(
                    list_of_dicts_to_string(st.session_state.messages),
                    st.session_state.session_results,
                    st.session_state.previous_transcripts,
                )
            res = client.messages.create(
                model="claude-2.1",
                max_tokens=1024,
                messages=[{"role": "user", "content": fin_prompt}],
            )
            st.session_state.session_results = res.content[0].text
            st.session_state.previous_transcripts = st.session_state.messages
            # print(previous_transcripts)
            # print(session_results)
            st.session_state["authenticated"] = False
            st.session_state.messages = []
            st.rerun()


def main():
    # Setup page configuration
    st.set_page_config(
        page_title="Thinkwell-AI",
        page_icon=":brain:",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "Get Help": "https://www.mentalhealth.gov/",
            "About": "This is a mental health support chat application.",
        },
    )

    # Custom background color and font color
    st.markdown(
        """
        <style>
        .stApp { background-color: #98FF98; } /* Mint green background */
        /* Font color for different elements */
        .st-af { color: #333333; } /* Primary text color */
        .st-ag { color: #606060; } /* Secondary text color, adjust as needed */
        /* You might need to inspect the page and target specific elements based on their class for more precision */
        h1, h2, h3, h4, h5, h6, p, .stTextInput>div>div>input { color: #606060; } /* Headers & text input */
        .stButton>button { color: #606060; } /* Button text */
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = 0

    if st.session_state["authenticated"]:
        chat_interface()
        logout_button()  # Moved the logout to the sidebar for logical placement
    else:
        login_page()


if __name__ == "__main__":
    main()
