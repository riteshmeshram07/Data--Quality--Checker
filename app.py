import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Quality Checker", layout="wide")
st.title("📊 Automated Data Quality Checker")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

def run_data_quality_checks(df):
    report = {}
    report['nulls'] = df.isnull().sum().to_frame(name="Null Count")
    report['nulls']["% Null"] = (df.isnull().mean() * 100).round(2)
    report['duplicates'] = df.duplicated().sum()
    report['data_types'] = df.dtypes.to_frame(name="Data Type")
    report['cardinality'] = df.nunique().to_frame(name="Unique Values")
    report['summary'] = df.describe(include='all')
    numeric_cols = df.select_dtypes(include=np.number).columns
    outliers = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers[col] = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
    report['outliers'] = pd.DataFrame.from_dict(outliers, orient='index', columns=["Outlier Count"])
    return report

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Data", df.head())

    with st.spinner("Running data quality checks..."):
        report = run_data_quality_checks(df)

        st.subheader("🧹 Null Values")
        st.dataframe(report['nulls'])

        st.subheader("🧾 Duplicate Rows")
        st.write(f"Total duplicate rows: {report['duplicates']}")

        st.subheader("📘 Data Types")
        st.dataframe(report['data_types'])

        st.subheader("🔢 Unique Values (Cardinality)")
        st.dataframe(report['cardinality'])

        st.subheader("📊 Summary Statistics")
        st.dataframe(report['summary'])

        st.subheader("🚨 Outliers")
        st.dataframe(report['outliers'])


st.markdown("""---""")
st.markdown("### 👨‍💻 Made by [Ritesh Meshram](https://in.linkedin.com/in/ritesh-meshram) with ❤️ using Streamlit")
