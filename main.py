import streamlit as st
from prediction_helper_01 import predict  # Ensure this is correctly linked to your prediction_helper.py
import plotly.graph_objects as go


# Set the page configuration and title
st.set_page_config(page_title="Credit Risk Modelling", page_icon="📊")
st.title("Credit Risk Modelling 💳")
st.info("Loan Underwriting • Default Risk Assessment • Credit Scoring")

# Create rows of three columns each
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# Assign inputs to the first row with default values
with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28)
with row1[1]:
    income = st.number_input('Income', min_value=0, value=1200000)
with row1[2]:
    loan_amount = st.number_input('Loan Amount', min_value=0, value=2560000)

# Calculate Loan to Income Ratio and display it
loan_to_income_ratio = loan_amount / income if income > 0 else 0
with row2[0]:
    st.text("Loan to Income Ratio:")
    st.text(f"{loan_to_income_ratio:.2f}")  # Display as a text field

# Assign inputs to the remaining controls
with row2[1]:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
with row2[2]:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20)

with row3[0]:
    delinquency_ratio = st.number_input('Deliquency Ratio', min_value=0, max_value=100, step=1, value=30)
with row3[1]:
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0, max_value=100, step=1, value=30)
with row3[2]:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)


with row4[0]:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
with row4[2]:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])


# Button to calculate risk
if st.button('Calculate Risk'):
    # Call the predict function from the helper module
    # print((age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
    #                                             delinquency_ratio, credit_utilization_ratio, num_open_accounts,
    #                                             residence_type, loan_purpose, loan_type))
    probability, credit_score, rating = predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                                                delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                                                residence_type, loan_purpose, loan_type)

    # Create main layout
    left_col, right_col = st.columns([3, 2])

    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        st.metric(
            "Default Probability",
            f"{probability:.2%}"
        )

    with col2:
        st.metric(
            "Credit Score",
            credit_score
        )

    with col3:
        st.metric(
            "Rating",
            rating
        )
        if rating == "Poor":
            st.error("🚫 High Risk Borrower")
        elif rating == "Average":
            st.warning("⚠ Manual Review Recommended")
        elif rating == "Good":
            st.info("✓ Eligible for Review")
        else:
            st.success("✅ Strong Borrower Profile")

    with col4:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=credit_score,

            title={'text': "Credit Score"},

            gauge={
                'axis': {'range': [300, 900]},

                'bar': {
                    'color': "black",
                    'thickness': 0.2
                },

                'steps': [
                    {'range': [300, 500], 'color': "#dc2626"},
                    {'range': [500, 650], 'color': "#f59e0b"},
                    {'range': [650, 750], 'color': "#3b82f6"},
                    {'range': [750, 900], 'color': "#16a34a"}
                ],

                'threshold': {
                    'line': {'color': "black", 'width': 8},
                    'thickness': 0.75,
                    'value': credit_score
                }
            }
        ))

        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={'displayModeBar': False}
        )

    # fig = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=credit_score,
    #
    #     title={'text': "Credit Score"},
    #
    #     gauge={
    #         'axis': {'range': [300, 900]},
    #
    #         'bar': {
    #             'color': "black",
    #             'thickness': 0.2
    #         },
    #
    #         'steps': [
    #             {'range': [300, 500], 'color': "#dc2626"},
    #             {'range': [500, 650], 'color': "#f59e0b"},
    #             {'range': [650, 750], 'color': "#3b82f6"},
    #             {'range': [750, 900], 'color': "#16a34a"}
    #         ],
    #
    #         'threshold': {
    #             'line': {'color': "black", 'width': 8},
    #             'thickness': 0.75,
    #             'value': credit_score
    #         }
    #     }
    # ))
    #
    # fig.update_layout(
    #     height=100,  # Reduce size
    #     margin=dict(l=10, r=10, t=30, b=10)
    # )
    #
    # st.plotly_chart(fig, use_container_width=True)
    #
    # col1, col2, col3 = st.columns(3)
    #
    # with col1:
    #     st.metric("Default Probability", f"{probability:.2%}")
    #
    # with col2:
    #     st.metric("Credit Score", credit_score)
    #
    # with col3:
    #     st.metric("Rating", rating)
    # # Display additional results
    # st.write(f"Default Probability: {probability:.2%}")
    # st.write(f"Credit Score: {credit_score}")
    # st.write(f"Rating: {rating}")

    # # Display the results
    # st.write(f"Deafult Probability: {probability:.2%}")
    # st.write(f"Credit Score: {credit_score}")
    # st.write(f"Rating: {rating}")

# Footer
# st.markdown('_Project From Codebasics ML Course_')
