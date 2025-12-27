import streamlit as st
import json
import pandas as pd
import os
import base64
import math

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="IPÊ - LCCMat",
    page_icon="assets/logo_lccmat.png", 
    layout="wide"
)

# --- CONSTANTS ---
DB_PATH = "data/master_index.json"
LOGO_PATH = "assets/logo_lccmat_h.png" 

# --- HELPER FUNCTIONS ---
def render_centered_image_base64(image_path, width_px=200):
    if not os.path.exists(image_path):
        if os.path.exists(os.path.basename(image_path)):
            image_path = os.path.basename(image_path)
        else:
            return
    
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{b64_string}" width="{width_px}" style="max-width: 100%;">
        </div>
        """,
        unsafe_allow_html=True
    )

@st.cache_data
def load_database():
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return []

def format_year(val):
    """Limpa o ano para não mostrar 2010.0 ou nan"""
    if val is None:
        return ""
    try:
        # Se for string 'nan' ou float nan
        if isinstance(val, float) and math.isnan(val):
            return ""
        if str(val).lower() == 'nan':
            return ""
        # Tenta converter para inteiro
        return str(int(float(val)))
    except:
        return str(val)

# --- CSS STYLING ---
st.markdown("""
<style>
    /* 1. Header Styles */
    .header-text {
        text-align: center;
        color: #111111;
        font-family: 'Helvetica', sans-serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #555555;
        font-size: 1.1em;
        margin-bottom: 2rem;
    }

    /* 2. Card Styling (Borda e Sombra Forte) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #d1d5db !important; /* Borda cinza visível */
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    /* 3. Tags styling */
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: 600;
        margin-left: 10px;
        vertical-align: middle;
        text-decoration: none;
    }
    .tag-reax { background-color: #e3f2fd; color: #1565c0; border: 1px solid #bbdefb; }
    .tag-eam { background-color: #fce4ec; color: #c2185b; border: 1px solid #f8bbd0; }
    .tag-semi { background-color: #fff3e0; color: #ef6c00; border: 1px solid #ffe0b2; }
    .tag-airebo { background-color: #f3e5f5; color: #7b1fa2; border: 1px solid #e1bee7; }

    /* 4. Fix st.code colors for Light Mode */
    .stCodeBlock {
        border: 1px solid #eeeeee;
        border-radius: 5px;
    }
    /* Força o fundo do código a ser claro e texto escuro */
    code {
        color: #d63384 !important; /* Cor padrão do Streamlit light para inline code */
    }
</style>
""", unsafe_allow_html=True)

def main():
    # --- HEADER SECTION ---
    st.write("")
    render_centered_image_base64(LOGO_PATH, width_px=300)

    _, col_center, _ = st.columns([1, 6, 1])

    with col_center:
        st.markdown("<h1 class='header-text'>Interatomic Potentials Explorer</h1>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>Interactive database for Computational Materials Science</div>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 30px; font-size: 0.9em;'>
                <p style='margin-bottom: 2px;'>Discover the research and publications produced by the LCCMat group:</p>
                <a href='https://lccmat.unb.br/' target='_blank' style='text-decoration: none; color: #0068c9; font-weight: bold;'>
                    Visit LCCMat Official Website (lccmat.unb.br)
                </a>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # --- DATA LOADING ---
        raw_data = load_database()
        if not raw_data:
            st.error("Database is empty. Please run the crawler script.")
            st.stop()
        df = pd.DataFrame(raw_data)

        # --- DATA LOADING ---
        raw_data = load_database()
        if not raw_data:
            st.error("Database is empty. Please run the crawler script.")
            st.stop()
        df = pd.DataFrame(raw_data)

        # =========================================================
        # DASHBOARD COMPACTO (VISUAL MAIS LIMPO)
        # =========================================================
        with st.container(border=True):
            st.subheader("Database Overview")

            # CSS Ajustado para ser mais compacto ("Mini Cards")
            st.markdown("""
            <style>
                div[data-testid="stMetric"] {
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    padding: 16px; 
                    border-radius: 6px;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                    text-align: center;
                    min-height: 80px;
                }
                
                div[data-testid="stMetricLabel"] {
                    justify-content: center;
                    font-size: 0.8rem !important;
                    color: #666;
                }
                
                div[data-testid="stMetricValue"] {
                    justify-content: center;
                    font-size: 1.5rem !important;
                    font-weight: 700;
                    color: #212529;
                }
            </style>
            """, unsafe_allow_html=True)

            type_counts = df['type'].value_counts()
            total = len(df)
            
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                st.metric("Total Potentials", total)
            
            top_types = type_counts.index.tolist()
            
            if len(top_types) >= 1:
                c2.metric(top_types[0], type_counts[top_types[0]])
            if len(top_types) >= 2:
                c3.metric(top_types[1], type_counts[top_types[1]])
            if len(top_types) >= 3:
                c4.metric(top_types[2], type_counts[top_types[2]])

            remaining_types = top_types[3:]
            if remaining_types:
                st.write("")
                cols = st.columns(len(remaining_types)) 
                for i, t_type in enumerate(remaining_types):
                    with cols[i]:
                        st.metric(t_type, type_counts[t_type])

        # =========================================================

        # --- SEARCH FILTERS ---
        with st.container(border=True):
            st.markdown("#### Search Filters")
            
            c1, c2 = st.columns(2)
            
            with c1:
                real_types = sorted(list(set(entry.get('type', 'Unknown') for entry in raw_data)))
                
                options_with_all = ["All"] + real_types
                
                selected_types = st.multiselect(
                    "Physics Model (Force Field Type)",
                    options=options_with_all,
                    default=["All"], 
                    help="Select 'All' to view all types, or remove it to select specific ones."
                )

            with c2:
                all_elements = set()
                for el_list in df['elements']:
                    all_elements.update(el_list)
                
                selected_elements = st.multiselect(
                    "Chemical Elements", 
                    options=sorted(list(all_elements)),
                    placeholder="Select elements (e.g., C, H, Fe)..."
                )
            
            search_logic = st.radio(
                "Element Search Logic", 
                ["Contains ANY of selected", "Contains ALL of selected", "Exact Match"], 
                horizontal=True
            )

    st.divider()

    # --- FILTERING LOGIC ---
    filtered_df = df.copy()
        
    if selected_types:
        if "All" not in selected_types:
            filtered_df = filtered_df[filtered_df['type'].isin(selected_types)]
    else:
        filtered_df = filtered_df[0:0]

    if selected_elements:
        if search_logic == "Contains ANY of selected":
            filtered_df = filtered_df[filtered_df['elements'].apply(lambda x: any(el in selected_elements for el in x))]
        elif search_logic == "Contains ALL of selected":
            filtered_df = filtered_df[filtered_df['elements'].apply(lambda x: all(el in x for el in selected_elements))]
        elif search_logic == "Exact Match":
            req_set = sorted(selected_elements)
            filtered_df = filtered_df[filtered_df['elements'].apply(lambda x: sorted(x) == req_set)]

    # --- RESULTS DISPLAY ---
    _, col_results, _ = st.columns([1, 8, 1])
    
    with col_results:
        c_res, c_count = st.columns([6, 1])
        c_res.subheader("Available Potentials")
        c_count.markdown(f"<h2 style='text-align: right; color: #1565c0;'>{len(filtered_df)}</h2>", unsafe_allow_html=True)

        if filtered_df.empty:
            st.warning("No potentials found matching the current criteria.")
        
        for index, row in filtered_df.iterrows():
            p_type = row.get('type', 'Unknown')
            type_class = "tag-reax"
            if "EAM" in p_type: type_class = "tag-eam"
            if "Tersoff" in p_type or "SW" in p_type: type_class = "tag-semi"
            if "AIREBO" in p_type: type_class = "tag-airebo"

            year_display = format_year(row.get('year'))

            try:
                clean_path = row['local_path'].replace("\\", "/")
                with open(clean_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
            except:
                file_content = "Error: File not found locally."

            # --- CARD RENDER ---
            with st.container(border=True):
                cols = st.columns([3, 1])
                
                with cols[0]:
                    # Header: System + Badge
                    st.markdown(f"### {row['system']} <span class='tag {type_class}'>{p_type}</span>", unsafe_allow_html=True)
                    
                    # Metadata Line
                    meta_html = f"<span style='color: #666;'>Filename:</span> <code>{row['filename']}</code>"
                    if year_display:
                        meta_html += f" &nbsp;|&nbsp; <span style='color: #666;'>Year:</span> <b>{year_display}</b>"
                    st.markdown(meta_html, unsafe_allow_html=True)
                    
                    st.markdown(f"<div style='margin-top:5px; font-size:0.9em; color:#444;'>Repository: {row['source_repo']}</div>", unsafe_allow_html=True)
                    
                    if row.get('description'):
                        st.caption(f"{row['description']}")

                    # --- CITATION SECTION ---
                    citation = row.get('citation')
                    if citation and citation != "Unknown" and len(citation) > 5:
                        st.markdown("<div style='margin-top: 15px; font-weight: bold; font-size: 0.9em;'>Bibliographic Reference:</div>", unsafe_allow_html=True)
                        st.code(citation, language=None)
                
                with cols[1]:
                    st.write("") 
                    st.download_button(
                        label="Download File",
                        data=file_content,
                        file_name=row['filename'],
                        mime='text/plain',
                        key=f"dl_{row['id']}",
                        use_container_width=True,
                        type="primary"
                    )
                    
                    # LAMMPS Snippet Expander
                    style_cmd = "reax/c" if "Reax" in p_type else p_type.lower()
                    snippet = f"pair_style {style_cmd} ...\npair_coeff * * {row['filename']} {' '.join(row['elements'])}"
                    
                    with st.expander("Usage Snippet"):
                        st.code(snippet, language="bash")

    # --- FOOTER ---
    st.write("")
    st.divider()
    
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.9em; padding-bottom: 20px;">
            <p><strong>Developed at the Laboratory of Computing in Materials Science (LCCMat)</strong></p>
            <p><em>University of Brasília (UnB) - Institute of Physics</em></p>
            <p style="margin-top: 20px;">© 2025 LCCMat. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()