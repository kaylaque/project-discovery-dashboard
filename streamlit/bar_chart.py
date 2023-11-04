import streamlit as st
import matplotlib.pyplot as plt

def main():
    st.title("Bar Chart Example")

    # Sample data
    categories = ["Category A", "Category B", "Category C", "Category D"]
    values = [10, 20, 15, 25]

    # Create the bar chart
    plt.bar(categories, values)
    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.title("My Bar Chart")

    # Display the bar chart using Matplotlib
    st.pyplot()

if __name__ == "__main__":
    main()
