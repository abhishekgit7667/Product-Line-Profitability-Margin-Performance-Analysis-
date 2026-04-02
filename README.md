# Nassau Candy Product Profitability & Margin Analysis

## Project Overview
This project analyzes product line profitability and margin performance for Nassau Candy Distributor. The objective is to identify which products and divisions truly drive profit, detect high-sales low-margin products, evaluate cost efficiency, and build an interactive Streamlit dashboard for business decision-making.

## Key Objectives
- Analyze product-level profitability
- Compare division-level revenue and profit performance
- Calculate gross margin and profit per unit
- Perform Pareto analysis for revenue and profit concentration
- Identify margin-risk and cost-heavy products
- Build a Streamlit dashboard for interactive analysis

## Project Structure
- `data/raw/` : Original dataset
- `data/processed/` : Cleaned and transformed data
- `data/mapping/` : Factory mapping and coordinates
- `notebooks/` : Jupyter notebooks
- `src/` : Python scripts
- `app/` : Streamlit dashboard
- `outputs/` : Charts, tables, and model outputs
- `report/` : Final internship report
- `presentation/` : Final PPT

## Tools Used
- Python
- Pandas
- NumPy
- Matplotlib / Plotly
- Streamlit
- Scikit-learn

## Status
Phase 1 completed: Folder setup and project initialization.

Phase 2 completed : Completed data preprocessing for the project by handling missing values, resolving merge mismatches, and ensuring data consistency. Non-critical fields such as factory and location were filled appropriately to avoid data loss. The dataset is now clean and ready for further analysis and modeling.

phase 3 Completed : Feature Engineering Completed(Feature engineering was performed to create key profitability metrics such as Gross Margin (%), Profit per Unit, Sales per Unit, Cost per Unit, Cost Ratio, and Markup %. Risk indicators like Margin Risk and Cost Efficiency flags were added to identify underperforming products. Additionally, products were segmented into Star Products, High Sales–Low Margin, High Margin–Low Sales, and Low Performers, enabling deeper business insights and decision-making.)

phase 4 Completed : Aggregation and Business analysis (The dataset was aggregated at product, division, and monthly levels to generate key business insights. Product-level analysis included sales, cost, profit, and margin metrics with ranking and segmentation (e.g., Star Products, High Sales–Low Margin). Division-level analysis identified performance and revenue-profit gaps, while monthly and factory-level aggregations enabled trend and operational performance analysis.)

