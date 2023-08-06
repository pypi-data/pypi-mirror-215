import os
import streamlit as st
import streamlit.components.v1 as components


_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "chat_box_streamlit",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("chat_box_streamlit", path=build_dir)


def message(isLeft=True, message="", loading=False, loadingText="Loading...", placeholder="Enter your input", height=500, key=None):
    component_value =  _component_func(component="message", isLeft=isLeft, message=message, placeholder=placeholder, loading=loading, loadingText=loadingText, height=height, key=key)
    return component_value

def input(placeholder="Enter your input", loading=False, loadingText="Loading...", rows=1, key=None):
    component_value = _component_func(component="input", placeholder=placeholder, rows=rows, loading=loading, loadingText=loadingText, key=key)
    return component_value

def display_chat(leftMessages = [], rightMessages=[], height=500, rows=1, key=None):
    component_value = _component_func(component="", leftMessages=leftMessages, rightMessages=rightMessages, rows=rows, height=height, key=key)
    return component_value