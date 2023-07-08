import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="startup analysis")
df = pd.read_csv('startup_funding1.csv')
df['date'] = pd.to_datetime(df['date'], errors="coerce")
df['year']=df['date'].dt.year
st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select Option", ['Overall analysis', 'Startup', 'Investor'])

def showoverall():
    st.title('Overall Analysis')
    st.markdown('---')
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total Amount',str(round(df['amount'].sum()))+' CR')
    with col2:
        st.metric('Max Amount',str(df.groupby('startup')['amount'].max().sort_values(ascending=False).values[0])+" CR")
    with col3:
        st.metric('Average Amount',str(round(df['amount'].mean()))+" CR")
    with col4:
        st.metric('Funded Startup',df['startup'].nunique())
    st.markdown('---')
    df['month'] = df['date'].dt.month
    option=st.selectbox('Show by',['count','amount'])
    if option=="count":
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        temp_df['x-axis'] = temp_df['year'].astype('str') + '-' + temp_df['month'].astype('str')
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig5,ax5=plt.subplots()
    ax5.plot(temp_df['x-axis'],temp_df['amount'])
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.xticks(fontsize=4)
    col5,col6=st.columns(2)
    with col5:
        st.pyplot(fig5)

def show_investor_details(investor):
    st.header(f"{investor}")
    recent_investments = df[df['investors'].str.contains(investor)].head(5)
    st.subheader('Most Recent Investments')
    st.dataframe(recent_investments)
    st.subheader('Biggest Investments')
    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
        ascending=False).head()
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(big_series)
    fig, ax = plt.subplots()
    ax.bar(big_series.index, big_series.values)
    with col2:
        st.pyplot(fig)
    col3, col4 = st.columns(2)
    with col3:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        fig1, ax1 = plt.subplots()
        st.subheader('Sectors Invested in')
        ax1.pie(vertical_series, labels=vertical_series.index)
        st.pyplot(fig1)
    with col4:
        st.subheader('Generally Invests at Stage')
        stage_series = df[df['investors'].str.contains(investor)].groupby('type')['amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_series, labels=stage_series.index)
        st.pyplot(fig2)
    col5, col6 = st.columns(2)
    city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
    fig3, ax3 = plt.subplots()
    ax3.pie(city_series, labels=city_series.index)
    with col5:
        st.subheader('Total investment by city')
        st.pyplot(fig3)
    with col6:
        st.subheader('YoY Graph')
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)
        st.pyplot(fig4)
    st.subheader('Similar Investors')
    most_invested_vertical=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(
        1).index[0]
    temp_df = df.groupby(['investors', 'vertical'])['amount'].sum().sort_values(
        ascending=False).reset_index().drop_duplicates(subset=['investors'])
    similar_investors_df=temp_df[temp_df['vertical'] == most_invested_vertical].head(5)['investors'].reset_index(drop=True)
    st.dataframe(similar_investors_df)



if option == "Overall analysis":
    showoverall()
elif option == "Startup":
    name = st.sidebar.selectbox("Select Startup", sorted(df['startup'].unique()))
    st.title('Startup Analysis')
elif option == 'Investor':
    investor = st.sidebar.selectbox("Select Investor", sorted(set(df['investors'].str.split(',').sum())))
    show_investor_details(investor)
