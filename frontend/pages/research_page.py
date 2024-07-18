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
    st.title("Research Report")
    st.write("This is the research report page.")

    if 'refresh_token' not in st.session_state:
        st.error("Please log in to access the chat page.")
        return

    # Show market research reports history
    if st.session_state.refresh_token:
        headers = set_cookie_in_header(st.session_state.refresh_token)
        try:
            response = requests.get(GET_REPORT_URL, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            reports = response.json()
            if reports:
                report_titles = [report["query"] for report in reports]
                selected_report = st.selectbox(label="Select a Research Report",
                    options=report_titles.append(None))
                if selected_report:
                    report_details = next(
                        report for report in reports if report["query"] == selected_report)
                    st.write(report_details['report'])
            else:
                st.write("No reports available.")
        except requests.RequestException as e:
            st.error(f"Failed to fetch reports: {e}")
    else:
        st.warning("Please enter your refresh token to view reports.")
