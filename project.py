import json
from datetime import datetime
import streamlit as st
import ollama
import random

# Fictif names list
FIRST_NAMES = ["Stephen", "Lebron", "Victor", "Kevin", "James", "Jason", "Kyrie", "Jon", "Stipe", "Khabib", "Conor", "Kamaru"]
LAST_NAMES = ["Curry", "James", "Wembanyama", "Durant", "Harden", "Tatum", "Irving", "Jones", "Miocic", "Nurmagomedov", "McGregor", "Usman"]

# Dictionnary to store author_id -> author_name associations
AUTHOR_ID_TO_NAME = {}

def generate_fake_name():
    return f"{random.choice(FIRST_NAMES) + ' ' + random.choice(LAST_NAMES)}"

def create_author_mapping(data):
    author_ids = set()

    for obj in data['data']['sources']:
        for source in obj.get('comments', []) + obj.get('classifications', []):
            author_id = source.get('author_id')
            author_name = source.get('author_name')
            
            if author_id:
                author_ids.add(author_id)
            
            if author_name and author_id not in AUTHOR_ID_TO_NAME:
                AUTHOR_ID_TO_NAME[author_id] = author_name

    for author_id in author_ids:
        if author_id not in AUTHOR_ID_TO_NAME:
            AUTHOR_ID_TO_NAME[author_id] = generate_fake_name()

    return AUTHOR_ID_TO_NAME

# Load the JSON file
with open('rcf_sample_sources.json', 'r') as file:
    data = json.load(file)

# Create the author mapping
AUTHOR_ID_TO_NAME = create_author_mapping(data)

# Extract unique group names
unique_groups = list(set(group['name'] for obj in data['data']['sources'] for group in obj['groups']))

# Function to clean and prepare data
def clean_data(obj):
    # Find most recent redshift value
    if obj.get('redshift_history'):
        latest_redshift = max(
            obj['redshift_history'],
            key=lambda x: datetime.fromisoformat(x['set_at_utc'].replace('Z', ''))
        )
        redshift_value = latest_redshift['value']
    else:
        redshift_value = obj.get('redshift', None)

    # Mark the classifications generated by ML
    classifications = [
        {
            'classification': c['classification'],
            'probability': c.get('probability', None),
            'author_name': AUTHOR_ID_TO_NAME.get(c.get('author_id'), 'Unknown'),
            'ml_generated': c['ml']
        }
        for c in obj.get('classifications', [])
    ]

    # Mark the comments generated by bots
    comments = [
        {
            'author_id': c['author_id'],
            'text': c['text'],
            'created_at': c['created_at'],
            'bot_generated': c['bot'],
            'author_name': AUTHOR_ID_TO_NAME.get(c['author_id'], 'Unknown')
        }
        for c in obj.get('comments', [])
    ]

    cleaned_obj = {
        'id': obj['id'],
        'RA/Dec': f"{obj['ra']}, {obj['dec']}",
        'redshift': redshift_value,
        'tns_name': obj.get('tns_name', 'N/A'),
        'classifications': classifications,
        'comments': comments,
        'groups': [group['name'] for group in obj['groups']],
        'host': obj.get('host', 'Unknown'),
        'host_offset': obj.get('host_offset', 'N/A'),
        'gal_lon': obj.get('gal_lon', None),
        'gal_lat': obj.get('gal_lat', None),
        'luminosity_distance': obj.get('luminosity_distance', 'N/A'),
        'dm': obj.get('dm', 'N/A'),
        'angular_diameter_distance': obj.get('angular_diameter_distance', 'N/A'),
        'thumbnails': [thumbnail['public_url'] for thumbnail in obj.get('thumbnails', [])]
    }

    return cleaned_obj


# Clean the data for all objects
cleaned_objects = [clean_data(obj) for obj in data['data']['sources']]

# Function to create a prompt for Ollama
def create_prompt(obj):
    classifications_str = ', '.join([
        f"{c['classification']} (ML-generated)" if c['ml_generated'] else f"{c['classification']} by {c['author_name']}"
        for c in obj['classifications']
    ]) if obj['classifications'] else 'None'

    comments_str = ', '.join([
        f"{comment['text']} (Bot-generated)" if comment['bot_generated'] else f"{comment['text']} by {comment['author_name']}"
        for comment in obj['comments'] if comment['text']
    ]) if obj['comments'] else 'None'

    data_block = f"""
    Object Name: {obj['tns_name'] or 'N/A'}
    Position: {obj['RA/Dec']}
    Redshift: {obj['redshift'] or 'None'}
    Classification: {classifications_str}
    Key Comments: {comments_str}
    Thumbnail URLs: {', '.join(obj['thumbnails']) if obj['thumbnails'] else 'None'}
    """

    prompt = f"""
    Summarize the following data on astronomical transients observed on 16/05/2021 for an experienced astronomer audience.
    Provide the object name, position, redshift, classification, and summarize key actions such as spectra taken,
    comments of interest, or significant classifications. About the comment and classification data: put them only if they are not empty.
    Highlight the names of the authors of the comments or classifications like : (by Author Name).
    Indicate clearly when the classification or comment was done by a bot or by ML pipelines.
    Provide the thumbnail URLs for reference.
    Use a formal tone.

    Data: {data_block}
    """
    return prompt



# Function to generate a summary using Ollama
def generate_summary(prompt):
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        return response['message']['content']
    except Exception as e:
        return f"Error generating summary: {e}"

# Streamlit interface
st.title("Daily Summaries of Astronomical Actions")
st.write("Select a group and an object by TNS Name to view the summary.")

# Add a dropdown menu to select the group
selected_group = st.selectbox("Select a group", unique_groups)

# Filter objects based on the selected group
filtered_objects = [obj for obj in cleaned_objects if selected_group in obj['groups']]

# Add a selectbox to choose the object by tns_name
tns_names = [obj['tns_name'] for obj in filtered_objects if obj['tns_name'] != 'N/A']
selected_tns_name = st.selectbox("Select an object by TNS Name", tns_names)

# Validate button to generate the summary
validate_button = st.button("Generate Summary")

timer = st.empty()
start_time = datetime.now()

# Generate and display the summary for the selected object
if validate_button:
    selected_obj = next((obj for obj in filtered_objects if obj['tns_name'] == selected_tns_name), None)
    if selected_obj:
        with st.spinner("Generating summary..."):
            prompt = create_prompt(selected_obj)
            summary = generate_summary(prompt)
            st.subheader(f"Summary for Object {selected_tns_name}")
            # Display the time taken to generate the summary
            timer.write(f"Time taken to generate summary: {datetime.now() - start_time}")
            st.write(summary)
    else:
        st.write("Selected object not found.")