import streamlit as st
import plotly.express as px

def main():
    st.title("Pie Chart Example")

    # Sample data
    data = {
        "Category": ["Category A", "Category B", "Category C"],
        "Value": [30, 40, 30],
    }

    # Create a pie chart using Plotly Express
    fig = px.pie(data, names="Category", values="Value", title="My Pie Chart")

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
