import streamlit as st
import requests
import pandas as pd
import os
import cv2

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Missing Person AI",
    layout="wide"
)

st.title("🔍 Missing Person Identification System")

# ---------------- Dashboard ----------------

st.header("📊 Dashboard")

try:
    dashboard = requests.get(
        f"{BACKEND_URL}/dashboard"
    ).json()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Registered Persons",
            dashboard["total_registered"]
        )

    with col2:
        st.metric(
            "Total Searches",
            dashboard["total_searches"]
        )

except Exception:
    st.warning("Backend not running.")

st.divider()

# ---------------- Search ----------------

st.header("🔎 Search Person")

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(
        uploaded_file,
        caption="Uploaded Image",
        width=250
    )

if st.button("Search"):

    if uploaded_file is None:

        st.error("Please upload an image.")

    else:

        response = requests.post(
            f"{BACKEND_URL}/search/",
            files={"file": uploaded_file}
        )

        result = response.json()

        # Uncomment for debugging
        # st.write(result)

        if result["status"] == "error":

            st.error(result["message"])

        elif result["status"] == "no_match":

            st.error("❌ No Match Found")
            st.write("Similarity Score: 0")

        elif result["status"] == "match":

            st.success("✅ Match Found")

            st.subheader("Top Matches")

            for idx, match in enumerate(
                result["matches"],
                start=1
            ):

                st.write(f"### Rank {idx}")
                st.write(f"Name: {match['name']}")
                st.write(
                    f"Score: {match['score']:.4f}"
                )

                image_path = match["image_path"]

                try:

                    if os.path.exists(image_path):

                        img = cv2.imread(image_path)

                        if img is not None:

                            img = cv2.cvtColor(
                                img,
                                cv2.COLOR_BGR2RGB
                            )

                            st.image(
                                img,
                                width=200
                            )

                        else:

                            st.warning(
                                f"Cannot read image:\n{image_path}"
                            )

                    else:

                        st.warning(
                            f"Image not found:\n{image_path}"
                        )

                except Exception as e:

                    st.warning(
                        f"Error displaying image:\n{e}"
                    )

                st.divider()

        else:

            st.warning(
                "Unexpected response from backend."
            )

st.divider()

# ---------------- History ----------------

st.header("🕒 Search History")

if st.button("Load History"):

    history = requests.get(
        f"{BACKEND_URL}/history"
    ).json()

    df = pd.DataFrame(
        history["history"],
        columns=[
            "ID",
            "Person",
            "Result",
            "Score"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )