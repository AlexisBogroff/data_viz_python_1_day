import io
import zipfile
from typing import Optional

import pandas as pd
import requests
import streamlit as st

import pydeck as pdk


DATA_URL = "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20251018-234902/valeursfoncieres-2025-s1.txt.zip"


@st.cache_data(show_spinner=True)
def download_and_load(url: str) -> pd.DataFrame:
    """Download the zipped DVF file and return a pandas DataFrame.

    The function attempts common separators ('|', ';', '\t') and encodings.
    """
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    bio = io.BytesIO(resp.content)
    with zipfile.ZipFile(bio) as z:
        # pick the largest text file in the archive
        candidates = [n for n in z.namelist() if n.lower().endswith((".txt", ".csv"))]
        if not candidates:
            raise RuntimeError("No .txt or .csv file found in archive")
        # choose largest candidate
        target = max(candidates, key=lambda n: z.getinfo(n).file_size)
        with z.open(target) as fh:
            raw = fh.read()

    # try decoding and delimiter detection
    for encoding in ("utf-8", "latin-1"):
        text = None
        try:
            text = raw.decode(encoding)
        except Exception:
            continue
        # peek first line
        first_line = text.splitlines()[0]
        for sep in ["|", ";", "\t", ","]:
            if sep in first_line:
                try:
                    df = pd.read_csv(io.StringIO(text), sep=sep, low_memory=False)
                    # minimal sanity check
                    if "valeur_fonciere" in df.columns or "valeur_fonciere" in [c.lower() for c in df.columns]:
                        return df
                    # Accept if latitude/longitude are present
                    if set(["longitude", "latitude"]).issubset(set(df.columns)):
                        return df
                except Exception:
                    continue
    # last resort try pandas automatic (automatic separator detection requires python engine)
    try:
        df = pd.read_csv(io.StringIO(raw.decode("latin-1")), sep=None, engine="python")
        return df
    except Exception as e:
        raise RuntimeError(f"Could not parse file with automatic separator detection: {e}")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # lower-case columns for convenience
    df.columns = [c.strip() for c in df.columns]
    lc = {c: c.lower() for c in df.columns}
    df = df.rename(columns=lc)
    return df


def filter_paris_8(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure columns exist
    df = standardize_columns(df)

    # Normalize important fields
    for col in ("type_local", "libelle_commune", "code_postal", "code_commune"):
        if col not in df.columns:
            df[col] = ""

    # Try multiple strategies to detect Paris 8
    mask_type = df["type_local"].astype(str).str.upper().str.contains("APPART")

    mask_commune_code = df["code_commune"].astype(str).str.strip() == "75108"
    mask_postal = df["code_postal"].astype(str).str.startswith("75008")
    mask_libelle = df["libelle_commune"].astype(str).str.upper().str.contains("PARIS") & (
        df["libelle_commune"].astype(str).str.contains("8")
    )

    mask_geo = mask_commune_code | mask_postal | mask_libelle

    df2 = df[mask_type & mask_geo].copy()

    # Parse numerics
    if "valeur_fonciere" in df2.columns:
        df2["valeur_fonciere"] = (
            df2["valeur_fonciere"].astype(str).str.replace(",", ".").str.replace(" ", "")
        )
        df2["valeur_fonciere"] = pd.to_numeric(df2["valeur_fonciere"], errors="coerce")

    for c in ("longitude", "latitude"):
        if c in df2.columns:
            df2[c] = pd.to_numeric(df2[c], errors="coerce")

    # parse date
    if "date_mutation" in df2.columns:
        df2["date_mutation"] = pd.to_datetime(df2["date_mutation"], errors="coerce", dayfirst=True)
        df2["year"] = df2["date_mutation"].dt.year
    else:
        df2["year"] = pd.NA

    df2 = df2.dropna(subset=["longitude", "latitude", "valeur_fonciere"]) if set(["longitude", "latitude", "valeur_fonciere"]).issubset(df2.columns) else df2

    return df2


def main():
    st.set_page_config(page_title="Immo Paris 8e", layout="wide")
    st.title("Immo — Prix des appartements dans le 8e arrondissement")

    st.markdown(
        "Ce petit outil télécharge les données DVF (valeurs foncières) et affiche les transactions "
        "d'appartements localisés dans le 8e arrondissement de Paris. Le téléchargement peut être volumineux."
    )

    with st.spinner("Téléchargement et traitement des données — ceci peut prendre plusieurs dizaines de secondes..."):
        try:
            df_raw = download_and_load(DATA_URL)
        except Exception as e:
            st.error(f"Impossible de télécharger ou lire les données: {e}")
            return

    df = filter_paris_8(df_raw)

    if df.empty:
        st.warning("Aucune transaction trouvée pour le 8e arrondissement avec les critères actuels.")
        st.stop()

    # sidebar filters
    st.sidebar.header("Filtres")
    years = sorted([int(y) for y in df["year"].dropna().unique()])
    selected_years = st.sidebar.multiselect("Année(s)", years, default=years)

    min_price = int(df["valeur_fonciere"].min())
    max_price = int(df["valeur_fonciere"].quantile(0.99))
    price_slider = st.sidebar.slider("Prix (quantile 99%)", min_price, max_price, (min_price, max_price))

    mask = df["valeur_fonciere"].between(price_slider[0], price_slider[1])
    if selected_years:
        mask = mask & df["year"].isin(selected_years)

    df_filtered = df[mask]

    st.subheader("Synthèse")
    st.write(f"Transactions affichées: **{len(df_filtered)}**")

    # Map
    midpoint = (df_filtered["latitude"].mean(), df_filtered["longitude"].mean())
    st.subheader("Carte des transactions")

    # prepare columns for pydeck
    df_map = df_filtered[["longitude", "latitude", "valeur_fonciere", "date_mutation"].copy()]
    df_map = df_map.rename(columns={"valeur_fonciere": "price", "date_mutation": "date"}).dropna()
    df_map["radius"] = (df_map["price"] / df_map["price"].median()).clip(0.1, 10) * 50

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map,
        pickable=True,
        get_position="[longitude, latitude]",
        get_radius="radius",
        get_fill_color="[255 * (price - @min_price) / (@max_price - @min_price + 1), 100, 140]",
        tooltip=True,
    )

    view_state = pdk.ViewState(latitude=midpoint[0], longitude=midpoint[1], zoom=13)

    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"html": "<b>Prix:</b> {price} €<br><b>Date:</b> {date}", "style": {"backgroundColor": "white"}})

    st.pydeck_chart(r)

    st.subheader("Détail des transactions")
    st.dataframe(df_filtered[["date_mutation", "valeur_fonciere", "adresse_nom_voie", "code_postal", "libelle_commune", "longitude", "latitude"]].rename(columns={"date_mutation": "date", "valeur_fonciere": "prix"}))

    st.caption("Source: data.gouv.fr — demandes de valeurs foncières")


if __name__ == "__main__":
    main()
