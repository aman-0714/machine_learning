import streamlit as st
import pickle
import pandas as pd

# Load the trained model pipeline
pipe = pickle.load(open('pipe_01.pkl', 'rb'))  # updated file path

# Define team and city options
teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
    'England', 'West Indies', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 'London',
    'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 'St Lucia', 'Wellington',
    'Lauderhill', 'Hamilton', 'Centurion', 'Manchester', 'Abu Dhabi', 'Mumbai',
    'Nottingham', 'Southampton', 'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore',
    'Delhi', 'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff',
    'Christchurch', 'Trinidad'
]

# Streamlit app title
st.title('🏏 International Cricket Score Predictor')

# Select teams
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

# Select city
city = st.selectbox('Select Match Venue', sorted(cities))

# Match details
col3, col4, col5 = st.columns(3)
with col3:
    current_score = st.number_input('Current Score', min_value=0)
with col4:
    overs = st.number_input('Overs Completed (Must be > 5)', min_value=0.0, max_value=20.0, step=0.1)
with col5:
    wickets = st.number_input('Wickets Lost', min_value=0, max_value=10)

# Runs in last 5 overs
last_five = st.number_input('Runs Scored in Last 5 Overs', min_value=0)

# Predict when button is clicked
if st.button('Predict Score'):

    if overs < 5:
        st.warning("⚠️ Please enter more than 5 overs for accurate predictions.")
    elif batting_team == bowling_team:
        st.warning("⚠️ Batting and Bowling teams cannot be the same.")
    else:
        # Feature engineering
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs if overs > 0 else 0

        # Create input dataframe
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'current_score': [current_score],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
            'last_five': [last_five]
        })

        # Make prediction
        result = pipe.predict(input_df)[0]
        st.success(f"🏁 Predicted Final Score: {int(result)} runs")
