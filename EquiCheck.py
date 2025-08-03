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
    cleaned_data= data[["ScripCode","Scrip Name","Total Holding"]].copy()
    cleaned_data["ScripCode"] = cleaned_data["ScripCode"].astype(str).str.strip()
    cleaned_data["Scrip Name"] = cleaned_data["Scrip Name"].astype(str).str.strip()
    cleaned_data["Total Holding"] = pd.to_numeric(cleaned_data["Total Holding"], errors="coerce").fillna(0)

    return cleaned_data

if file1 and file2:
    try:
        totalholding1= file_cleaner(file1).copy()
        totalholding2= file_cleaner(file2).copy()
        # all_stocks=pd.unique(totalholding1["ScripCode"].tolist()+totalholding2["ScripCode"].tolist())
        # all_stocks.sort()
        # def editor(df1,df2):
        #     missing_stocks= set(all_stocks)-set(df1["ScripCode"])
        #     additions=[]
        #     for stock in missing_stocks:
        #         name=df2.loc(df2["ScripCode"]==stock, "Scrip Name").values
        #         name= name[0] if len(name) else ""
        #         additions.append({"ScripCode":stock,"Scrip Name":name,"Total Holding":0})
        #     return pd.concat([df1, pd.DataFrame(additions)], ignore_index=True)   
        # totalholding1= editor(totalholding1,totalholding2)
        # totalholding2= editor(totalholding2,totalholding1)
        all_scrips = pd.unique(totalholding1["ScripCode"].tolist() + totalholding2["ScripCode"].tolist())
        all_scrips.sort()

        def fill_missing(df, ref_df):
            missing_codes = set(all_scrips) - set(df["ScripCode"])
            rows_to_add = []
            for code in missing_codes:
                name = ref_df.loc[ref_df["ScripCode"] == code, "Scrip Name"].values
                name = name[0] if len(name) else ""
                rows_to_add.append({"ScripCode": code, "Scrip Name": name, "Total Holding": 0})
            return pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)

        totalholding1 = fill_missing(totalholding1, totalholding2)
        totalholding2 = fill_missing(totalholding2, totalholding1)

        totalholding1= totlaholding1.sort_values(by="Scrip Name").reset_index(drop=True)
        totalholding2= totalholding2.sort_values(by="Scrip Name").reset_index(drop=True)
        
        compared=pd.DataFrame({"ScripCode":totalholding1["ScripCode"],
                               "Scrip Name":totalholding1["Scrip Name"],
                               "Total Holding (old week)":totalholding1["Total Holding"],
                               "Total Holding (new week)":totalholding2["Total Holding"]})
        
        compared["Difference"]= compared["Total Holding (new week)"]-compared["Total Holding (old week)"] 
        
        status=[]
        for _, row in compared.iterrows():
            old = row["Total Holding (old week)"]
            new = row["Total Holding (new week)"]
            if old == 0 and new > 0:
                status.append("Newly Bought")
            elif old > 0 and new == 0:
                status.append("Sold Entirely")
            elif old != new:
                status.append("Traded")
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





