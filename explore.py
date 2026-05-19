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
cols = st.columns(2)

with cols[0]:
    client_location = st.radio(
    "Client Location",
    [":green-background[South Scotland]", ":yellow-background[Netherlands]", ":red-background[Poland]"],
    captions=[
        "2 gCO2/kWh (low)",
        "253 gCO2/kWh (medium)",
        "565 gCO2/kWh (high)",
    ],
)
    
with cols[1]:
    server_location = st.radio(
    "Server Location",
    [":green-background[Stockholm]", ":yellow-background[London]", ":red-background[Frankfurt]"],
    captions=[
        "20 gCO2/kWh (low)",
        "180 gCO2/kWh (medium)",
        "342 gCO2/kWh (high)",
    ],
)

carbon_intensities = {
    ":green-background[South Scotland]": 2,
    ":yellow-background[Netherlands]": 253,
    ":red-background[Poland]": 565,
    ":green-background[Stockholm]": 20,
    ":yellow-background[London]": 180,
    ":red-background[Frankfurt]": 342
}

ci_client = carbon_intensities[client_location]
ci_server = carbon_intensities[server_location]


st.markdown("#### Model")
heading = "What are these models?"
if st.button(heading, key="model1_btn", icon=":material/help:"):
    description = "Purpose of these models (task) and size comparison to modern LLM."
    page_link = "background.py"
    label = "Machine Learning Model Partitioning"
    help(heading, description, page_link, label)

model_options = ["small", "medium", "large"]
model_selection = st.pills("Size", model_options, default=model_options[0], selection_mode="single", label_visibility="hidden")
model_names = {"small": "resnet50", "medium": "resnet101", "large": "resnet152"}
model = model_names[model_selection]

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
    partition_point = st.slider("Blocks", 1, 8, 8)
columns = st.columns(10, gap="small")

icons = [":material/panorama:", ":material/filter_alt:", ":material/stacks:", 
         ":material/stacks:", ":material/stacks:", ":material/stacks:",
         ":material/filter_alt:", ":material/lightbulb:"]

for i in range(1, partition_point+1):
    icon = icons[i-1]
    col = columns[i]
    with col:
        st.error("", icon=icon)

for i in range(partition_point+1, 9):
    icon = icons[i-1]
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
carbon_client_list = carbon_client.tolist()
carbon_server = round(ci_server * energy_server, 2)
carbon_server_list = carbon_server.tolist()
carbon_total = round(carbon_client + carbon_server, 2)
carbon_total_list = carbon_total.tolist()
change = round((((carbon_total_list[partition_point-1] - carbon_total_list[7])/ carbon_total_list[7]) * 100))

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Full Model on Client**")
    st.metric("Total [gCO2]", f"{carbon_total_list[7]}")
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.metric("Client [gCO2]", f"{carbon_client_list[7]}")
    with sub_col2:
        st.metric("Server [gCO2]", f"{carbon_server_list[7]}")
with col2:
    if partition_point < 8 and partition_point > 1:
        text = f"{partition_point} Blocks on Client"
    elif partition_point == 1:
        text = f"{partition_point} Block on Client"
    else:
        text = "Full Model on Client"
    st.markdown(f"**{text}**")
    st.metric("Total [gCO2]", f"{carbon_total_list[partition_point-1]}", f"{change} %", delta_color="inverse")
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.metric("Client [gCO2]", f"{carbon_client_list[partition_point-1]}")
    with sub_col2:
        st.metric("Server [gCO2]", f"{carbon_server_list[partition_point-1]}")
