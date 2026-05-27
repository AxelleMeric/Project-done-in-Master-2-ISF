# 📚 Le Conseiller Enneigé — Mon Bibliothécaire IA (RAG & LangGraph)

**Projet NLP / IA Générative** *Auteur : Axelle MERIC*

## 📝 Description

Le Conseiller Enneigé est un assistant conversationnel intelligent conçu pour vous aider à choisir votre prochaine lecture parmi votre Pile À Lire (PAL). Le système utilise des techniques avancées de NLP (RAG, Embeddings multilingues, Agents LangGraph) pour extraire vos critères de lecture, interroger une base de données vectorielle de vos propres livres, et vous formuler des recommandations personnalisées de manière naturelle et chaleureuse.

## ✨ Fonctionnalités

- 🕷️ **Enrichissement des données (Scraping)** : Récupération automatique des résumés de livres via Livraddict, Google Books et Goodreads.
- 🔍 **Recherche sémantique (RAG)** : Recherche hybride combinant similarité vectorielle (FAISS) et filtres stricts de métadonnées.
- 🤖 **Agent LangGraph (MistralAI)** : Orchestration intelligente avec extraction stricte de critères au format JSON (Pydantic).
- ✋ **Validation "Human-in-the-loop"** : L'agent demande la validation des critères extraits avant d'exécuter la recherche.
- 💬 **Interface Streamlit interactive** : Design personnalisé avec historique de chat, avatars sur-mesure et mémorisation du contexte.

## 🏗️ Architecture

    ┌─────────────────────────────────────────────────────────────┐
    │          Mon Bibliothécaire IA — Le Conseiller Enneigé      │
    │                                                             │
    │  🎨 Frontend : Streamlit (Interface de Chat)                │
    │  🧠 Cœur d'IA : LangGraph & MistralAI                       │
    │     ├── 1. Nœud de Planification (Extraction JSON)          │
    │     ├── 2. Nœud de Validation (Human-in-the-loop)           │
    │     ├── 3. Nœud d'Exécution (Recherche FAISS)               │
    │     └── 4. Nœud de Synthèse (Rédaction de la recommandation)│
    │  📊 Base Vectorielle : FAISS + HuggingFace Embeddings       │
    │  📚 Base de Données : CSV enrichi par Web Scraping          │
    └─────────────────────────────────────────────────────────────┘

## ⚙️ Prérequis

- Python ≥ 3.9
- Une clé API MistralAI (`MISTRAL_API_KEY`)

## 🚀 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/AxelleMeric/Le-Conseiller-Enneig-/tree/main
cd Mon_Bibliothecaire_IA
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```
*(Assurez-vous d'avoir les packages: `streamlit`, `langchain`, `langchain-mistralai`, `langchain-huggingface`, `faiss-cpu`, `langgraph`, `pandas`, `beautifulsoup4`, `requests`)*

3. **Configurer la clé API MistralAI**
Dans le fichier `app.py`, remplacez `"METTRE_UNE_CLE_API"` par votre véritable clé (ou configurez une variable d'environnement) :
```bash
export MISTRAL_API_KEY="votre_cle_api"
```

## 📖 Utilisation

Le projet est divisé en trois grandes étapes :

### 1. Enrichissement des données (Web Scraping)
Ouvrez et exécutez le notebook `Code Résumé.ipynb`. Il prendra votre fichier `PAL_extract_without_resume.csv` d'origine, ira chercher les résumés manquants sur internet, et générera le fichier `PALextract.csv`.

### 2. Création de la Base Vectorielle FAISS
Ouvrez et exécutez le notebook `Biblio.ipynb`. Ce notebook va nettoyer le CSV final, générer les embeddings multilingues (`paraphrase-multilingual-MiniLM-L12-v2`) et sauvegarder la base de données dans le dossier local `faiss_index_bibliotheque`.

### 3. Lancement de l'Application Web
Lancez l'interface Streamlit depuis votre terminal :
```bash
python -m streamlit run app.py
```
L'application sera accessible sur `http://localhost:8501`.

## 📂 Contenu du Projet

|      Fichier / Dossier      |                                      Rôle                                    |
|:----------------------------|:-----------------------------------------------------------------------------|
| `Code Résumé.ipynb`         | Scripts de Web Scraping (BeautifulSoup) pour récupérer les résumés.          |
| `Biblio.ipynb`              | Préparation des données, création de la base FAISS et prototypage LangGraph. |
| `app.py`                    | Code de production de l'application web Streamlit.                           |
| `faiss_index_bibliotheque/` | Dossier généré contenant l'index vectoriel FAISS.                            |
| `.streamlit/config.toml`    | Fichier de configuration du thème visuel de l'application.                   |

## 🛠️ Technologies Principales

- **LangChain / LangGraph** : Orchestration du LLM et logique des graphes d'état.
- **MistralAI** : Modèle LLM (`mistral-small-latest`) pour l'extraction de critères et la rédaction.
- **FAISS** : Base de données vectorielle locale.
- **HuggingFace** : Modèle d'Embeddings (`paraphrase-multilingual-MiniLM-L12-v2`).
- **Streamlit** : Interface utilisateur web interactive.
- **BeautifulSoup4** : Extraction d'informations sur des sites web (Scraping).

## 💬 Exemples de questions supportées

- *"Je cherche une Romance en anglais de moins de 350 pages."*
- *"Je cherche mes livres sur Artemis Fowl."*
- *"Je cherche un roman écrit par Cathrine Arnaud."*
- *"Je veux un gros livre de fantasy (plus de 400 pages) avec une note d'au moins 15/20."*