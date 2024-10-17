# dataset-dashboard-rhuan

This is a web-based Sales Dashboard application built with Dash and Plotly. It allows users to visualize sales data through various interactive charts and graphs, providing insights into sales performance, customer types, and payment methods.

<Features>
Total Sales Over Time: Interactive area chart displaying total sales over a period.
Total Sales by Product Line: Bar chart showing sales distribution across different product lines.
Total Sales by City: Bar chart visualizing sales across different cities.
Customer Type Distribution: Pie chart illustrating the distribution of sales by customer type.
Payment Method Distribution: Pie chart showing sales by payment methods.
KPI Cards: Key metrics such as total sales, total gross income, and average customer rating.

Getting Started
To run this application locally, follow these steps:

1. Clone the Repository
git clone <repository-url>
cd <repository-folder>
Replace <repository-url> and <repository-folder> with the actual repository link and folder name.

Prerequisites
To run this application, you'll need to install the following dependencies:

Dash
Dash Bootstrap Components
Pandas
Plotly
You can install these dependencies using pip.

2. Install Dependencies
Make sure you have Python installed on your system. You can then install the required dependencies:

pip install dash dash-bootstrap-components pandas plotly

3. Run the Application
Once the dependencies are installed, you can run the app using the following command:

python python sales_dashboard_improved.py
This will start a local web server. Open your browser and navigate to http://127.0.0.1:8050/ to view the dashboard.

4. Data Requirements
Ensure that you have the dataset sales_uk.csv in the same directory as they Python code.

The dataset should contain columns like Date, Total, gross income, Rating, Product line, City, Customer_type, and Payment to ensure proper functionality of the app.

Application Structure

KPIs: Displays total sales, total gross income, and the average customer rating.

Interactive Charts:
Sales Over Time: Shows total daily sales in an area chart.
Sales by Product Line: Bar chart representing sales across different product lines.
Sales by City: Bar chart representing sales performance by city.
Customer & Payment Insights: Pie charts to provide insights into customer types and payment methods.
Instructions Modal: A detailed guide to navigating the dashboard, which can be accessed by clicking the "Instructions" button.

Usage
Click the navigation buttons at the top to explore specific visualizations.
The Instructions button provides a pop-up with guidance on how to use the dashboard.

Thank you, bye
