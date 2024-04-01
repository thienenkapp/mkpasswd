import streamlit as st
import requests

url_countries="https://api-mkpasswd.thienenkapp.de/countries"
url_categories="https://api-mkpasswd.thienenkapp.de/categories?country={country}"
url_passwords="https://api-mkpasswd.thienenkapp.de/passwords?country={country}&category={category}&number={number}"

if 'count' not in st.session_state:
    st.session_state.count = 0

def get_api_data(p_url):
    response = requests.get(p_url)
    #print(response)
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        # Process the data as needed
    else:
        print(f"Error: {response.status_code}")
        data={}
    return data

# Droplist options
countries = [item["name"] for item in get_api_data(url_countries)]

st.title('mkpasswd - make a password')

country_selected = st.selectbox("Select country:", countries)
#print(url_categories.format(country=country_selected))
categories = [item["name"] for item in get_api_data(url_categories.format(country=country_selected))]

category_selected = st.selectbox("Select category:", categories,index=0)
number_of_passwords = st.number_input("Number of password:", value=5, min_value=1, max_value=50)

with st.spinner():
    #print(url_passwords.format(country=country_selected,category=category_selected,number=number_of_passwords))
    passwords=get_api_data(url_passwords.format(country=country_selected,category=category_selected,number=number_of_passwords))
    #st.write(passwords)
    st.table(passwords)
    st.session_state.count += 1

st.info(f"Version v0.1.0, #{st.session_state.count}")

st.toast("Execution stopped")
st.stop()
