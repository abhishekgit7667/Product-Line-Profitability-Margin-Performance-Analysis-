
# Nassau Candy Product Line Profitability & Margin Performance Analysis

## 📌 Project Overview
This project analyzes product-level profitability and margin performance for Nassau Candy Distributor. The objective is to move beyond revenue-based analysis and identify which products and divisions generate real financial value. The project combines data analytics, business intelligence, and machine learning to provide actionable insights for pricing, cost optimization, and product portfolio decisions.

---

## 🎯 Business Problem
In many distribution businesses, high sales volume does not always translate into high profit. Some products generate large revenue but have weak margins due to high costs or inefficient pricing.

This project addresses key business questions:
- Which products truly drive profit?
- Which products are high-sales but low-margin?
- Which divisions are financially efficient?
- Where should pricing, promotion, or cost optimization be applied?

---

## ⚙️ Project Workflow

### Phase 1 – Project Setup
- Designed structured folder architecture
- Organized data, notebooks, outputs, and dashboard components
- Set up environment for scalable development

### Phase 2 – Data Cleaning & Validation
- Standardized column names
- Converted data types (dates, numeric values)
- Handled missing values and removed invalid records
- Validated profit consistency (Sales - Cost = Gross Profit)

### Phase 3 – Feature Engineering
Created key business metrics:
- Gross Margin (%)
- Profit per Unit
- Sales per Unit
- Cost per Unit
- Cost Ratio
- Markup Percentage

### Phase 4 – Aggregation & Analysis
- Product-level profitability analysis
- Division-level performance comparison
- Monthly trend analysis
- Factory-level contribution analysis

### Phase 5 – Advanced Analysis & Visualization
- Top profit products
- Top margin products
- Sales vs Margin analysis
- Revenue vs Profit imbalance
- Cost-heavy product identification
- Pareto analysis (80/20 rule)

### Phase 6 – Insight & Recommendation Framework
- Repricing candidates
- Promotion candidates
- Cost renegotiation candidates
- Discontinuation review candidates
- Action-based product segmentation

### Phase 7 – Streamlit Dashboard
Developed an interactive dashboard with:
- KPI summary cards
- Product performance analysis
- Division comparison
- Pareto analysis
- Recommendation tables
- Factory performance view
- User filters (date, division, product search, margin threshold)

### Phase 8 – Machine Learning Integration
- Linear Regression model for:
  - Sales forecasting
  - Profit forecasting
- K-Means clustering for:
  - Product segmentation based on sales, profit, and margin
- Integrated forecast visualization into dashboard

---

## 📊 Key Business Insights
- High sales does not always imply high profitability
- Profit is concentrated in a small number of products (Pareto effect)
- Some divisions generate high revenue but low profit
- Cost-heavy products significantly reduce margin
- High-margin products exist but are under-promoted

---

## 💡 Business Recommendations
- Reprice high-sales low-margin products
- Promote high-margin low-sales products
- Renegotiate cost-heavy products
- Review low-performing products for discontinuation
- Reduce dependency on limited high-profit products

---

## 🤖 Machine Learning Contribution
- Forecasted future sales and profit trends using Linear Regression
- Applied clustering (K-Means) for data-driven product segmentation
- Added predictive layer to support business planning decisions

---

## 🖥️ Dashboard Features
- Interactive filters (date, division, product search)
- KPI cards for quick insights
- Product and division performance visualization
- Pareto charts for concentration analysis
- Actionable recommendation tables
- Forecast visualization (future sales & profit)

---

## 🛠️ Tools & Technologies
- Python
- Pandas
- NumPy
- Matplotlib / Seaborn
- Plotly
- Streamlit
- Scikit-learn

---

## 📁 Project Structure

nassau_profitability_project/
│
├── data/
│ ├── raw/
│ ├── processed/
│ └── mapping/
│
├── notebooks/
│
├── outputs/
│ ├── charts/
│ └── tables/
│
├── app/
│ └── streamlit_app.py
│
├── README.md
└── requirements.txt


---

## 🚀 How to Run the Project

1. Install dependencies:
```bash
pip install -r requirements.txt

streamlit run app/streamlit_app.py

📌 Future Enhancements
- Use advanced time-series models (ARIMA, Prophet)
- Add real-time data integration
- Deploy dashboard on cloud (Streamlit Cloud / AWS)
- Add user authentication and role-based access
- Enhance UI/UX for business users

👨‍💻 Author

Abhishek Singh
MCA Final Year Student
Data Science Enthusiast


