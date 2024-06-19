import streamlit as st
from keboola_streamlit import KeboolaStreamlit

# Get secrets from Streamlit
TOKEN = st.secrets["STORAGE_API_TOKEN"]
URL = st.secrets["KEBOOLA_HOSTNAME"]
ROLE_ID = st.secrets["REQUIRED_ROLE_ID"]

# Initialize KeboolaStreamlit
keboola = KeboolaStreamlit(URL, TOKEN)

# Set mockup headers for development and testing purposes
keboola.set_dev_mockup_headers({
    'X-Kbc-User-Email': 'user@dev.com',
    'X-Kbc-User-Roles': ['123', '11111111-2222-3333-4444-1234567890', 'abc'],
    'X-Forwarded-Host': 'https://mock-server/non-existing-app'
})

# Automatically create event when user opens the app, can add custom message, default is 'Streamlit App Create Event'
# Session_state is used to prevent multiple events from being created
if 'event_created' not in st.session_state:
    keboola.create_event(message='Streamlit App Open')
    st.session_state['event_created'] = True

# Check if user has required role and is authorized to access the app; if not, stop the app. 
# Debug is set to True, showing the headers in the sidebar
st.sidebar.subheader("Authorization (Debug)")
keboola.auth_check(ROLE_ID, debug=True)

# Add logout button to sidebar in case user wants to log out from the app
st.sidebar.subheader("Logout")
keboola.logout_button()

# In case user wants to create an event manually
st.subheader("Create Event")
st.caption("Click the button to create an event.")
if st.button("Create"):
    keboola.create_event()
    st.success("Event created successfully.")

# Get table from Keboola Storage
# Text input to enter the table ID, but it can be hardcoded as well
st.subheader("Read Table")
st.caption("Enter the table ID to read the table from Keboola Storage.")
table_id = st.text_input("Table ID")
if st.button("Read Table"):
    df_read = keboola.read_table(table_id)
    st.session_state['table'] = df_read   

if 'table' in st.session_state:
    st.dataframe(st.session_state['table'])

# Write table to Keboola Storage
st.subheader("Write Table")
st.caption("In this example, the table is written to the same table ID as the one read. You have to read a table first.")
if st.button("Write Table"):
    keboola.write_table(table_id=table_id, df=st.session_state['table'])
    st.success("Done!")

# Add table selection to sidebar
st.sidebar.subheader("Table Selection")
df_select = keboola.add_table_selection(sidebar=True)
if not df_select.empty:
    st.subheader("Selected Table")
    st.dataframe(df_select)