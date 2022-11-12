import requests
import streamlit as st

st.set_page_config(page_title="Threat Map", page_icon=":fishing_pole_and_fish:", layout="wide")


def load_threats(page_number):
    key = st.secrets["key"]
    headers = {'X-OTX-API-KEY': key}
    # params = {'page': '5',}
    response = requests.get(f'https://otx.alienvault.com/api/v1/pulses/subscribed?page={page_number}', headers=headers)
    data = response.json()
    list = data['results']
    threat_collector(list)


def indicator_details(list_of_indicator):
    indicator_dict = {'indicator': '', 'type': '', 'created': ''}
    st.warning("Indicator of compromise", icon="⚠️")
    indicator_list = []
    indicator_type_list = []
    date_time_list = []
    table = '''
            <table style="width:100%;table-layout: fixed;">
                <tr>
                    <th style="width:50%;border:1px solid black;border-collapse: collapse;">Indicator</th>
                    <th style="width:25%;border:1px solid black;border-collapse: collapse;">Type</th>
                    <th style="width:25%;border:1px solid black;border-collapse: collapse;">Date of Creation</th>
                    </tr>
            </table>
            '''
    st.markdown(table, unsafe_allow_html=True)
    for i in range(len(list_of_indicator)):
        for key, val in list_of_indicator[i].items():
            indicator_dict[key] = val
        indicator_list.append(indicator_dict["indicator"])
        indicator_type_list.append(indicator_dict["type"])
        date_time_list.append(indicator_dict["created"])
        updated_table = f'''
        <table style="width:100%;table-layout: fixed;">
        <tr>
            <td style="width:50%;overflow-y: hidden;">{indicator_list[i]}</td>
            <td style="width:25%">{indicator_type_list[i]}</td>
            <td style="width:25%">{date_time_list[i]}</td>
        </tr>
        </table>
        '''
        st.markdown(updated_table, unsafe_allow_html=True)


def threat_collector(list_of_json):
    final_dict = {"name": "", "description": "", "adversary": "", "indicators": ""}
    for i in range(len(list_of_json)):
        for key, val in list_of_json[i].items():
            final_dict[key] = val
        st.info('Name: ' + final_dict["name"])
        st.write('Description: ' + final_dict["description"])
        st.write('Adversary: ' + final_dict["adversary"])
        with st.expander("Show IOC Details"):
            (indicator_details(final_dict["indicators"]))
        st.write('**********************************************************************************'
                 '************************************************************************************')


def post_url_sample(url):
    key = st.secrets["key"]
    headers = {'X-OTX-API-KEY': key}
    api = 'https://otx.alienvault.com/api/v1/indicators/submit_url'
    myobj = {'url': f'{url}'}
    result = requests.post(api, json=myobj, headers=headers)
    if result.status_code == 200:
        st.success("url Sample submitted succesfully")

def get_last_result():
    key = st.secrets["key"]
    headers = {'X-OTX-API-KEY': key}
    result = requests.get('https://otx.alienvault.com/api/v1/indicators/submitted_urls', headers=headers)
    data = result.json()
    list = data['results']
    result_dict = {'url': '', 'add_date': '', 'sent_date': '', 'complete_date': '', 'tlp': ''}
    for i in range(1):
        for key, val in list[i].items():
            result_dict[key] = val
    st.write(f'Submitted url: {result_dict["url"]}  \nAdded Date: {result_dict["add_date"]}  \nSent Date: {result_dict["sent_date"]}  \nCompleted Date: {result_dict["complete_date"]}  \nTLP: {result_dict["tlp"]}')

def get_all_result():
    key = st.secrets["key"]
    headers = {'X-OTX-API-KEY': key}
    result = requests.get('https://otx.alienvault.com/api/v1/indicators/submitted_urls', headers=headers)
    data = result.json()
    list = data['results']
    result_dict = {'url': '', 'add_date': '', 'sent_date': '', 'complete_date': '', 'tlp': ''}
    url_list = []
    add_date = []
    sent_date = []
    complete_date = []
    tlp_list = []
    for i in range(len(list)):
        for key, val in list[i].items():
            result_dict[key] = val

        url_list.append(result_dict['url'])
        add_date.append(result_dict['add_date'])
        sent_date.append(result_dict['sent_date'])
        complete_date.append(result_dict['complete_date'])
        tlp_list.append(result_dict['tlp'])
        st.write(
            f'Submitted url: {url_list[i]}  \nAdded Date: {add_date[i]}  \nSent Date: {sent_date[i]}  \nCompleted Date: {complete_date[i]}  \nTLP: {tlp_list[i]}')


with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Top Threats")
        option = st.selectbox(
            'Load more threats by selecting next pages',
            ('1', '2', '3', '4', '5'))
        if option == '1':
            load_threats(1)
        if option == '2':
            load_threats(2)
        if option == '3':
            load_threats(3)
        if option == '4':
            load_threats(4)
        if option == '5':
            load_threats(5)
        st.write('You are viewing page:', option)
    with right_column:
        st.subheader("Analyse Malicious url")
        url = st.text_input('Paste the suspicious url here and hit enter', '')
        if url != '':
            post_url_sample(url)
            with st.expander("Check this result:"):
                get_last_result()
            with st.expander("Check all results submitted"):
                get_all_result()

        st.subheader("Analyse Malicious File")
        uploaded_file = st.file_uploader("Upload Suspicious File to Analyze")




