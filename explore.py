import streamlit as st
import pandas as pd

summary_df = pd.read_csv("summary.csv")


@st.dialog("Background")
def help(heading, description, info=None):
    st.markdown(f"# {heading}")
    st.markdown(description)
    if info:
        st.info(info[0], icon=info[1])

st.title("Can Model Partitioning Reduce Machine Learning Carbon Emissions?")
st.markdown('''
            Training machine learning (ML) models requires significant amounts of energy, which can result in high carbon emissions.
              
            ''')
st.info('''Explore how **carbon intensity**, **model size**, and **model partitioning** affect the **carbon footprint**.''', icon=":material/swipe_down:")

st.markdown("#### Carbon Intensity")
heading = "What is carbon intensity?"
if st.button(heading, key="ci_button", icon=":material/co2:"):
    description = '''
    - Carbon intensity denotes how much carbon was emitted by producing one unit of electricity  
    - Renewable energy sources, such as wind or solar, have significantly lower carbon intensities than fossil fuel-based sources, such as gas or coal  
    - As electricity grids around the world consist of different combinations of energy sources, the carbon intensity varies from grid to grid
    '''
    info = ["Does moving the client or server to a different location lower the carbon footprint?", ":material/globe_location_pin:"]
    help(heading, description, info)
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
    index=2
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
if st.button(heading, key="model1_btn", icon=":material/graph_4:"):
    description = '''
    - The models considered in this study are trained for **image classification**, so assigning predetermined classes to an image based on its content
    - The main difference between these models is their **size**, i.e., their number of parameters
        - "small": ~100 million
        - "medium": ~200 million
        - "large": ~250 million
        - To put these numbers into perspective: some modern large language models (LLMs) are estimated to have over 1 trillion parameters.
    - **More parameters** mean the model can be adjusted more precisely, which can improve its **accuracy**
    - However, this also results in **more work** during the training to adjust all those extra parameters
'''
    info = ["How does model size affect the overall carbon footprint?", ":material/bid_landscape:"]
    help(heading, description, info)

model_options = ["small", "medium", "large"]
model_selection = st.pills("Size", model_options, default=model_options[1], selection_mode="single")
model_names = {"small": "resnet50", "medium": "resnet101", "large": "resnet152"}
model = model_names[model_selection]

st.markdown("#### Partitioning")
heading = "How does model partitioning work?"
if st.button(heading, key="partitioning_btn", icon=":material/content_cut:"):
    description = '''
    - A machine learning model consists of a sequence of layers   
    - In model partitioning, models are **split into blocks** consisting of one or more layers that can then be **offloaded** to a more powerful server
    - This **reduces the computational load**, and thereby the energy consumption, of the client but increases the computational load and energy consumption of the server  
    - Therefore, moving blocks between client and server allows us to essentially **shift energy consumption** between them
'''
    info = ["What happens to the carbon emissions when you **partition** the model and **offload** part of the work to the server?", ":material/split_scene:"]
    help(heading, description, info)

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



st.markdown("### Estimated Carbon Footprint")
heading = "How is the carbon footprint calculated for ML model training?"
if st.button(heading, key="carbon_btn", icon=":material/mystery:"):
    description = '''The carbon emissions are calculated with the following formula:    
    $C=CI_{Client} \\times E_{Client} + CI_{Server} \\times E_{Server}$
    \n\n where *CI* is the current carbon intensity and *E* is the energy consumed by the computing hardware during the training.
    '''
    help(heading, description)

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
    st.space("small")
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

st.markdown("### Connect with me")
col1, col2 = st.columns([0.25, 0.75])

with col1:
    st.image("linkedin.png")

with col2:
    st.space("medium")
    st.markdown("Add me on LinkedIn")
