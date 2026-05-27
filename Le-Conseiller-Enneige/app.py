
from datetime import datetime as dt
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import PydanticOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field
from typing import TypedDict, List, Optional
import base64 
import os
import streamlit as st

# =======================================
# 1. CONFIGURATION DE LA PAGE STREAMLIT
# =======================================
st.set_page_config(page_title="Le conseiller enneigé", page_icon="pioupiou.jpg", layout="centered")

@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

nom_image_gauche = "photo_gauche.jpg" 
nom_image_droite = "photo_droite.jpg"

img_left_base64 = get_base64_image(nom_image_gauche)
img_right_base64 = get_base64_image(nom_image_droite)

if img_left_base64 and img_right_base64:
    st.markdown(f"""
        <style>
            .fixed-img-left {{
                position: fixed;
                top: 50%; 
                transform: translateY(-50%);
                left: 2%;
                width: 18vw; 
                /* On remplace l'aspect-ratio par une hauteur calculée mathématiquement (18 * 16/9 = 32) */
                height: 32vw; 
                /* La magie est ici : on "peint" l'image en fond */
                background-image: url("data:image/jpeg;base64,{img_left_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 15px;
                z-index: 0; 
                pointer-events: none; 
                box-shadow: 4px 4px 15px rgba(0,0,0,0.3);
            }}
            .fixed-img-right {{
                position: fixed;
                top: 50%; 
                transform: translateY(-50%);
                right: 2%;
                width: 18vw; 
                height: 32vw; 
                background-image: url("data:image/jpeg;base64,{img_right_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 15px;
                z-index: 0; 
                pointer-events: none; 
                box-shadow: -4px 4px 15px rgba(0,0,0,0.3);
            }}
            @media (max-width: 1050px) {{
                .fixed-img-left, .fixed-img-right {{ display: none; }}
            }}

            [data-testid="stChatInput"] textarea::placeholder {{
                /* Le texte indicatif transparent, basé sur ton violet foncé (#983399) */
                color: rgba(152, 51, 153, 0.6) !important;
            }}
            
            [data-testid="stChatInput"] textarea {{
                /* Le texte que tu tapes en violet foncé */
                color: #983399 !important;
                font-weight: bold;
            }}
        </style>
        <div class="fixed-img-left"></div>
        <div class="fixed-img-right"></div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 4]) 

with col1:
    st.image("pioupiou.jpg", width=100) 

with col2:
    st.title("Le conseiller enneigé") 
st.write("Bienvenue ! Voici le conseiller enneigé qui connait toute la pile à lire du Livre enneigé et peut te conseiller.")

# =======================================
# 2. CONFIGURATION DE L'IA ET DE LA BASE
# =======================================

os.environ["MISTRAL_API_KEY"] = "METTRE_UNE_CLE_API"

# On utilise un cache pour ne pas recharger la base FAISS à chaque message
@st.cache_resource
def charger_ressources():
    print("Chargement du modèle Multilingue et de la base FAISS")
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    vectorstore = FAISS.load_local("faiss_index_bibliotheque", embeddings, allow_dangerous_deserialization=True)
    model = ChatMistralAI(model="mistral-small-latest", temperature=0)
    return vectorstore, model

vectorstore, model = charger_ressources()

# =================================
# 3. SCHÉMAS ET OUTIL DE RECHERCHE
# =================================
class PlanRechercheLivre(BaseModel):
    query: str = Field(..., description="Le thème principal ou 'livre' par défaut.")
    auteur: Optional[str] = Field(None, description="Nom de l'auteur.")
    genre: Optional[str] = Field(None, description="Genre littéraire.")
    editeur: Optional[str] = Field(None, description="Maison d'édition.")
    langue: Optional[str] = Field(None, description="Code langue ('fr', 'en').")
    lectorat: Optional[str] = Field(None, description="Public visé.")
    nb_pages_min: Optional[int] = Field(None, description="Nombre minimum de pages.")
    nb_pages_max: Optional[int] = Field(None, description="Nombre maximum de pages.")
    note_min: Optional[float] = Field(None, description="Note minimale sur 20.")
    annee_min: Optional[int] = Field(None, description="Année de publication minimale.")
    annee_max: Optional[int] = Field(None, description="Année de publication maximale.")
    date_achat_apres: Optional[str] = Field(None, description="Acheté après cette date (YYYY-MM-DD).")
    date_achat_avant: Optional[str] = Field(None, description="Acheté avant cette date (YYYY-MM-DD).")

class AgentState(TypedDict):
    question: str
    plan_recherche: Optional[dict]
    validation_errors: Optional[List[str]]
    resultats_livres: Optional[str]
    reponse_finale: str

@tool
def chercher_livres_filtres(query: str, auteur: Optional[str] = None, langue: Optional[str] = None, nb_pages_min: Optional[int] = None, nb_pages_max: Optional[int] = None, note_min: Optional[float] = None, annee_min: Optional[int] = None, annee_max: Optional[int] = None, date_achat_apres: Optional[str] = None, date_achat_avant: Optional[str] = None, genre: Optional[str] = None, editeur: Optional[str] = None, lectorat: Optional[str] = None) -> str:
    """Outil de recherche avancé pour interroger la bibliothèque de livres.""" 
    
    def filtre_faiss(metadata: dict) -> bool:
        if auteur and auteur.lower() not in str(metadata.get("auteur", "")).lower(): return False
        if editeur and editeur.lower() not in str(metadata.get("editeur", "")).lower(): return False
        if lectorat and lectorat.lower() != str(metadata.get("lectorat", "")).lower(): return False
        if genre and genre.lower() not in str(metadata.get("genre", "")).lower(): return False
        if langue:
            meta_lang = str(metadata.get("langue", "")).lower()
            if langue.lower() == "en" and "anglais" not in meta_lang: return False
            if langue.lower() == "fr" and "français" not in meta_lang and "francais" not in meta_lang: return False
        if nb_pages_min and metadata.get("nb_pages", 0) < nb_pages_min: return False
        if nb_pages_max and metadata.get("nb_pages", 0) > nb_pages_max: return False
        if note_min and metadata.get("note_moyenne", 0) < note_min: return False
        if annee_min and metadata.get("annee", 0) < annee_min: return False
        if annee_max and metadata.get("annee", 0) > annee_max: return False
        return True

    try:
        results_with_scores = vectorstore.similarity_search_with_score(query, k=5, filter=filtre_faiss, fetch_k=1000)
    except Exception as e:
        return f"Erreur technique FAISS : {str(e)}"

    textes_formates = []
    for doc, distance in results_with_scores:
        if query.lower().strip() != "livre" and distance > 15.0:
            continue
        t = doc.metadata.get("titre", "Inconnu")
        a = doc.metadata.get("auteur", "Inconnu")
        textes_formates.append(f"Titre: {t}\nAuteur: {a}\nRésumé: {doc.page_content}")
        
    if not textes_formates:
        return "Aucun livre pertinent n'a été trouvé pour ce sujet exact dans la bibliothèque."
    return "\n\n---\n\n".join(textes_formates)

# ==============================
# 4. NOEUDS DU GRAPHE LANGGRAPH
# ==============================
def planning_node(state: AgentState):
    question = state["question"]
    parser = PydanticOutputParser(pydantic_object=PlanRechercheLivre)

    prompt = f"""Ta SEULE tâche est de générer un objet JSON valide. Ne rédige AUCUN texte, AUCUN code. JUSTE LE JSON.
Question de l'utilisateur : "{question}"

RÈGLES STRICTES :
1. 'query' : Si l'utilisateur donne un vrai sujet d'histoire (ex: magie, meurtre, vampires), mets-le ici. S'il ne demande qu'un genre (ex: romance, fantasy) ou un format, tu DOIS écrire "livre" ici.
2. 'genre' : Les genres littéraires (Romance, Fantasy, Polar...) vont UNIQUEMENT ici. Ne les mets jamais dans 'query'.
3. Pages : Traduis "court", "moins de 300 pages" dans 'nb_pages_max' et "gros", "plus de 500 pages" dans 'nb_pages_min'.
4. N'invente rien. Laisse la valeur à null si l'information n'est pas dans la question.

{parser.get_format_instructions()}"""
    
    try:
        reponse = model.invoke(prompt)
        plan = parser.parse(reponse.content)
        return {"plan_recherche": plan.model_dump(), "validation_errors": None}
    except Exception as e:
        return {"plan_recherche": {"query": "livre"}, "validation_errors": ["Erreur de format du LLM."]}

def validation_node(state: AgentState):
    plan = state.get("plan_recherche")
    errors = state.get("validation_errors") or []
    if plan:
        p_min, p_max = plan.get("nb_pages_min"), plan.get("nb_pages_max")
        if p_min and p_max and p_min > p_max: errors.append(f"Erreur : Pages Min > Pages Max.")
    return {"validation_errors": errors if errors else None}

def execution_node(state: AgentState):
    plan = state["plan_recherche"]
    try:
        resultats = chercher_livres_filtres.invoke(plan)
    except Exception as e:
        resultats = f"Erreur de recherche : {e}"
    return {"resultats_livres": resultats}

def synthesis_node(state: AgentState):
    question = state["question"]
    contexte_livres = state.get("resultats_livres", "Aucun résultat.")
    prompt = f"""Tu es un bibliothécaire personnel très chaleureux.
DEMANDE : "{question}"
LIVRES TROUVÉS :
{contexte_livres}
CONSIGNE : Si aucun livre, dis-le gentiment sans rien inventer. Sinon, présente-les avec enthousiasme. Ne parle pas de la technique. Rédige ta réponse finale en t'adressant directement à l'utilisateur :"""
    try:
        reponse = model.invoke(prompt)
        return {"reponse_finale": reponse.content}
    except:
        return {"reponse_finale": "Désolé, problème lors de la rédaction."}

# =========================
# 5. COMPILATION DU GRAPHE 
# =========================
@st.cache_resource
def creer_graphe():
    graph = StateGraph(AgentState)
    graph.add_node("planifier", planning_node)
    graph.add_node("valider", validation_node)
    graph.add_node("chercher", execution_node)
    graph.add_node("repondre", synthesis_node)
    
    graph.set_entry_point("planifier")
    graph.add_edge("planifier", "valider")
    
    def validation_router(state: AgentState):
        if state.get("validation_errors"): return END 
        return "chercher" 
        
    graph.add_conditional_edges("valider", validation_router)
    graph.add_edge("chercher", "repondre")
    graph.add_edge("repondre", END)
    
    return graph.compile()

app_biblio = creer_graphe()

# =======================================
# 6. INTERFACE DE CHAT (Avec Validation)
# =======================================
st.write("---")

AVATARS = {
    "user": "photo_moi.jpg",        
    "assistant": "photo_agent.jpg"      
}

# INITIALISATION DE LA MÉMOIRE 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis ton bibliothécaire personnel. Quel genre de livre aimerais-tu lire ?"}
    ]
if "attente_validation" not in st.session_state:
    st.session_state.attente_validation = False
if "plan_temporaire" not in st.session_state:
    st.session_state.plan_temporaire = None
if "question_originale" not in st.session_state:
    st.session_state.question_originale = ""

# AFFICHAGE DES ANCIENS MESSAGES 
for message in st.session_state.messages:
    # On ajoute l'avatar correspondant au rôle
    with st.chat_message(message["role"], avatar=AVATARS[message["role"]]):
        st.markdown(message["content"])

# BOÎTE DE SAISIE
if prompt := st.chat_input("Tape ta recherche ou réponds par oui/non..."):
    
    # Message de l'utilisateur avec son avatar
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # ==========================================
    # CAS A : ON ATTENDAIT UNE RÉPONSE (OUI/NON)
    # ==========================================
    if st.session_state.attente_validation:
        # Message de l'IA avec son avatar
        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            if prompt.lower().strip() in ["oui", "o", "yes", "ouais", "ok", "parfait", "yep"]:
                with st.spinner("Génial, je cherche dans tes étagères... 🧐"):
                    try:
                        plan = st.session_state.plan_temporaire
                        question_init = st.session_state.question_originale
                        
                        state = {"question": question_init, "plan_recherche": plan}
                        
                        resultats_recherche = execution_node(state)
                        state.update(resultats_recherche)
                        
                        resultats_redaction = synthesis_node(state)
                        state.update(resultats_redaction)
                        
                        reponse_ia = state["reponse_finale"]
                        st.markdown(reponse_ia)
                        st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
                        
                    except Exception as e:
                        erreur_msg = f"Erreur technique lors de la recherche : {e}"
                        st.error(erreur_msg)
                        st.session_state.messages.append({"role": "assistant", "content": erreur_msg})
            else:
                reponse_ia = "D'accord, on annule cette recherche ! Reformule ta demande avec d'autres mots."
                st.markdown(reponse_ia)
                st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
        
        st.session_state.attente_validation = False
        st.session_state.plan_temporaire = None
        st.session_state.question_originale = ""

    # ======================================
    # CAS B : C'EST UNE NOUVELLE RECHERCHE
    # ======================================
    else:
        # Message de l'IA avec son avatar
        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            with st.spinner("Je décortique ta demande... 🤔"):
                try:
                    state = {"question": prompt}
                    state = planning_node(state)
                    plan = state["plan_recherche"]
                    
                    reponse_ia = "**Voici les critères que j'ai extraits :**\n"
                    reponse_ia += f"- 📝 **Sujet** : {plan.get('query', 'livre')}\n"
                    
                    if plan.get('auteur'): reponse_ia += f"- ✍️ **Auteur** : {plan['auteur']}\n"
                    if plan.get('genre'): reponse_ia += f"- 🎭 **Genre** : {plan['genre']}\n"
                    if plan.get('langue'): reponse_ia += f"- 🌍 **Langue** : {plan['langue']}\n"
                    if plan.get('nb_pages_min'): reponse_ia += f"- 📄 **Pages Min** : {plan['nb_pages_min']}\n"
                    if plan.get('nb_pages_max'): reponse_ia += f"- 📄 **Pages Max** : {plan['nb_pages_max']}\n"
                    if plan.get('note_min'): reponse_ia += f"- ⭐ **Note Min** : {plan['note_min']}/20\n"
                    if plan.get('annee_min'): reponse_ia += f"- 📅 **Année Min** : {plan['annee_min']}\n"
                    if plan.get('annee_max'): reponse_ia += f"- 📅 **Année Max** : {plan['annee_max']}\n"
                    if plan.get('editeur'): reponse_ia += f"- 🏢 **Éditeur** : {plan['editeur']}\n"
                    if plan.get('lectorat'): reponse_ia += f"- 👥 **Lectorat** : {plan['lectorat']}\n"
                    if plan.get('date_achat_apres'): reponse_ia += f"- 🛒 **Acheté après le** : {plan['date_achat_apres']}\n"
                    if plan.get('date_achat_avant'): reponse_ia += f"- 🛒 **Acheté avant le** : {plan['date_achat_avant']}\n\n"
                    
                    reponse_ia += "\n\n👉 **Est-ce que ces critères te conviennent ? (Réponds par Oui ou Non)**"
                    
                    st.markdown(reponse_ia)
                    st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
                    
                    st.session_state.attente_validation = True
                    st.session_state.plan_temporaire = plan
                    st.session_state.question_originale = prompt 
                    
                except Exception as e:
                    erreur = f"Oups, j'ai eu un problème : {e}"
                    st.error(erreur)
                    st.session_state.messages.append({"role": "assistant", "content": erreur})