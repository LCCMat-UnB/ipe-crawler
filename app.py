import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(
    page_title="ReaxFF Library - LCCMat",
    page_icon="assets/logo_lccmat.png", 
    layout="wide"
)

@st.cache_data
def load_database():
    file_path = "data/master_index.json"
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return []

def get_snippet(filename, elements):
    elems_str = " ".join(elements)
    return f"""# LAMMPS Input Snippet
pair_style reax/c lmp_control
pair_coeff * * {filename} {elems_str}
fix qeq all qeq/reax 1 0.0 10.0 1e-6 param.qeq"""

def main():

    c_left, c_logo, c_right = st.columns([4, 1, 4])
    
    with c_logo:
        if os.path.exists("assets/logo_lccmat_h.png"):
            st.image("assets/logo_lccmat_h.png", use_container_width=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        # ATUALIZAÇÃO AQUI: Texto sobre o grupo e link para produções
        st.markdown(
            """
            <h1 style='text-align: center;'>ReaxFF Potential Library</h1>
            <h5 style='text-align: center; color: gray;'>Interactive database for Reactive Force Fields</h5>
            
            <div style='text-align: center; margin-top: 15px; font-size: 0.9em; color: #444;'>
                <p style='margin-bottom: 5px;'>
                    Discover the research and publications produced by the LCCMat group:
                </p>
                <a href='https://lccmat.unb.br/' target='_blank' style='text-decoration: none; color: #0068c9; font-weight: bold; font-size: 1.1em;'>
                    Visit Official Website (lccmat.unb.br)
                </a>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.write("") 
        st.write("") 

        st.markdown("### Search")
        
        raw_data = load_database()
        if not raw_data:
            st.error("Database empty.")
            st.stop()
        df = pd.DataFrame(raw_data)

        all_elements = set()
        for el_list in df['elements']:
            all_elements.update(el_list)
        sorted_elements = sorted(list(all_elements))

        selected_elements = st.multiselect(
            label="Search inputs", 
            options=sorted_elements,
            #default=["C", "H", "O"],
            placeholder="Select elements...",
            label_visibility="collapsed"
        )
        
        strict_mode = st.checkbox("Strict Match (Exact elements only)", value=False)

    if selected_elements:
        req_set = set(selected_elements)
        def filter_func(row_elements):
            row_set = set(row_elements)
            if strict_mode:
                return row_set == req_set
            else:
                return req_set.issubset(row_set)
        filtered_df = df[df['elements'].apply(filter_func)]
    else:
        filtered_df = df

    st.divider()
    
    col_info, col_count = st.columns([8, 1])
    col_info.subheader(f"Results")
    col_count.metric("Found", len(filtered_df))

    if not filtered_df.empty:
        selection = st.dataframe(
            filtered_df[['system', 'original_filename', 'source_repo']],
            use_container_width=True,
            column_config={
                "system": "System",
                "original_filename": "File Name",
                "source_repo": "Repository"
            },
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun"
        )

        if selection.selection.rows:
            selected_index = selection.selection.rows[0]
            selected_id = filtered_df.iloc[selected_index]['id']
            record = df[df['id'] == selected_id].iloc[0]

            with st.container(border=True):
                st.markdown(f"### 📄 {record['original_filename']}")
                c1, c2 = st.columns(2)
                
                with c1:
                    st.info(f"**Composition:** {record['system']}")
                    st.text(f"Source: {record['source_repo']}")
                    if record.get('download_url'):
                        st.link_button("View on GitHub", record['download_url'])

                with c2:
                    snippet = get_snippet(record['original_filename'], record['elements'])
                    st.code(snippet, language="bash")

                clean_path = record['local_path'].replace("\\", "/")
                if os.path.exists(clean_path):
                    with open(clean_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    with st.expander("Show File Content"):
                        st.text(content[:3000])
                    st.download_button(
                        f"Download {record['original_filename']}", 
                        content, 
                        file_name=record['original_filename'],
                        type="primary"
                    )
    else:
        c_l, c_msg, c_r = st.columns([1, 2, 1])
        with c_msg:
            st.warning("No potentials found matching these criteria.")

    st.write("")
    st.write("")
    st.write("")
    st.divider()
    
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.9em;">
            <p><strong>Developed at the Laboratory of Computing in Materials Science (LCCMat)</strong></p>
            <p><em>University of Brasília (UnB) - Institute of Physics</em></p>
            <p style="font-size: 0.8em; max-width: 800px; margin: 0 auto;">
                Established in 2020, LCCMat serves as the primary High-Performance Computing (HPC) infrastructure 
                supporting advanced research in Nanomaterials and Biomaterials. 
                This tool is provided as a multi-user platform resource for the scientific community.
            </p>
            <p style="margin-top: 20px;">© 2025 LCCMat. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()