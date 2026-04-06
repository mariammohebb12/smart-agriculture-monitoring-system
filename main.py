import streamlit.web.bootstrap as bootstrap
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "dashboard.py"]
    bootstrap.run()