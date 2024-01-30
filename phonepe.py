import os
import json
import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

st.title(":violet[PhonePe Pulse Data Visualization]")
st.markdown(":violet[Welcome to the PhonePe Pulse Dashboard ,This PhonePe Pulse Data Visualization and Exploration dashboard is a user-friendly tool designed to provide insights and information about the data in the PhonePe Pulse GitHub repository. This dashboard offers a visually appealing and interactive interface for users to explore various metrics and statistics.]")
st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

#Connection to postgres
mydab = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "harsh",
                        database = "phonepe_data",
                        port = "5432"
                        )
cursor=mydab.cursor()

#Menu creation 
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

#Menu to Home
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

#Menu to Top Charts
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users","Insurance"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """
                )

#Top Chart to Transactions
        
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
    
    
        with col1:
            st.markdown("### :violet[States]")
            cursor.execute(f"select states, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total_Transaction_Amount from aggregated_transaction where years = {Year} and quarter = {Quarter} group by states order by Total_Transaction_Amount desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Transaction_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='States',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transaction_Count'],
                                labels={'Transaction_Count':'Transaction_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select district, sum(Transaction_count) as Total_Transaction_Count, sum(Transaction_amount) as Total_Transaction_Amount from map_transaction where years = {Year} and quarter = {Quarter} group by district order by Total_Transaction_Amount desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction_count','Total_amount'])
            fig = px.pie(df, values='Total_amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transaction_count'],
                                labels={'Transaction_count':'Transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        with col3:
            st.markdown("### :violet[Pincodes]")
            cursor.execute(f"select pincodes, sum(Count) as Total_Transactions_Count, sum(Amount) as Total_Transaction_Amount from top_transaction where years = {Year} and quarter = {Quarter} group by pincodes order by Total_Transaction_Amount desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transaction_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transaction_Count'],
                                labels={'Transaction_Count':'Transaction_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

#Top to Users
            
    if Type == "Users":
            col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
            
            with col1:
                st.markdown("### :violet[Brands]")
                if Year == 2022 and Quarter in [2,3,4]:
                  st.markdown("#### No Data")
                elif Year == 2023 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
                else:
                    cursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from aggregated_user where years = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Total_Users','Avg_Percentage'])
                    fig = px.bar(df,
                                title='Top 10',
                                x="Total_Users",
                                y="Brands",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                    st.plotly_chart(fig,use_container_width=True)  

            with col2:
                st.markdown("### :violet[Districts]")
                
                cursor.execute(f"select districts, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by districts order by Total_Users desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Districts', 'Total_Users','Total_Appopens'])
                df.Total_Users = df.Total_Users.astype(float)
                fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="Districts",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)

            with col3:
                st.markdown("### :violet[Pincodes]")
                
                cursor.execute(f"select Pincodes, sum(RegisteredUser) as Total_Users from top_user where years = {Year} and quarter = {Quarter} group by Pincodes order by Total_Users desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Pincodes', 'Total_Users'])
                fig = px.pie(df,
                            values='Total_Users',
                            names='Pincodes',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
            with col4:
                st.markdown("### :violet[States]")
              
                cursor.execute(f"select states, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by states order by Total_Users desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Users','Total_Appopens'])
                fig = px.pie(df, values='Total_Users',
                                names='States',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
             
#Top charts to Insurance

    if Type == "Insurance":
            col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        
            with col1:
                st.markdown("### :violet[States]")
                if Year == 2018 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
                elif Year == 2019 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
                elif Year == 2020 and Quarter in [1]:
                    st.markdown("#### No Data")
                elif Year == 2023 and Quarter in [4]:
                        st.markdown("#### No Data")
                else:
                    cursor.execute(f"select states, sum(Insurance_count) as Total_Insurance_Count, sum(Insurance_amount) as Total_Insurance_Amount from aggregated_Insurance where years = {Year} and quarter = {Quarter} group by states order by Total_Insurance_Amount desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Insurance_count','Total_Amount'])
                    fig = px.pie(df, values='Total_Amount',
                                    names='States',
                                    title='Top 10',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Insurance_count'],
                                    labels={'Insurance_count':'Insurance_count'})
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)  

            with col2:
                st.markdown("### :violet[District]")
                if Year == 2018 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
                elif Year == 2019 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
                elif Year == 2020 and Quarter in [1]:
                    st.markdown("#### No Data")
                elif Year == 2023 and Quarter in [4]:
                        st.markdown("#### No Data")
                else:
                    cursor.execute(f"select districts , sum(Count) as Total_Count, sum(Amount) as Total from map_insurance where years = {Year} and quarter = {Quarter} group by districts order by Total desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['Districts', 'Insurance_count','Total_Amount'])

                    fig = px.pie(df, values='Total_Amount',
                                    names='Districts',
                                    title='Top 10',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Insurance_count'],
                                    labels={'Insurance_count':'Insurance_count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)

            with col3:
                st.markdown("### :violet[Pincodes]")
                if Year == 2018 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
                elif Year == 2019 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
                elif Year == 2020 and Quarter in [1]:
                    st.markdown("#### No Data")
                elif Year == 2023 and Quarter in [4]:
                        st.markdown("#### No Data")
                else:
                    cursor.execute(f"select pincodes, sum(Count) as Total_Insurance_Count, sum(Amount) as Total from top_insurance where years = {Year} and quarter = {Quarter} group by pincodes order by Total desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['Pincodes', 'Insurance_count','Total_Amount'])
                    fig = px.pie(df, values='Total_Amount',
                                    names='Pincodes',
                                    title='Top 10',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Insurance_count'],
                                    labels={'Insurance_count':'Insurance_count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)

#Menu to Explore Data
                    
if selected == "Explore Data":
    Year = st.sidebar.slider ("**Years**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider ("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox ("**Type**", ("Transactions", "Users","Insurance"))
    col1,col2 = st.columns(2)

#Explore data to Transactions
    if Type == "Transactions":
         
#Overall State Data to Transactions Amount to Indian Map
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            
            cursor.execute(f"select states, sum(transaction_count) as Total_Transaction, sum(transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['States', 'Total_Transaction', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.States = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='States',
                        color='Total_amount',
                        color_continuous_scale='sunset')


            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

# Overall State Data to TRANSACTIONS COUNT to INDIA MAP
        
        with col2:    
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            
            cursor.execute(f"select states, sum(transaction_count) as Total_Transaction, sum(transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['States', 'Total_Transaction', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transaction = df1.Total_Transaction
            df1.States = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='States',
                    color='Total_Transaction',
                    color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

# BAR CHART - TOP PAYMENT TYPE
        with col1:
            st.markdown("## :violet[Top Payment Type]")
            
            cursor.execute(f"select transaction_type, sum(transaction_count) as Total_Transaction, sum(transaction_amount) as Total_amount from aggregated_transaction where years= {Year} and quarter = {Quarter} group by transaction_type order by transaction_type")
            df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_Type', 'Total_Transaction','Total_amount'])

            fig = px.bar(df,
                        title='Transaction Types vs Total_Transaction',
                        x="Transaction_Type",
                        y="Total_Transaction",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Cividis)
            st.plotly_chart(fig,use_container_width=False)

# BAR CHART TRANSACTIONS to DISTRICT WISE DATA            
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("## :violet[Select any State to explore more]")
            selected_state = st.selectbox("",
                                  ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa',
                                   'Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka', 'Kerala','Ladakh','Lakshadweep', 'Madhya Pradesh', 'Maharashtra','Manipur',
                                   'Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttarkhand','Uttar Pradesh','West Bengal'),index=30)
            
            cursor.execute(f"select states,district,years,quarter,sum(transaction_count) as Total_transaction, sum(transaction_amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} and States = '{selected_state}' group by states,district,years,quarter order by states,district")
            
            df1 = pd.DataFrame(cursor.fetchall(), columns=['States','District','Years','Quarter',
                                                            'Total_transaction','Total_amount'])
            fig = px.bar(df1,
                        title=selected_state,
                        x="District",
                        y="Total_transaction",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Magma)
            st.plotly_chart(fig,use_container_width=True)

# EXPLORE DATA - USERS      
    if Type == "Users":
        
# Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        
        cursor.execute(f"select States, sum(registereduser) as Total_Users, sum(appopens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by states order by states")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.States = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='States',
                color='Total_Appopens',
                color_continuous_scale='Viridis')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
            
# BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('Andaman & Nicobar', 'Andhra Pradesh',  'Arunachal Pradesh', 'Assam', 'Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa',
                             'Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra','Manipur',
                             'Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttarkhand',	'Uttar Pradesh','West Bengal'),index=30)
        
        if Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
        else:
        
            cursor.execute(f"select states,years,quarter,districts,sum(registereduser) as Total_Users, sum(appopens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} and states = '{selected_state}' group by states,districts,years,quarter order by states,districts")
            
            df = pd.DataFrame(cursor.fetchall(), columns=['States','Years', 'Quarter', 'Districts', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(int)
            
            fig = px.bar(df,
                        title=selected_state,
                        x="Districts",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Inferno)
            st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - Insurance
    if Type == "Insurance":
        
# Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2020 and Quarter in [1]:
                st.markdown("#### No Data")
            else:
                cursor.execute(f"select states, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_insurance where years = {Year} and quarter = {Quarter} group by states order by states")
                df1 = pd.DataFrame(cursor.fetchall(),columns= ['States', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.States = df2
                                            
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='States',
                        color='Total_amount',
                        color_continuous_scale='sunset')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
            
# Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2020 and Quarter in [1]:
                st.markdown("#### No Data")
            else:
                cursor.execute(f"select states, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_insurance where years = {Year} and quarter = {Quarter} group by states order by states")
                df1 = pd.DataFrame(cursor.fetchall(),columns= ['States', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.Total_Transactions = df1.Total_Transactions.astype(int)
                df1.States = df2

                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='States',
                        color='Total_Transactions',
                        color_continuous_scale='Reds')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
                        
# BAR CHART - TOP PAYMENT TYPE
            
        st.markdown("## :violet[Top Payment Type]")
        if Year == 2018 and Quarter in [1,2,3,4]:
            st.markdown("#### No Data")
        elif Year == 2019 and Quarter in [1,2,3,4]:
            st.markdown("#### No Data")
        elif Year == 2020 and Quarter in [1]:
            st.markdown("#### No Data")
        else:
            cursor.execute(f"select insurance_type, sum(insurance_count) as Total_Count, sum(insurance_amount) as Total_Amount from aggregated_insurance where years= {Year} and quarter = {Quarter} group by insurance_type order by insurance_type")
            df = pd.DataFrame(cursor.fetchall(), columns=['Insurance_type', 'Total_Count','Total_Amount'])

            fig = px.bar(df,
                        title='Insurance Types vs Total_Counts',
                        x="Insurance_type",
                        y="Total_Count",
                        orientation='v',
                        color='Total_Amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('Andaman & Nicobar', 'Andhra Pradesh',  'Arunachal Pradesh', 'Assam', 'Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa',
                             'Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra','Manipur',
                             'Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttarkhand',	'Uttar Pradesh','West Bengal'),index=30)
        if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
        elif Year == 2019 and Quarter in [1,2,3,4]:
            st.markdown("#### No Data")
        elif Year == 2020 and Quarter in [1]:
            st.markdown("#### No Data")
        else:
         
            cursor.execute(f"select states, districts,years,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_insurance where years = {Year} and quarter = {Quarter} and States = '{selected_state}' group by states, districts,years,quarter order by states,districts")
            
            df1 = pd.DataFrame(cursor.fetchall(), columns=['States','Districts','Years','Quarter',
                                                            'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                        title=selected_state,
                        x="Districts",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

# MENU 4 - ABOUT
            
if selected == "About":
    st.write(" ") 
    st.write(" ")
    st.markdown("### :violet[About PhonePe Pulse:] ")
    st.write("##### PhonePe Pulse offers real-time insights and visualizations, leveraging GitHub data for dynamic analytics within the PhonePe ecosystem. With customizable views and interactive dashboards, it provides a powerful and user-friendly solution for extracting, transforming, and visualizing data, enhancing decision-making capabilities.")
    st.markdown("### :violet[About PhonePe:] ")
    st.write("##### PhonePe is a leading digital payments platform in India, offering a range of services from mobile recharges to bill payments. Acquired by Flipkart in 2016, PhonePe is known for its user-friendly app and secure Unified Payments Interface (UPI) transactions, making it a widely used financial tool in the country.")
        
       
       