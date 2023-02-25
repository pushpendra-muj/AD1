import streamlit as st
import os
import database as db
from keras.models import model_from_json
import numpy as np
from tensorflow.keras.preprocessing import image
with open('model_arch.json', 'r') as json_file:
    json_savedModel= json_file.read()
model = model_from_json(json_savedModel)
model.load_weights('my_model_weights.h5')



def form():
    st.title ("Form")
    with st.form(key= "Information form"):
        col1, col2 = st.columns(2)
        with col1:
            st.title('Doctor Information')
            docname=st.text_input("Enter Doctor name ")
            doc_contact=st.number_input("Enter Doctor contact number ",step=1)
            doc_quli=st.text_input("Enter Doctor Qualification ")
            hospital_name=st.text_input("Enter Hospital name ")
            hospital_address=st.text_input("Enter Hospital Address ")
        with col2:
            st.title('Patient Information')
            id=st.text_input("Enter Patient id: ")
            name=st.text_input("Enter Patient name ")
            age=st.number_input("Enter Patient age: ",step=1)
            date = st.date_input("Enter the date: ")
            address=st.text_input("Enter Patient Address: ")
            pat_contact=st.number_input("Enter Patient contact number: ",step=1)
            aadhar=st.number_input("Enter Patient aadhar number: ",step=1)
            remark=st.text_input("Enter Remark (for Doctor Use): ")
            st.markdown("Predicted Class is "+str(pred_class))
            pred=str(pred_class)
        submission=st.form_submit_button(label="Submit")
        
        if submission == True :
            db.insert_result(docname,doc_contact,doc_quli,hospital_name,hospital_address,id,name,age,date,address,pat_contact,aadhar,remark,pred)
            st.success ("Successfully submitted")
            
            st.title('Results')
            st.markdown('Patient id: '+str(id))
            st.markdown('Name: '+name)
            st.markdown('Age: '+str(age))
            st.markdown('Date: '+str(date))
            st.markdown('Address: '+address)
            st.markdown('Contact: '+str(pat_contact))
            st.markdown('Aadhar: '+str(aadhar))
            st.markdown('Prediction : '+pred)


def predict_img(img):
    input_img = image.img_to_array(img)
    input_img = np.expand_dims(input_img, axis=0)
    predict_img = model.predict(input_img)
    y_pred = np.argmax(predict_img, axis=1)
    target_names = ['Actinic Keratosis', 'Basal Cell Carcinoma', 'Dermatofibroma','Squamous Cell Carcinoma' , 'Nevus', 'Pigmented Benign Keratosis', 'Seborrheic Keratosis', 'Melanoma', 'Vascular Lesion']
    return target_names[y_pred[0]]

html_temp = """
    <div style="background-color:#f63366;padding:10px;margin-bottom: 25px">
    <h2 style="color:white;text-align:center;">Skin Cancer Detection</h2>
    <p style="color:white;text-align:center;" >This is a <b>Streamlit</b> app use for prediction of the <b>9 type of Skin Cancer</b>.</p>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)

option = st.radio('', ['Choose a test image', 'Choose your own image'])
if option == 'Choose your own image':
    uploaded_file = st.file_uploader("Choose an image...", type="jpg") #file upload
    if uploaded_file is not None:
        
        img = image.load_img(uploaded_file, target_size=(180,180,3))
        pred_class = predict_img(img)
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, width=200)
        with col2:
            st.success("Skin Cancer Type:  [" + str(pred_class) + "] ")
        form()
else:
    test_images = os.listdir('sample_images')
    test_image = st.selectbox('Please select a test image:', test_images)
    file_path = 'sample_images/' + test_image
    img = image.load_img(file_path, target_size=(180,180,3))
    pred_class = predict_img(img)
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, width=200)
    with col2:
        st.success("Skin Cancer Type:  [" + str(pred_class) + "] ")
    form()
