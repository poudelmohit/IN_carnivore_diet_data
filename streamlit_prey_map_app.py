from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Indiana Carnivore Diet Data", page_icon="🗺️", layout="wide")

DEFAULT_DATA_FILE = Path(__file__).with_name("indiana_final_prey_result.csv")
METADATA_COLUMNS = {"sample_id", "latitude", "longitude", "region_id", "region", "donor"}


@st.cache_data
def load_data(source) -> pd.DataFrame:
    """Load and validate the sample CSV."""
    df = pd.read_csv(source)

    required = {"sample_id", "latitude", "longitude", "region", "donor"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"]).copy()

    prey_columns = [column for column in df.columns if column not in METADATA_COLUMNS]
    for column in prey_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def make_prey_summary(row: pd.Series, prey_columns: list[str]) -> str:
    detected = [
        column
        for column in prey_columns
        if row[column] > 0
    ]
    return "<br>".join(detected) if detected else "No non-zero prey items"


st.title("Indiana Carnivore Diet Data")
st.caption("Filter samples by donor, region, or prey detection, then hover over map points for the full non-zero prey profile.")

with st.sidebar:
    st.header("Data and filters")
    uploaded_file = st.file_uploader("Upload a CSV", type="csv")

source = uploaded_file if uploaded_file is not None else DEFAULT_DATA_FILE

try:
    if uploaded_file is None and not DEFAULT_DATA_FILE.exists():
        st.error(
            f"Place the data file at `{DEFAULT_DATA_FILE.name}` beside this script, "
            "or upload it using the sidebar."
        )
        st.stop()
    data = load_data(source)
except Exception as exc:
    st.error(f"Could not load the CSV: {exc}")
    st.stop()

prey_columns = [column for column in data.columns if column not in METADATA_COLUMNS]

with st.sidebar:
    donor_options = sorted(data["donor"].dropna().astype(str).unique())
    selected_donors = st.multiselect("Donor", donor_options, default=donor_options)

    region_options = sorted(data["region"].dropna().astype(str).unique())
    selected_regions = st.multiselect("Region", region_options, default=region_options)

    selected_prey = st.multiselect(
        "Prey items",
        prey_columns,
        placeholder="Choose one or more prey items",
        help="Choose prey columns to keep samples where those values meet the threshold below.",
    )

    if selected_prey:
        prey_match_mode = st.radio(
            "Selected prey must match",
            ["Any selected prey", "All selected prey"],
            horizontal=False,
        )
        minimum_value = st.number_input(
            "Minimum prey value",
            min_value=0.0,
            value=1.0,
            step=1.0,
            help="A selected prey item matches when its value is at least this amount.",
        )
    else:
        prey_match_mode = "Any selected prey"
        minimum_value = 1.0

    point_size = st.slider("Map point size", 5, 20, 10)

filtered = data[
    data["donor"].astype(str).isin(selected_donors)
    & data["region"].astype(str).isin(selected_regions)
].copy()

if selected_prey:
    prey_matches = filtered[selected_prey].ge(minimum_value)
    if prey_match_mode == "All selected prey":
        filtered = filtered[prey_matches.all(axis=1)].copy()
    else:
        filtered = filtered[prey_matches.any(axis=1)].copy()

filtered["non_zero_prey"] = filtered.apply(
    make_prey_summary,
    axis=1,
    prey_columns=prey_columns,
)
filtered["detected_prey_count"] = filtered[prey_columns].gt(0).sum(axis=1)

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Visible samples", f"{len(filtered):,}")
metric_2.metric("Donors represented", filtered["donor"].nunique())
metric_3.metric("Regions represented", filtered["region"].nunique())

if filtered.empty:
    st.warning("No samples match the current filters.")
    st.stop()

fig = px.scatter_mapbox(
    filtered,
    lat="latitude",
    lon="longitude",
    color="donor",
    color_discrete_map={"coyote": "#F28E2B", "bobcat": "#1F77B4"},
    hover_name="sample_id",
    hover_data={
        "region": True,
        "donor": True,
        "detected_prey_count": True,
        "non_zero_prey": True,
        "latitude": ":.5f",
        "longitude": ":.5f",
    },
    zoom=6,
    height=700,
)
fig.update_traces(marker={"size": point_size, "opacity": 0.8})
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend_title_text="Donor",
)

st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

with st.expander("View filtered sample data"):
    display_columns = [
        "sample_id",
        "latitude",
        "longitude",
        "region",
        "donor",
        "detected_prey_count",
    ] + selected_prey
    st.dataframe(
        filtered[display_columns].sort_values(["region", "donor", "sample_id"]),
        use_container_width=True,
        hide_index=True,
    )

st.download_button(
    "Download filtered samples as CSV",
    data=filtered.drop(columns=["non_zero_prey"]).to_csv(index=False).encode("utf-8"),
    file_name="filtered_prey_samples.csv",
    mime="text/csv",
)


st.divider()
st.header("Acknowledgment")
st.markdown(
    "Funding for this project was provided by the "
    "**Federal Aid in Wildlife Restoration Program (W-134-P-20)** and the "
    "**Indiana Department of Natural Resources (INDR-20000686-050-SUB76186)**."
)
