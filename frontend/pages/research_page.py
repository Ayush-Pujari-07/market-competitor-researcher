import streamlit as st
import requests

CREATE_REPORT_URL = "http://localhost:9000/research/report/create"
GET_REPORT_URL = "http://localhost:9000/research/get_all"

def set_cookie_in_header(refresh_token):
    from http.cookies import SimpleCookie  # type: ignore
    cookies = SimpleCookie()
    cookies["refreshToken"] = refresh_token
    cookie_header = cookies.output(header="", sep=";").strip()
    return {"Cookie": cookie_header}

def research_report():
    st.title("Your Research Reports")

    if 'refresh_token' not in st.session_state:
        st.error("Please log in to access the chat page.")
        return

    refresh_token = st.session_state.refresh_token
    headers = set_cookie_in_header(refresh_token)

    try:
        response = requests.get(GET_REPORT_URL, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        reports = response.json()
        report_titles = [report["query"] for report in reports] if reports else []

        selected_report = st.selectbox("Select a Research Report", [""] + report_titles)

        if selected_report:
            report_details = next(report for report in reports if report["query"] == selected_report)
            st.write(report_details['report'])
        else:
            st.title("Start New Research Report")
            industry = st.text_input("Enter the industry")
            company = st.text_input("Enter the company")
            competitors = st.text_area("Enter competitors (comma-separated)").split(',')
            market_research = st.checkbox("Market Research")
            competitor_research = st.checkbox("Competitor Research")

            if st.button("Create Report"):
                new_report = {
                    "industry": industry,
                    "company": company,
                    "competitors": competitors,
                    "market_research": market_research,
                    "competitor_research": competitor_research
                }
                create_report(new_report, headers)

    except requests.RequestException as e:
        st.error(f"Failed to fetch reports: {e}")

def create_report(report_request, headers):
    try:
        response = requests.post(CREATE_REPORT_URL, json=report_request, headers=headers)
        response.raise_for_status()
        report = response.json()
        st.write(report['report']['report'])
        st.success("Report created successfully!")
    except requests.RequestException as e:
        st.error(f"Failed to create report: {e}")