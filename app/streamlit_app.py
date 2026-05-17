import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page Setup
# -------------------------------------------------
st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    layout="wide"
)

st.title("Nassau Candy Distributor Dashboard")
st.caption("Simple business dashboard for profit, margin, product performance, division performance, and forecast analysis")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("D:/nassau_profitability_project/data/processed/nassau_featured.csv")
    product_summary = pd.read_csv("D:/nassau_profitability_project/data/processed/product_summary.csv")
    division_summary = pd.read_csv("D:/nassau_profitability_project/data/processed/division_summary.csv")
    monthly_summary = pd.read_csv("D:/nassau_profitability_project/data/processed/monthly_summary.csv")
    factory_summary = pd.read_csv("D:/nassau_profitability_project/data/processed/factory_summary.csv")

    product_actions = pd.read_csv("D:/nassau_profitability_project/outputs/tables/product_summary_with_actions.csv")
    pareto_profit = pd.read_csv("D:/nassau_profitability_project/outputs/tables/pareto_profit_table.csv")
    pareto_revenue = pd.read_csv("D:/nassau_profitability_project/outputs/tables/pareto_revenue_table.csv")

    sales_forecast = pd.read_csv("D:/nassau_profitability_project/outputs/tables/sales_forecast_next_6_months.csv")
    profit_forecast = pd.read_csv("D:/nassau_profitability_project/outputs/tables/profit_forecast_next_6_months.csv")
    monthly_model = pd.read_csv("D:/nassau_profitability_project/outputs/tables/monthly_profit_model_output.csv")

    return (
        df,
        product_summary,
        division_summary,
        monthly_summary,
        factory_summary,
        product_actions,
        pareto_profit,
        pareto_revenue,
        sales_forecast,
        profit_forecast,
        monthly_model
    )

(
    df,
    product_summary,
    division_summary,
    monthly_summary,
    factory_summary,
    product_actions,
    pareto_profit,
    pareto_revenue,
    sales_forecast,
    profit_forecast,
    monthly_model
) = load_data()

# -------------------------------------------------
# Data Type Fixes
# -------------------------------------------------
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
monthly_summary["year_month"] = pd.to_datetime(monthly_summary["year_month"], errors="coerce")
monthly_model["year_month"] = pd.to_datetime(monthly_model["year_month"], errors="coerce")
sales_forecast["year_month"] = pd.to_datetime(sales_forecast["year_month"], errors="coerce")
profit_forecast["year_month"] = pd.to_datetime(profit_forecast["year_month"], errors="coerce")

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("Filter Dashboard")

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

division_list = sorted(df["division"].dropna().unique().tolist())
selected_divisions = st.sidebar.multiselect(
    "Select division",
    options=division_list,
    default=division_list
)

product_search = st.sidebar.text_input("Search product name")

margin_threshold = st.sidebar.slider(
    "Low margin alert threshold (%)",
    min_value=0,
    max_value=100,
    value=20
)

# -------------------------------------------------
# Apply Filters
# -------------------------------------------------
filtered_df = df.copy()

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["order_date"] >= start_date) &
        (filtered_df["order_date"] <= end_date)
    ]

filtered_df = filtered_df[filtered_df["division"].isin(selected_divisions)]

if product_search:
    filtered_df = filtered_df[
        filtered_df["product_name"].str.contains(product_search, case=False, na=False)
    ]

# -------------------------------------------------
# Rebuild Summaries After Filters
# -------------------------------------------------
filtered_product_summary = filtered_df.groupby(
    ["product_id", "product_name", "division"],
    as_index=False
).agg({
    "sales": "sum",
    "cost": "sum",
    "gross_profit": "sum",
    "units": "sum",
    "order_id": "nunique"
})
filtered_product_summary.rename(columns={"order_id": "total_orders"}, inplace=True)

if not filtered_product_summary.empty:
    filtered_product_summary["gross_margin_pct"] = (
        filtered_product_summary["gross_profit"] / filtered_product_summary["sales"]
    ) * 100
    filtered_product_summary["profit_per_unit"] = (
        filtered_product_summary["gross_profit"] / filtered_product_summary["units"]
    )
    filtered_product_summary["cost_ratio"] = (
        filtered_product_summary["cost"] / filtered_product_summary["sales"]
    )

filtered_division_summary = filtered_df.groupby("division", as_index=False).agg({
    "sales": "sum",
    "cost": "sum",
    "gross_profit": "sum",
    "units": "sum"
})

if not filtered_division_summary.empty:
    filtered_division_summary["gross_margin_pct"] = (
        filtered_division_summary["gross_profit"] / filtered_division_summary["sales"]
    ) * 100
    filtered_division_summary["profit_per_unit"] = (
        filtered_division_summary["gross_profit"] / filtered_division_summary["units"]
    )
    filtered_division_summary["revenue_contribution_pct"] = (
        filtered_division_summary["sales"] / filtered_division_summary["sales"].sum()
    ) * 100
    filtered_division_summary["profit_contribution_pct"] = (
        filtered_division_summary["gross_profit"] / filtered_division_summary["gross_profit"].sum()
    ) * 100

filtered_monthly_summary = filtered_df.groupby("year_month", as_index=False).agg({
    "sales": "sum",
    "cost": "sum",
    "gross_profit": "sum",
    "units": "sum"
})

if not filtered_monthly_summary.empty:
    filtered_monthly_summary["year_month"] = pd.to_datetime(filtered_monthly_summary["year_month"], errors="coerce")
    filtered_monthly_summary["gross_margin_pct"] = (
        filtered_monthly_summary["gross_profit"] / filtered_monthly_summary["sales"]
    ) * 100
    filtered_monthly_summary = filtered_monthly_summary.sort_values("year_month")

filtered_factory_summary = filtered_df.groupby("factory", as_index=False).agg({
    "sales": "sum",
    "cost": "sum",
    "gross_profit": "sum",
    "units": "sum"
})

if not filtered_factory_summary.empty:
    filtered_factory_summary["gross_margin_pct"] = (
        filtered_factory_summary["gross_profit"] / filtered_factory_summary["sales"]
    ) * 100

# -------------------------------------------------
# KPI Section
# -------------------------------------------------
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["gross_profit"].sum()
total_units = filtered_df["units"].sum()
overall_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0
profit_per_unit = (total_profit / total_units) if total_units != 0 else 0

top_product = "N/A"
if not filtered_product_summary.empty:
    top_product = filtered_product_summary.sort_values("gross_profit", ascending=False).iloc[0]["product_name"]

top_division = "N/A"
if not filtered_division_summary.empty:
    top_division = filtered_division_summary.sort_values("gross_margin_pct", ascending=False).iloc[0]["division"]

high_risk_count = 0
if not filtered_product_summary.empty:
    high_risk_count = (filtered_product_summary["gross_margin_pct"] < margin_threshold).sum()

st.subheader("Quick Business Summary")

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Sales", f"${total_sales:,.1f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Overall Margin %", f"{overall_margin:.2f}%")
c4.metric("Profit per Unit", f"${profit_per_unit:,.2f}")
with c5:
    st.markdown("### Top Profit Product")
    st.write(top_product)
c6.metric("Low Margin Products", f"{high_risk_count}")

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Overview",
    "Product Performance",
    "Division Performance",
    "Profit Concentration",
    "Recommended Actions",
    "Factory Performance",
    "Forecast"
])

# -------------------------------------------------
# TAB 1 - OVERVIEW
# -------------------------------------------------
with tab1:
    st.markdown("### Monthly Business Trend")
    st.write("This section shows how sales, profit, and margin changed over time.")

    if not filtered_monthly_summary.empty:
        fig_sales = px.line(
            filtered_monthly_summary,
            x="year_month",
            y="sales",
            markers=True,
            title="Monthly Sales Trend"
        )
        st.plotly_chart(fig_sales, use_container_width=True)

        fig_profit = px.line(
            filtered_monthly_summary,
            x="year_month",
            y="gross_profit",
            markers=True,
            title="Monthly Profit Trend"
        )
        st.plotly_chart(fig_profit, use_container_width=True)

        fig_margin = px.line(
            filtered_monthly_summary,
            x="year_month",
            y="gross_margin_pct",
            markers=True,
            title="Monthly Margin % Trend"
        )
        st.plotly_chart(fig_margin, use_container_width=True)

    st.markdown("### Division Summary Table")
    st.dataframe(filtered_division_summary, use_container_width=True)

# -------------------------------------------------
# TAB 2 - PRODUCT PERFORMANCE
# -------------------------------------------------
with tab2:
    st.markdown("### Top Products by Profit")
    st.write("These products contribute the most total profit.")

    if not filtered_product_summary.empty:
        top_profit_products = filtered_product_summary.sort_values("gross_profit", ascending=False).head(10)
        fig_top_profit = px.bar(
            top_profit_products,
            x="gross_profit",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Profit"
        )
        fig_top_profit.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_top_profit, use_container_width=True)

        st.markdown("### Top Products by Margin %")
        st.write("These products have the strongest profit quality compared with sales.")

        top_margin_products = filtered_product_summary.sort_values("gross_margin_pct", ascending=False).head(10)
        fig_top_margin = px.bar(
            top_margin_products,
            x="gross_margin_pct",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Margin %"
        )
        fig_top_margin.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_top_margin, use_container_width=True)

        st.markdown("### Sales vs Margin")
        st.write("Products on high sales but low margin need attention.")

        fig_scatter = px.scatter(
            filtered_product_summary,
            x="sales",
            y="gross_margin_pct",
            size="gross_profit",
            color="division",
            hover_name="product_name",
            title="Sales vs Margin %"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("### Product Table")
        st.dataframe(
            filtered_product_summary.sort_values("gross_profit", ascending=False),
            use_container_width=True
        )

# -------------------------------------------------
# TAB 3 - DIVISION PERFORMANCE
# -------------------------------------------------
with tab3:
    st.markdown("### Division-Level Comparison")
    st.write("This section compares which divisions drive revenue and which divisions drive profit.")

    if not filtered_division_summary.empty:
        fig_div_sales = px.bar(
            filtered_division_summary,
            x="division",
            y="sales",
            color="division",
            title="Sales by Division"
        )
        st.plotly_chart(fig_div_sales, use_container_width=True)

        fig_div_profit = px.bar(
            filtered_division_summary,
            x="division",
            y="gross_profit",
            color="division",
            title="Profit by Division"
        )
        st.plotly_chart(fig_div_profit, use_container_width=True)

        fig_div_margin = px.bar(
            filtered_division_summary,
            x="division",
            y="gross_margin_pct",
            color="division",
            title="Margin % by Division"
        )
        st.plotly_chart(fig_div_margin, use_container_width=True)

        compare_df = filtered_division_summary.melt(
            id_vars="division",
            value_vars=["revenue_contribution_pct", "profit_contribution_pct"],
            var_name="metric",
            value_name="value"
        )

        fig_compare = px.bar(
            compare_df,
            x="division",
            y="value",
            color="metric",
            barmode="group",
            title="Revenue Contribution vs Profit Contribution"
        )
        st.plotly_chart(fig_compare, use_container_width=True)

        st.dataframe(filtered_division_summary, use_container_width=True)

# -------------------------------------------------
# TAB 4 - PROFIT CONCENTRATION
# -------------------------------------------------
with tab4:
    st.markdown("### Revenue and Profit Concentration")
    st.write("This section shows whether a small number of products drive most of the business.")

    if not filtered_product_summary.empty:
        pareto_revenue_filtered = filtered_product_summary.sort_values("sales", ascending=False).reset_index(drop=True)
        pareto_revenue_filtered["cumulative_sales"] = pareto_revenue_filtered["sales"].cumsum()
        pareto_revenue_filtered["cumulative_sales_pct"] = (
            pareto_revenue_filtered["cumulative_sales"] / pareto_revenue_filtered["sales"].sum()
        ) * 100

        fig_pareto_rev = px.bar(
            pareto_revenue_filtered,
            x=pareto_revenue_filtered.index,
            y="sales",
            title="Revenue Concentration"
        )
        fig_pareto_rev.add_scatter(
            x=pareto_revenue_filtered.index,
            y=pareto_revenue_filtered["cumulative_sales_pct"],
            mode="lines+markers",
            name="Cumulative Revenue %"
        )
        st.plotly_chart(fig_pareto_rev, use_container_width=True)

        revenue_80_count = (pareto_revenue_filtered["cumulative_sales_pct"] <= 80).sum()
        st.metric("Products contributing 80% of Revenue", revenue_80_count)

        pareto_profit_filtered = filtered_product_summary.sort_values("gross_profit", ascending=False).reset_index(drop=True)
        pareto_profit_filtered["cumulative_profit"] = pareto_profit_filtered["gross_profit"].cumsum()
        pareto_profit_filtered["cumulative_profit_pct"] = (
            pareto_profit_filtered["cumulative_profit"] / pareto_profit_filtered["gross_profit"].sum()
        ) * 100

        fig_pareto_profit = px.bar(
            pareto_profit_filtered,
            x=pareto_profit_filtered.index,
            y="gross_profit",
            title="Profit Concentration"
        )
        fig_pareto_profit.add_scatter(
            x=pareto_profit_filtered.index,
            y=pareto_profit_filtered["cumulative_profit_pct"],
            mode="lines+markers",
            name="Cumulative Profit %"
        )
        st.plotly_chart(fig_pareto_profit, use_container_width=True)

        profit_80_count = (pareto_profit_filtered["cumulative_profit_pct"] <= 80).sum()
        st.metric("Products contributing 80% of Profit", profit_80_count)

# -------------------------------------------------
# TAB 5 - RECOMMENDED ACTIONS
# -------------------------------------------------
with tab5:
    st.markdown("### Suggested Business Actions")
    st.write("This section turns analysis into simple action points for decision-making.")

    if not filtered_product_summary.empty:
        sales_threshold = filtered_product_summary["sales"].median()
        margin_threshold_dynamic = filtered_product_summary["gross_margin_pct"].median()
        profit_threshold = filtered_product_summary["gross_profit"].median()
        filtered_product_summary["cost_ratio"] = filtered_product_summary["cost"] / filtered_product_summary["sales"]
        cost_ratio_threshold = filtered_product_summary["cost_ratio"].median()

        def get_action(row):
            if row["sales"] >= sales_threshold and row["gross_margin_pct"] < margin_threshold_dynamic:
                return "Reprice"
            elif row["cost_ratio"] > cost_ratio_threshold and row["gross_margin_pct"] < margin_threshold_dynamic:
                return "Renegotiate Cost"
            elif row["gross_margin_pct"] >= margin_threshold_dynamic and row["sales"] < sales_threshold:
                return "Promote"
            elif row["sales"] < sales_threshold and row["gross_profit"] < profit_threshold:
                return "Discontinue Review"
            else:
                return "Monitor"

        filtered_product_summary["recommended_action"] = filtered_product_summary.apply(get_action, axis=1)

        st.markdown("#### Reprice")
        st.write("Products with strong sales but weak margin.")
        st.dataframe(
            filtered_product_summary[filtered_product_summary["recommended_action"] == "Reprice"]
            .sort_values("sales", ascending=False),
            use_container_width=True
        )

        st.markdown("#### Renegotiate Cost")
        st.write("Products where cost is too high compared with sales.")
        st.dataframe(
            filtered_product_summary[filtered_product_summary["recommended_action"] == "Renegotiate Cost"]
            .sort_values("cost_ratio", ascending=False),
            use_container_width=True
        )

        st.markdown("#### Promote")
        st.write("Products with good margin but lower sales.")
        st.dataframe(
            filtered_product_summary[filtered_product_summary["recommended_action"] == "Promote"]
            .sort_values("gross_margin_pct", ascending=False),
            use_container_width=True
        )

        st.markdown("#### Discontinue Review")
        st.write("Products with low sales and weak profit performance.")
        st.dataframe(
            filtered_product_summary[filtered_product_summary["recommended_action"] == "Discontinue Review"]
            .sort_values("gross_profit", ascending=True),
            use_container_width=True
        )

# -------------------------------------------------
# TAB 6 - FACTORY PERFORMANCE
# -------------------------------------------------
with tab6:
    st.markdown("### Factory Performance")
    st.write("This section shows which factories contribute the most profit and margin.")

    if not filtered_factory_summary.empty:
        fig_factory_profit = px.bar(
            filtered_factory_summary,
            x="factory",
            y="gross_profit",
            color="factory",
            title="Profit by Factory"
        )
        st.plotly_chart(fig_factory_profit, use_container_width=True)

        fig_factory_margin = px.bar(
            filtered_factory_summary,
            x="factory",
            y="gross_margin_pct",
            color="factory",
            title="Margin % by Factory"
        )
        st.plotly_chart(fig_factory_margin, use_container_width=True)

        st.dataframe(filtered_factory_summary, use_container_width=True)

# -------------------------------------------------
# TAB 7 - FORECAST
# -------------------------------------------------
with tab7:
    st.markdown("### Future Trend Forecast")
    st.write("This section uses machine learning to estimate future sales and profit trends.")

    if not monthly_model.empty:
        st.markdown("#### Actual vs Predicted Sales")
        if "predicted_sales" in monthly_model.columns:
            sales_compare = monthly_model[["year_month", "sales", "predicted_sales"]].copy()
            fig_sales_model = px.line(
                sales_compare,
                x="year_month",
                y=["sales", "predicted_sales"],
                markers=True,
                title="Actual Sales vs Model Estimated Sales"
            )
            st.plotly_chart(fig_sales_model, use_container_width=True)

        st.markdown("#### Actual vs Predicted Profit")
        if "predicted_profit" in monthly_model.columns:
            profit_compare = monthly_model[["year_month", "gross_profit", "predicted_profit"]].copy()
            fig_profit_model = px.line(
                profit_compare,
                x="year_month",
                y=["gross_profit", "predicted_profit"],
                markers=True,
                title="Actual Profit vs Model Estimated Profit"
            )
            st.plotly_chart(fig_profit_model, use_container_width=True)

    if not sales_forecast.empty:
        st.markdown("#### Next 6 Months Sales Forecast")
        fig_future_sales = px.line(
            sales_forecast,
            x="year_month",
            y="predicted_sales",
            markers=True,
            title="Future Sales Forecast"
        )
        st.plotly_chart(fig_future_sales, use_container_width=True)
        st.dataframe(sales_forecast, use_container_width=True)

    if not profit_forecast.empty and "predicted_profit" in profit_forecast.columns:
        st.markdown("#### Next 6 Months Profit Forecast")
        fig_future_profit = px.line(
            profit_forecast,
            x="year_month",
            y="predicted_profit",
            markers=True,
            title="Future Profit Forecast"
        )
        st.plotly_chart(fig_future_profit, use_container_width=True)
        st.dataframe(profit_forecast, use_container_width=True)