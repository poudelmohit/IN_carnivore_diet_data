from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Indiana Carnivore Diet Data", page_icon="🗺️", layout="wide")

DEFAULT_DATA_FILE = Path(__file__).with_name("IN_final_prey_result.csv")
METADATA_COLUMNS = {"sample_id", "latitude", "longitude", "region_id", "region", "donor"}

PREY_SCIENTIFIC_NAMES = {
    "Eagles/hawks/kites": "Accipitridae",
    "Spotted sandpiper": "Actitis_macularius",
    "Western grebe": "Aechmophorus_occidentalis",
    "Mandarin duck": "Aix_galericulata",
    "Wood duck": "Aix_sp.",
    "Mole salamanders": "Ambystoma_sp.",
    "Mallards": "Anas_sp.",
    "Ducks/Geese/Swans": "Anatidae",
    "NA toads": "Anaxyrus_sp.",
    "Greylag goose": "Anser_anser",
    "Chuck-will's-widow": "Antrostomus_carolinensis",
    "Frog/Toads": "Anura",
    "Americab bullfrog": "Aquarana_catesbeiana",
    "Even-hoofed ungulates": "Artiodactyla",
    "Birds": "Aves",
    "Greater scaup": "Aythya_marila",
    "Northern short-tailed shrew": "Blarina_brevicauda",
    "Cattle": "Bos_taurus",
    "Common goldeneye": "Bucephala_clangula",
    "Rough-legged hawk": "Buteo_lagopus",
    "Red-shouldered hawk": "Buteo_lineatus",
    "Broad-winged hawk": "Buteo_platypterus",
    "Raptors": "Buteo_sp.",
    "Northern cardinal": "Cardinalis_cardinalis",
    "North American beaver": "Castor_canadensis",
    "Veery": "Catharus_fuscescens",
    "Thrushes": "Catharus_sp.",
    "Killdeer": "Charadrius_vociferus",
    "Common nighthawk": "Chordeiles_minor",
    "Southern redbelly dace": "Chrosomus_erythrogaster",
    "Northern bobwhite": "Colinus_virginianus",
    "Doves": "Columbidae",
    "Common raven": "Corvus_corax",
    "Japanese quail": "Coturnix_japonica",
    "New world mice and rats": "Cricetidae",
    "North American least shrew": "Cryptotis_parvus",
    "Trumpeter swan": "Cygnus_buccinator",
    "Mute swan": "Cygnus_olor",
    "Cypriniformes": "Cypriniformes",
    "Virginia opossum": "Didelphis_virginiana",
    "Emydidae": "Emydidae",
    "Horned lark": "Eremophila_alpestris",
    "American coot": "Fulica_americana",
    "Landfowl": "Galliformes",
    "Chicken": "Gallus_gallus",
    "Southern flying squirrel": "Glaucomys_volans",
    "Evening grosbeak": "Hesperiphona_vespertina",
    "Swallows": "Hirundinidae",
    "Barn swallow": "Hirundo_rustica",
    "Ictalurids": "Ictaluridae",
    "Thirteen-lined ground squirrel": "Ictidomys_tridecemlineatus",
    "Mississippi kite": "Ictinia_mississippiensis",
    "Loggerhead shrike": "Lanius_ludovicianus",
    "Seabirds": "Laridae",
    "Rabbits/Hares": "Leporidae",
    "NA River otter": "Lontra_canadensis",
    "Groundhog": "Marmota_monax",
    "Melanerpes woodpecker": "Melanerpes",
    "Wild turkey": "Meleagris_gallopavo",
    "Song sparrow": "Melospiza_melodia",
    "Prairie vole": "Microtus_ochrogaster",
    "Meadow vole": "Microtus_pennsylvanicus",
    "Woodland vole": "Microtus_pinetorum",
    "Voles": "Microtus_sp.",
    "Old World mice and rats": "Muridae",
    "House mouse": "Mus_musculus",
    "Least weasel": "Mustela_nivalis",
    "Weasels": "Mustelidae",
    "Long-tailed weasel": "Neogale_frenata",
    "Weasel/mink": "Neogale_sp.",
    "Helmeted guineafowl": "Numida_meleagris",
    "White-tailed deer": "Odocoileus_sp.",
    "Common Muskrat": "Ondatra_zibethicus",
    "European rabbit": "Oryctolagus_cuniculus",
    "Ruddy duck": "Oxyura_jamaicensis",
    "Osprey": "Pandion_haliaetus",
    "Warblers": "Parulidae",
    "True sparrows": "Passer_sp.",
    "New World sparrows": "Passerellidae",
    "Passerines": "Passeriformes",
    "White-footed mouse": "Peromyscus_leucopus",
    "Deermice": "Peromyscus_sp.",
    "Pheasants": "Phasianidae",
    "Ring-necked pheasant": "Phasianus_colchicus",
    "Woodpeckers": "Picidae",
    "Pine grosbeak": "Pinicola_enucleator",
    "Roseate spoonbill": "Platalea_ajaja",
    "Horned grebe": "Podiceps_auritus",
    "Eared grebe": "Podiceps_nigricollis",
    "Grebes": "Podicipedidae",
    "Pied-billed grebe": "Podilymbus_podiceps",
    "Northern Raccoon": "Procyon_lotor",
    "Frogs": "Ranidae",
    "Norway rat": "Rattus_norvegicus",
    "Rodents": "Rodentia",
    "Squirrels (family)": "Sciuridae",
    "Eastern gray squirrel": "Sciurus_carolinensis",
    "Fox squirrel": "Sciurus_niger",
    "Squirrels": "Sciurus_sp.",
    "Shorebirds": "Scolopacidae",
    "Masked shrew": "Sorex_cinereus",
    "Shrews": "Soricidae",
    "Chipping sparrow": "Spizella_passerina",
    "Eurasian collared-dove": "Streptopelia_decaocto",
    "Meadowlarks": "Sturnella_sp.",
    "European starling": "Sturnus_vulgaris",
    "Wild boar": "Sus_scrofa",
    "Eastern cottontail": "Sylvilagus_floridanus",
    "Southern bog lemming": "Synaptomys_cooperi",
    "Eastern chipmunk": "Tamias_striatus",
    "Red squirrel": "Tamiasciurus_hudsonicus",
    "American Badger": "Taxidea_taxus",
    "Pond slider": "Trachemys_scripta",
    "Willet": "Tringa_semipalmata",
    "Trhushes": "Turdidae",
    "American robin": "Turdus_migratorius",
    "Red-eyed vireo": "Vireo_olivaceus",
    "White-winged dove": "Zenaida_asiatica",
}


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
    detected = []
    for column in prey_columns:
        if row[column] > 0:
            scientific_name = PREY_SCIENTIFIC_NAMES.get(column)
            if scientific_name:
                display_name = scientific_name.replace("_", " ")
                detected.append(f"{column} (<i>{display_name}</i>)")
            else:
                detected.append(column)
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
        help="Choose prey items to keep samples where those prey are detected (> 0).",
    )

    if selected_prey:
        prey_match_mode = st.radio(
            "Selected prey must match",
            ["Any selected prey", "All selected prey"],
            horizontal=False,
        )
    else:
        prey_match_mode = "Any selected prey"

    point_size = st.slider("Map point size", 5, 20, 10)

filtered = data[
    data["donor"].astype(str).isin(selected_donors)
    & data["region"].astype(str).isin(selected_regions)
].copy()

if selected_prey:
    prey_matches = filtered[selected_prey].gt(0)
    if prey_match_mode == "All selected prey":
        filtered = filtered[prey_matches.all(axis=1)].copy()
    else:
        filtered = filtered[prey_matches.any(axis=1)].copy()

filtered["non_zero_prey"] = filtered.apply(
    make_prey_summary,
    axis=1,
    prey_columns=prey_columns,
)

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
    labels={"non_zero_prey": "Detected prey"},
    hover_data={
        "region": True,
        "donor": True,
        "non_zero_prey": True,
        "latitude": False,
        "longitude": False,
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
