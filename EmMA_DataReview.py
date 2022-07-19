# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 09:21:57 2022
Streamlit - EmMA Data Review
@author: chengh19
"""
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px

st.title('EmMA Data Review')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

#%% input text
txt = st.text_area('Description of Experiment - eLN ID', '''
     It was the best of times, it was the worst of times, it was
     the age of wisdom, it was the age of foolishness, it was
     the epoch of belief, it was the epoch of incredulity, it
     was the season of Light, it was the season of Darkness, it
     was the spring of hope, it was the winter of despair, (...)
     ''')
#st.write('Sentiment:', run_info_check(txt))

#%% plot data 
#samp_id = df['Sample_ID']
#run_id = df['MesureCount']
#eff_sig = df['EFSignal']
#eff_vol = df['EFVoltage']
#eff_cur = df['EFCurrent']

df['Run_index'] = [i+1 for i, _ in enumerate(df['EFSignal'])]  

#%% Plot: sample ID as symbol 
name_data = ['EFSignal','EFVoltage','EFCurrent']
figures = [px.scatter(df,x='Run_index',y=name_data[0],symbol='Sample_ID'),
           px.scatter(df,x='Run_index',y=name_data[1],symbol='Sample_ID'),
           px.scatter(df,x='Run_index',y=name_data[2],symbol='Sample_ID')]

fig1 = make_subplots(rows=len(figures), cols=1) 

for i, figure in enumerate(figures):
    for trace in range(len(figure["data"])):
        fig1.append_trace(figure["data"][trace], row=i+1, col=1)
fig1['layout']['yaxis1'].update(title=name_data[0]) # useful script to modify the label names
fig1['layout']['yaxis2'].update(title=name_data[1])
fig1['layout']['yaxis3'].update(title=name_data[2])
fig1['layout']['xaxis3'].update(title='Run Index')
fig1.update_layout(showlegend=False)

##%% melt the dataframe --> To be improved
#df_melt = df.melt(
#    id_vars='Run_index', 
#    value_vars=['EFSignal', 'EFVoltage', 'EFCurrent'])
#fig = px.scatter(
#    df_melt, 
#    x='Run_index', 
#    y='value',
#    facet_row='variable' 
#    )
#fig.update_yaxes(showticklabels=True, matches=None)
#fig.show()

#%% Signal recovery grouped by Sample_ID
df_norm = df.groupby('Sample_ID').transform(lambda x: (x /x.mean()))
norm_name_data = ['EFSignal_recovery','EFVoltage_recovery','EFCurrent_recovery']
df[norm_name_data[0]] = df_norm['EFSignal']
df[norm_name_data[1]] = df_norm['EFVoltage']
df[norm_name_data[2]] = df_norm['EFCurrent']

figures = [px.scatter(df,x='Run_index',y=norm_name_data[0],symbol='Sample_ID'),
           px.scatter(df,x='Run_index',y=norm_name_data[1],symbol='Sample_ID'),
           px.scatter(df,x='Run_index',y=norm_name_data[2],symbol='Sample_ID')]
fig2= make_subplots(rows=len(figures), cols=1) 

for i, figure in enumerate(figures):
    for trace in range(len(figure["data"])):
        fig2.append_trace(figure["data"][trace], row=i+1, col=1)
fig2.update_yaxes(range=[0.85,1.15])
fig2['layout']['yaxis1'].update(title=name_data[0],range=[0.85,1.15])
fig2['layout']['yaxis2'].update(title=name_data[1],range=[0.95,1.05])
fig2['layout']['yaxis3'].update(title=name_data[2],range=[0.95,1.05])
fig2['layout']['xaxis3'].update(title='Run Index')     
fig2.update_layout(showlegend=False)

if st.checkbox('Show Recovery (Group by SampleID)'):
    fig1.show()
    fig2.show()
else:
    fig1.show()

    

