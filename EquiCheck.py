import streamlit as st
import pandas as pd
st.set_page_config(page_title="EquiCheck", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.shutterstock.com/image-vector/bullish-candlestick-graph-chart-stock-260nw-2169680589.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center;'> EquiCheck </h1>
    <p style='text-align: center;'> A simple app for you to comapare your holdings! </p>
    <p style='text-align: center;'>Upload the excel sheets with old week and new week holdings and it'll verify mismatches in your stock quantities </p>
    """,
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)
file1 = st.file_uploader("Upload old week excel sheet", type="xlsx")
file2 = st.file_uploader("Upload new week excel sheet", type="xlsx")

def file_cleaner(file):
    data=pd.read_excel(file,header=None)
    for i, row in data.iterrows():
        if "Scrip Name" in row.values and "Total Holding" in row.values and "ScripCode" in row.values:
            index=i
            break
    else :
        raise ValueError("No such column names found")
    data.columns= data.iloc[index]
    data = data.drop(index=range(index + 1)).reset_index(drop=True)
    data = data[:-2]
    cleaned_data= data[["ScripCode","Scrip Name","Total Holding"]]
    return cleaned_data

if file1 and file2:
    try:
        totalholding1= file_cleaner(file1)
        totalholding2= file_cleaner(file2)
        
        compared=pd.DataFrame({"ScripCode":totalholding1["ScripCode"],
                               "Scrip Name":totalholding1["Scrip Name"],
                               "Total Holding (old week)":totalholding1["Total Holding"],
                               "Total Holding (new week)":totalholding2["Total Holding"]})
        compared["Total Holding (old week)"]=pd.to_numeric(compared["Total Holding (old week)"],errors="coerce")
        compared["Total Holding (new week)"]=pd.to_numeric(compared["Total Holding (new week)"],errors="coerce")
        compared["Difference"]= compared["Total Holding (new week)"]-compared["Total Holding (old week)"] 
        # compared=compared.drop(index=62)
        mismatches=compared[compared["Difference"]!=0]
        if mismatches.empty:
            st.success("NO MISMATCHES DETECTED")
        else:
            st.error("THE FOLLOWING ARE THE MISMATCHED STOCKS")
            st.dataframe(mismatches)
    except Exception as e:
        st.error(f"Error processing files: {e}")





