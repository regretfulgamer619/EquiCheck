import streamlit as st
import pandas as pd
st.set_page_config(page_title="EquiCheck", layout="wide")
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
st.write("Data preview:")
st.dataframe(file1.head(100))

if file1 and file2:
    try:
        data_1= pd.read_excel(file1,header=None)
        data_2=pd.read_excel(file2, header=None)
        
        data_1.columns=data_1.iloc[2]
        data_1=data_1.drop(data_1.index[[0,1,2]]).reset_index(drop=True)
        totalholding1=data_1[["ScripCode","Scrip Name","Total Holding"]]
        totalholding1 = totalholding1.drop(totalholding1.index[[-1,-2]])
       
        data_2.columns=data_2.iloc[2]
        data_2=data_2.drop(data_2.index[[0,1,2]]).reset_index(drop=True)
        totalholding2=data_2[["ScripCode","Scrip Name","Total Holding"]]
        totalholding2=totalholding2.drop(totalholding2.index[[-1,-2]])
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





