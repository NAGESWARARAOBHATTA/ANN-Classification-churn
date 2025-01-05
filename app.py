import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
import streamlit as st
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder

model=tf.keras.models.load_model('model.h5')

with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender=pickle.load(file)

with open('onehot_encoder_geo.pkl','rb') as file:
    label_encoder_geo=pickle.load(file)

with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)

st.title('Customer Churn Prediction')

geography=st.selectbox('Geography',list(label_encoder_geo.categories_[0]))
gender=st.selectbox('Gender',label_encoder_gender.classes_)
age=st.slider("Age",18,92)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
num_of_products=st.slider('Number of Products',1,4)
has_cr_card=st.selectbox('Has Credit Card',[0,1])
is_active_number=st.selectbox('Is Activate Member',[0,1])


input_data=pd.DataFrame({
    'CreditScore':[credit_score],
    'Gender':[label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_number],
    'EstimatedSalary':[estimated_salary]
})




geo_encoder=label_encoder_geo.transform([[geography]]).toarray()
geo_encoder_df=pd.DataFrame(geo_encoder,columns=label_encoder_geo.get_feature_names_out(['Geography']))

input_data=pd.concat([input_data.reset_index(drop=True),geo_encoder_df],axis=1)


input_data_scaled=scaler.transform(input_data)

prediction=model.predict(input_data_scaled)
prediction_prob=prediction[0][0]

st.write("churn probability:",prediction_prob)

if prediction_prob>0.5:
    st.write("The customer is likely to churn")
else:
    st.write("the customer is not likely to churn")
