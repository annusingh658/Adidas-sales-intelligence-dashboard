import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
ADIDAS_BLUE = "#0057B8"
ADIDAS_ORANGE = "#FF6B35"
ADIDAS_BLACK = "#000000"
df = pd.read_excel("Adidas.xlsx")
st.set_page_config(
    page_title="Adidas Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)
image = Image.open("adidas-logo.jpg")
ADIDAS_BLUE = "#0057B8"
ADIDAS_ORANGE = "#FF6B35"

st.markdown("""
<style>
div.block-container{
    padding-top:1rem;
}

.title-test{
    font-size:42px;
    font-weight:bold;
    color:#000000;
}

[data-testid="stMetric"]{
    background-color:#f8f9fa;
    padding:15px;
    border-radius:10px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)

html_title = """
<center>
<h1 class="title-test">
Adidas Sales Intelligence Dashboard
</h1>

<p style="font-size:18px;color:gray;">
Retail Performance Analysis | Streamlit • Plotly • Pandas
</p>
</center>
"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)
total_sales = df["TotalSales"].sum()
total_units = df["UnitsSold"].sum()
total_states = df["State"].nunique()

k1,k2,k3 = st.columns(3)

k1.metric("💰 Total Sales", f"${total_sales:,.0f}")
k2.metric("📦 Units Sold", f"{total_units:,.0f}")
k3.metric("📍 States", total_states)

st.divider()
col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

with col4:
    fig = px.bar(
    df,
    x="Retailer",
    y="TotalSales",
    color="Retailer",
    title="Total Sales by Retailer",
    template="plotly_white",
    height=500,
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig.update_layout(
    title_x=0.3,
    showlegend=False
)
st.plotly_chart(fig,use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer","TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by = df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(
    result,
    x="Month_Year",
    y="TotalSales",
    title="Monthly Sales Trend",
    template="plotly_white"
)

fig1.update_traces(
    line=dict(
        color=ADIDAS_BLUE,
        width=4
    )
)
st.plotly_chart(fig1,use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Get Data", data = result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales.csv", mime="text/csv")
    
st.divider()

result1 = df.groupby(by="State")[["TotalSales","UnitsSold"]].sum().reset_index()

# add the units sold as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(
    go.Bar(
        x=result1["State"],
        y=result1["TotalSales"],
        name="Total Sales",
        marker_color=ADIDAS_BLUE
    )
)
fig3.add_trace(
    go.Scatter(
        x=result1["State"],
        y=result1["UnitsSold"],
        mode="lines+markers",
        name="Units Sold",
        yaxis="y2",
        line=dict(
            color=ADIDAS_ORANGE,
            width=3
        )
    )
)
fig3.update_layout(
    title = "Total Sales and Units Sold by State",
    xaxis = dict(title="State"),
    yaxis = dict(title="Total Sales", showgrid = False),
    yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)
_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)

_, view3, dwn3 = st.columns([0.5,0.45,0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data", data = result1.to_csv().encode("utf-8"), 
                       file_name = "Sales_by_UnitsSold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns([0.1,1])
treemap = df[["Region","City","TotalSales"]].groupby(by = ["Region","City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(
    treemap,
    path=["Region","City"],
    values="TotalSales",
    hover_name="TotalSales (Formatted)",
    hover_data=["TotalSales (Formatted)"],
    color="TotalSales",
    color_continuous_scale="Blues",
    height=700
)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4,use_container_width=True)

_, view4, dwn4 = st.columns([0.5,0.45,0.45])
with view4:
    result2 = df[["Region","City","TotalSales"]].groupby(by=["Region","City"])["TotalSales"].sum()
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("Get Data", data = result2.to_csv().encode("utf-8"),
                                        file_name="Sales_by_Region.csv", mime="text.csv")

_,view5, dwn5 = st.columns([0.5,0.45,0.45])
with view5:
    expander = st.expander("View Sales Raw Data")
    expander.write(df)
with dwn5:
    st.download_button("Get Raw Data", data = df.to_csv().encode("utf-8"),
                       file_name = "SalesRawData.csv", mime="text/csv")
st.divider()
