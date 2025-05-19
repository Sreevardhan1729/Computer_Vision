import streamlit as st
import cv2
import numpy as np

def cvt(img):
    image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return image
def grayscale(img):
    image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return image
def blur(img):
    image = cv2.GaussianBlur(img,(7,7),0)
    image = cvt(image)
    return image
def sharpen(img):
    kernel = np.array([
        [-1,-1,-1],
        [-1,9,-1],
        [-1,-1,-1]
    ])
    image = cv2.filter2D(img,-1,kernel=kernel)
    image = cvt(image)
    return image
def histEqui(img):
    image = grayscale(img)
    image = cv2.equalizeHist(image)
    return image
def edges(img):
    image = grayscale(img)
    edges = cv2.Canny(image,100,200)
    return edges
def contours(img):
    edge = edges(img)
    contours, _ = cv2.findContours(edge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    image = img.copy()
    cv2.drawContours(image,contours,-1,(0,255,0),3)
    return image
    
def apply_effect(effect,tab,img):
    if effect == "GrayScale":
        tab.image(grayscale(img))
    elif effect == "Blur":
        tab.image(blur(img))
    elif effect == "Sharpening":
        tab.image(sharpen(img))
    elif effect == "Histogram Equization":
        tab.image(histEqui(img))
    elif effect == "Edges":
        tab.image(edges(img))
    elif effect == "Contours":
        tab.image(contours(img))
    elif effect=="Original":
        tab.image(img,channels="BGR")


st.header("Interactive Image Filter App")

upload_file = st.file_uploader("Upload an Image",type=["png","jpeg","jpg"])

if upload_file:
    img = np.frombuffer(upload_file.read(),np.uint8)

    img = cv2.imdecode(img,cv2.IMREAD_COLOR)

else:
    st.write("Upload an appropriate Image")
    st.stop()

effects = ["GrayScale", "Blur", "Sharpening", "Histogram Equization", "Edges", "Contours", "Original"]
selected_effects = []

st.write("Select Effects:")

num_columns = 5

for row_start in range(0, len(effects), num_columns):
    cols = st.columns(num_columns)
    
    for i, effect in enumerate(effects[row_start:row_start + num_columns]):
        with cols[i]:
            if st.checkbox(effect, value=(effect == "Original")):
                selected_effects.append(effect)

if selected_effects:
    tabs = st.tabs([i for i in selected_effects])
    for i, effect in enumerate(selected_effects):
        apply_effect(selected_effects[i],tabs[i],img)
        
else:
    st.write("Select at least one effect")
