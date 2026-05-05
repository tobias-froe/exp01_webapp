import streamlit as st
import pandas as pd

summary_df = pd.read_csv("summary.csv")


@st.dialog("Background")
def help(heading, description, page_link, label):
    st.markdown(f"# {heading}")
    st.markdown(description)
    st.markdown("Read on:")
    st.page_link(page_link, label=label)

st.title("How Can Model Partitioning Reduce Training Carbon Emissions?")
st.markdown('''Explore how **carbon intensity** and **model size** affect the **carbon footprint** of machine learning model training.  
What happens when you **partition** the model and **offload** part of the work to the server?''')

st.markdown("#### Carbon Intensity")
heading = "What is carbon intensity?"
if st.button(heading, key="ci_button", icon=":material/help:"):
    description = "Carbon intensity denotes how clean a given energy source is. It varies temporally and geographically."
    page_link = "background.py"
    label = "Carbon-Aware Computing"
    help(heading, description, page_link, label)

ci_client = st.slider("Client [gCO2e/kWh]", 0, 1000, 800)
ci_server = st.slider("Server [gCO2e/kWh]", 0, 1000, 2)


st.markdown("#### Model")
heading = "What are these models?"
if st.button(heading, key="model1_btn", icon=":material/help:"):
    description = "Purpose of these models (task) and size comparison to modern LLM."
    page_link = "background.py"
    label = "Machine Learning Model Partitioning"
    help(heading, description, page_link, label)

model_options = ["ResNet-50", "ResNet-101", "ResNet-152"]
model_selection = st.pills("", model_options, default=model_options[0], selection_mode="single", label_visibility="hidden")
model_selection = model_selection.lower().split("-")
model = f"{model_selection[0]}{model_selection[1]}"

st.markdown("#### :scissors: Partitioning")
heading = "How does model partitioning work?"
if st.button(heading, key="partitioning_btn", icon=":material/help:"):
    description = '''A machine learning model consists of multiple layers:  
    - :material/panorama: : An input layer where data samples, such as images, are passed in  
    - :material/flowchart: : One or more hidden layers where stuff happens  
    - :material/lightbulb: : An output layer where the model makes a prediction, such as assigning a class  
    We can partition, i.e. cut, models between these layers and offload them to a more powerful server.
    This reduces the computational load of the client.
'''
    page_link = "background.py"
    label = "Machine Learning Model Partitioning"
    help(heading, description, page_link, label)

part_columns = st.columns([0.1, 0.8, 0.1], gap="small")
with part_columns[0]:
    st.write("")
    st.write("")
    st.badge("Client", color="red")

with part_columns[2]:
    st.write("")
    st.write("")
    st.badge("Server", color="blue")

with part_columns[1]:
    partition_point = st.slider("Layers", 1, 8, 8)
columns = st.columns(10, gap="small")

for i in range(1, partition_point+1):
    if i == 1:
        icon = ":material/panorama:"
    else:
        icon = ":material/flowchart:"
    col = columns[i]
    with col:
        st.error("", icon=icon)

for i in range(partition_point+1, 9):
    if i == 8:
        icon = ":material/lightbulb:"
    else:
        icon = ":material/flowchart:"
    col = columns[i]
    with col:
        st.info(icon)



st.markdown("### :cloud: Estimated Carbon Footprint")
heading = "How is the carbon footprint calculated for ML model training?"
if st.button(heading, key="carbon_btn", icon=":material/help:"):
    description = '''The carbon emissions are calculated with the following formula:    
    $C=CI_{Client} \\times E_{Client} + CI_{Server} \\times E_{Server}$
    \n\n where *CI* is the current carbon intensity and *E* is the energy consumed by the computing hardware during the training.
    '''
    page_link = "methodology.py"
    label = "Methodology"
    help(heading, description, page_link, label)

carbon_emissions = []

energy_client = summary_df[(summary_df["model"] == model)]["energy_client"]
energy_server = summary_df[(summary_df["model"] == model)]["energy_server"]
carbon_client = round(ci_client * energy_client, 2)
carbon_server = round(ci_server * energy_server, 2)
carbon_total = round(carbon_client + carbon_server, 2)

carbon_emissions = carbon_total[partition_point-1]
change = round((((carbon_emissions - carbon_total[7])/ carbon_total[7]) * 100))

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Full Model on Client**")
    st.metric("gCO2", f"{carbon_total[7]}")
with col2:
    if partition_point < 8 and partition_point > 1:
        text = f"{partition_point} Layers on Client"
    elif partition_point == 1:
        text = f"{partition_point} Layer on Client"
    else:
        text = "Full Model on Client"
    st.markdown(f"**{text}**")
    st.metric("gCO2", f"{carbon_emissions}", f"{change} %", delta_color="inverse")

