import streamlit as st
import pandas as pd
st.set_page_config(page_title="EquiCheck", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center;'> EquiCheck </h1>
    <h5 style='text-align: center;'> Here is an early birthday gift for you Papa </h5>
    <h6 style='text-align: center;'> A simple app to compare your stock holdings! </h6> 
    <p style='text-align: center;'> Upload the excel sheets with old week and new week holdings and it'll verify the mismatches in your stock quantities. </p>
    """,
    unsafe_allow_html=True)


file1 = st.file_uploader("Upload old week excel sheet", type="xlsx")
file2 = st.file_uploader("Upload new week excel sheet", type="xlsx")

def file_cleaner(file):
    data=pd.read_excel(file,header=None)
    for i, row in data.iterrows():
        if "Scrip Name" in row.values and "Total Holding" in row.values:
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
        totalholding1= file_cleaner(file1).copy()
        totalholding2= file_cleaner(file2).copy()
         if totalholding1.shape > totalholding2.shape:
            for index, row in totalholding1.iterrows():
                 code = row["ScripCode"]
                 if code not in totalholding2["ScripCode"].values:
                     totalholding2.loc[index] = { code, row["Scrip Name"],0 }

        elif totalholding2.shape> totalholding1.shape:
            for index, row in totalholding2.iterrows():
                 code = row["ScripCode"]
                 if code not in totalholding1["Scrip Name"].values:
                     totalholding1.loc[index]={ code,row["Scrip Name"],0}
        
        compared=pd.DataFrame({"ScripCode":totalholding1["ScripCode"],
                               "Scrip Name":totalholding1["Scrip Name"],
                               "Total Holding (old week)":totalholding1["Total Holding"],
                               "Total Holding (new week)":totalholding2["Total Holding"]})
        compared["Total Holding (old week)"]=pd.to_numeric(compared["Total Holding (old week)"],errors="coerce")
        compared["Total Holding (new week)"]=pd.to_numeric(compared["Total Holding (new week)"],errors="coerce")
        compared["Difference"]= compared["Total Holding (new week)"]-compared["Total Holding (old week)"] 
        
        status=[]
        for _, row in compared.iterrows():
            old = row["Total Holding (old week)"]
            new = row["Total Holding (new week)"]
            if old == 0 and new > 0:
                status.append("Newly Bought")
            elif old > 0 and new == 0:
                status.append("Fully Sold")
            elif old != new:
                status.append("Quantity Changed")
            else:
                status.append("") 

        compared["Status"] = status

        mismatches=compared[compared["Difference"]!=0]
        if mismatches.empty:
            st.success("NO MISMATCHES DETECTED")
        else:
            st.error("THE FOLLOWING ARE THE MISMATCHED STOCKS")
            st.dataframe(mismatches)
    except Exception as e:
        st.error(f"Error processing files: {e}")





