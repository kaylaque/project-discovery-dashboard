import streamlit as st
import plotly.express as px
import pandas as pd

def main():
    st.title("Time Series Chart Example")

    # Sample time series data
    data = {
        "Date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
        "Value": [10, 15, 12, 17],
    }

    # Convert data to a DataFrame
    df = pd.DataFrame(data)

    # Create a time series chart using Plotly Express
    fig = px.line(df, x="Date", y="Value", title="Time Series Chart")

    # Display the time series chart in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
