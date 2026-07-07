import streamlit as st
import pandas as pd
import google.generativeai as genai

# Gemini API Key
genai.configure(api_key="YOUR API KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

# Load Dataset
df = pd.read_csv(
    r"C:\Users\siriv\Sample - Superstore.csv",
    encoding="latin1"
)

# KPIs
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

category_profit = df.groupby('Category')['Profit'].sum()

st.markdown("""
<style>
h1 {
    color: #111827 !important;
    font-weight: 800 !important;
}

h2 {
    color: #111827 !important;
    font-weight: 700 !important;
}

h3 {
    color: #1f2937 !important;
    font-weight: 700 !important;
}

thead tr th {
    color: black !important;
    font-weight: bold !important;
}

tbody tr td {
    color: #222222 !important;
}
</style>
""", unsafe_allow_html=True)


# UI
st.title("Agentic AI Business Intelligence Assistant")

st.header("Business Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("Total Profit", f"${total_profit:,.2f}")

st.subheader("Category Profit")

st.bar_chart(category_profit)

region_profit = df.groupby('Region')['Profit'].sum()

st.subheader("Region Profit")

st.bar_chart(region_profit)

if category_profit['Furniture'] < 20000:
    st.error("⚠ Furniture category requires immediate attention")
# Health Score
score = 90

st.subheader("Business Health Score")

st.success(f"Health Score: {score}/100")

st.info("""
📌 AI Recommendations

• Reduce Furniture discounts

• Focus more on Technology products

• Expand operations in West Region

• Review loss-making Furniture products
""")

st.subheader("Loss Making Sub-Categories")

subcat_profit = df.groupby('Sub-Category')['Profit'].sum()

loss_subcats = subcat_profit[subcat_profit < 0]

styled_loss = loss_subcats.sort_values().to_frame()

st.table(loss_subcats.sort_values().to_frame())
 
 
st.subheader("Executive Report")

report = f"""
📊 Executive Business Summary

Total Sales: ${total_sales:,.2f}
Total Profit: ${total_profit:,.2f}

Key Findings:
• Technology is the highest profit category.
• West is the highest profit region.
• Furniture is underperforming.
• Tables are causing the highest losses.

Recommendations:
• Reduce Furniture discounts.
• Focus on Technology growth.
• Expand operations in West region.
• Review loss-making products.
"""

st.text_area("Business Report", report, height=250)

st.download_button(
    label="📥 Download Executive Report",
    data=report,
    file_name="Executive_Report.txt",
    mime="text/plain"
)
# AI Assistant

st.subheader("AI Business Assistant")

question = st.text_input("Ask a business question")

if question:

    context = f"""
    Business Data Summary

    Total Sales: {total_sales}
    Total Profit: {total_profit}

    Category Profit:
    {category_profit.to_string()}

    Region Profit:
    {region_profit.to_string()}

    Loss Making Sub-Categories:
    {loss_subcats.to_string()}

    top_products = df.groupby("Product Name")["Profit"].sum().sort_values(ascending=False).head(5)

    st.subheader("Top 5 Profitable Products")
    st.table(top_products)

    Business Health Score:
    {score}/100

Current Recommendations:
1. Reduce Furniture discounts
2. Focus more on Technology products
3. Expand operations in West Region
4. Review loss-making Furniture products

You are a senior Business Intelligence Consultant.
Answer only using the business data provided.
Give actionable recommendations.
"""
    
    

    prompt = context + "\nQuestion : " + question
    
    with st.spinner("Analyzing business data..."):
     response = model.generate_content(prompt)


    st.success("Analysis Complete!")

    st.write(response.text)

   

   

   


    st.markdown("---")
    st.caption("Developed by Siri Vennela | Agentic AI Business Intelligence Assistant")