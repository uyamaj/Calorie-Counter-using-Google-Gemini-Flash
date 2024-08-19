
from dotenv import load_dotenv

load_dotenv()  # load all the environment variables from .env file

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load gemini-1.5-flash

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue() #read the files as bytes

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title=("Gemini Calorie App"))

st.header("Gemini Calorie App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the food...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the total calories")

input_prompt = """
               You are a registered dietician.
               You will upload a food image and calculate the total calories of the food in the image
               you will provide information on the specific ingredients and quantities
               of every food item.
               You will provide the calorie count based on the uploaded image,
               using the below format


                  1. Item 1 - no of calories
                  2. Item 2 - no of calories
                  ----
                  ----



               """
## If submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
