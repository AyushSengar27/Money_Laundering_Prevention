from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import streamlit as st

# Assuming `predict` and `start_model_training` are defined in 'src.main'
from src.main import predict, start_model_training

# Initialize session state for showing the welcome message
if 'show_welcome' not in st.session_state:
    st.session_state['show_welcome'] = True

st.set_page_config('Prevention System', '🎲', initial_sidebar_state='collapsed')

# Simple CSS for animation and welcome message
st.markdown('''
    <style>
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    @keyframes moneyFlow {
        0% {transform: translateX(-100px); opacity: 0;}
        50% {opacity: 1;}
        100% {transform: translateX(100px); opacity: 0;}
    }
    .welcome-message {
        animation: fadeIn 2s;
        border: 2px solid #4CAF50;
        padding: 10px;
        margin: 10px 0;
        border-radius: 15px;
        color: #4CAF50;
        text-align: center;
    }
    .money-flow-icon {
        display: inline-block;
        animation: moneyFlow 5s infinite;
        font-size: 24px;
        color: #FFC107;
    }
    </style>
    <h2 style="color: #4CAF50;" align=center>Money Laundering Prevention System</h2>
    <div class="welcome-message">
        <span class="money-flow-icon">💸</span>
        <strong>Welcome to the Money Laundering Prevention System!</strong><br>
        This advanced tool leverages state-of-the-art algorithms to monitor, analyze, and flag suspicious transactions. By scrutinizing patterns and behaviors that deviate from the norm, it aids financial institutions in combating the complex challenge of money laundering, ensuring compliance and safeguarding the integrity of financial systems.
        <span class="money-flow-icon">🛡️</span>
    </div>
''', unsafe_allow_html=True)


# Display welcome message if it's the user's first visit
if st.session_state['show_welcome']:
    st.markdown('''
        <div class="welcome-message">
            <strong>Welcome to the Money Laundering Prevention System!</strong><br>
            This system helps in identifying and preventing money laundering activities. Navigate through the sidebar to start.
        </div>
    ''', unsafe_allow_html=True)
    
    st.session_state['show_welcome'] = False

video_url = 'https://www.youtube.com/watch?v=vc5jhmyCruE'  
st.video(video_url)

@dataclass
class BaseDF:
    sourceid: int
    destinationid: int
    amountofmoney: int
    month: int
    typeofaction: str
    typeoffraud: str

    def __iter__(self):
        yield 'sourceid', self.sourceid
        yield 'destinationid', self.destinationid
        yield 'amountofmoney', self.amountofmoney
        yield 'month', self.month
        yield 'typeofaction', self.typeofaction
        yield 'typeoffraud', self.typeoffraud

# Global Variables
msg = st.empty()
base = None

# Sidebar
with st.sidebar:
    option = st.selectbox(
        'Prediction Type',
        ['Prediction from Form', 'Batch Prediction'],
        disabled=True,  # You might want to enable this by removing or changing the condition based on your app logic
    )

# Two different form declaration
if option == 'Prediction from Form':
    with st.form('prediction-from-form'):
        sourceid = int(st.number_input('Source ID', format='%d', value=30105))
        destinationid = int(st.number_input('Destination ID', format='%d', value=8692))
        amountofmoney = int(st.number_input('Amount of Money', format='%d', value=494528))
        month = int(st.number_input('Month of transaction', format='%d', value=5))
        typeofaction = str(st.selectbox('Type of Action', ['cash-in', 'transfer']))
        typeoffraud = str(st.selectbox('Type of Fraud', ['type1', 'type2', 'type3', 'none']))

        if st.form_submit_button():
            base = BaseDF(sourceid, destinationid, amountofmoney, month, typeofaction, typeoffraud)


# Process after getting the `base` DataFrame
if base is not None and isinstance(base, BaseDF):
    df = pd.DataFrame([dict(base)])
    try:
        _, prediction = predict(df)
    except FileNotFoundError:
        msg.error('Error')
        st.stop()
    else:
        result, color = ('Fraud', 'red') if prediction == 1 else ('Not Fraud', 'green')
        st.markdown(f'<h3 style="color: {color};">{result}.</h3>', unsafe_allow_html=True)
elif base is not None and isinstance(base, pd.DataFrame):
    df = base
    try:
        pred_df, _ = predict(df)
    except FileNotFoundError:
        msg.error('Model is not trained yet')
        st.stop()
    else:
        st.balloons()
        msg.success('Download the predicted data file.')
        st.download_button(
            label='Download Prediction DataFrame',
            data=pred_df.to_csv(index=False),
            file_name='Money-Laundering-Prediction.csv',
            mime='text/csv',
        )
else:
    st.markdown('<h3 align=center>Submit.</h3>', unsafe_allow_html=True)
