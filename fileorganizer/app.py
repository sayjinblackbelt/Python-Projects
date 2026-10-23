from pathlib import Path

import streamlit as st

from organizer import plan_organization, organize_files

st.set_page_config(page_title="FileOrganizer", page_icon="🗂️", layout="wide")
st.title("🗂️ FileOrganizer")
st.write("Organize arquivos por tipo. Analise primeiro; nada será movido sem sua confirmação.")

folder_text = st.text_input(
    "Caminho completo da pasta",
    placeholder="/Users/seu_usuario/Downloads",
    help="No macOS, você pode copiar o caminho da pasta no Finder e colá-lo aqui.",
)

if st.button("Analisar pasta", type="primary"):
    if not folder_text.strip():
        st.session_state["folder_plan"] = None
        st.error("Informe o caminho de uma pasta para continuar.")
    else:
        try:
            selected_folder = Path(folder_text.strip()).expanduser()
            st.session_state["folder_text"] = str(selected_folder)
            st.session_state["folder_plan"] = [
                (str(source), str(destination))
                for source, destination in plan_organization(selected_folder)
            ]
            st.session_state["plan_folder"] = str(selected_folder)
        except (FileNotFoundError, NotADirectoryError, PermissionError) as exc:
            st.session_state["folder_plan"] = None
            st.error(str(exc))

plan = st.session_state.get("folder_plan")
if plan is not None:
    st.subheader("Prévia da organização")
    st.caption("Pasta analisada: {}".format(st.session_state.get("plan_folder", "")))
    if not plan:
        st.info("Não há arquivos diretamente nesta pasta para organizar.")
    else:
        rows = [
            {"Arquivo atual": Path(source).name,
             "Destino previsto": str(Path(destination).parent.name) + "/" + Path(destination).name}
            for source, destination in plan
        ]
        st.dataframe(rows, use_container_width=True, hide_index=True)
        st.write("Arquivos encontrados: **{}**".format(len(plan)))
        confirm = st.checkbox(
            "Revisei a prévia e confirmo que quero mover estes arquivos."
        )
        if st.button("Organizar arquivos", disabled=not confirm):
            try:
                results = organize_files(Path(st.session_state["plan_folder"]))
                st.success("Organização concluída: {} arquivo(s) movido(s).".format(len(results)))
                st.session_state["folder_plan"] = None
                st.rerun()
            except (OSError, FileNotFoundError, NotADirectoryError) as exc:
                st.error("Não foi possível concluir a organização: {}".format(exc))

st.divider()
st.caption("Dica: teste primeiro com uma pasta de exemplo. A ferramenta não percorre subpastas.")
