import streamlit as st
import networkx as nx
from pyvis.network import Network
from stvis import pv_static

from make_graph import make_graph

st.set_page_config(layout='wide')

HEIGHT = 600
WIDTH = 1000

with st.sidebar:
    st.subheader('Multiplicadors:')
    st.slider("year_of_study", min_value=0.0, max_value=1.0, value=0.5, key="year_mult")
    st.slider("interests", min_value=0.0, max_value=1.0, value=0.5, key="interests_mult")
    st.slider("preferred_role", min_value=0.0, max_value=1.0, value=0.5, key="role_mult")
    st.slider("friend_registration", min_value=0.0, max_value=1.0, value=0.5, key="friend_mult")
    st.slider("interest_in_challenges", min_value=0.0, max_value=1.0, value=0.5, key="challenges_mult")
    st.slider("preferred_languages", min_value=0.0, max_value=1.0, value=0.5, key="languages_mult")
    st.slider("EDGE MAX WIDTH", min_value=1, max_value=15, value=10, key="edge_max_width")
    st.slider("EDGE THRESHOLD", min_value=0.05, max_value=1.0, value=0.5, key="edge_threshold")


graph = make_graph(
    year_mult=st.session_state.year_mult,
    interests_mult=st.session_state.interests_mult,
    preferred_role_mult=st.session_state.role_mult,
    friend_mult=st.session_state.friend_mult,
    languages_mult=st.session_state.languages_mult,
    challenges_mult=st.session_state.languages_mult,
    edge_max_width=st.session_state.edge_max_width,
    edge_threshold=st.session_state.edge_threshold,
    n_clusters=8
)

pos = nx.circular_layout(graph, scale=500)

net = Network(height=f"{HEIGHT}px", width=f"{WIDTH}px")
net.from_nx(graph)

for node in net.get_nodes():
    net.get_node(node)['x']=pos[node][0]
    net.get_node(node)['y']=-pos[node][1]
    net.get_node(node)["physics"] = False

net.toggle_physics(False)

pv_static(net)
