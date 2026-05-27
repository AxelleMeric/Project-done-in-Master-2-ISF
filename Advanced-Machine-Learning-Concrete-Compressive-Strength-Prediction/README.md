# Advanced Machine Learning: Concrete Compressive Strength Prediction

Projet de régression supervisée visant à prédire la résistance à la compression du béton à partir de ses composants, avec nettoyage des données, ingénierie de variables, sélection de variables, modèles avancés, ensemble stacking et interprétabilité.

## Objectif

L'objectif du projet est de comparer plusieurs approches de modélisation sur le jeu de données Concrete Compressive Strength, puis d'interpréter les prédictions obtenues avec des méthodes globales et locales.

## Prérequis

- macOS/Linux (ou shell compatible)
- Python 3.13+
- `uv` installé

Installation de `uv` (si nécessaire):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Structure du dépôt

- `Projet.ipynb`: notebook principal contenant toute l'analyse
- `data/Concrete_Data.csv`: données source
- `figures/`: figures exportées par le notebook en mode rapport
- `pyproject.toml`: métadonnées et dépendances Python
- `Projet_AML_M2_ISF.pdf`: énoncé du projet

## Installation de l'environnement

Depuis la racine du projet:

```bash
uv sync
```

Cette commande crée automatiquement `.venv/` et installe les dépendances du projet.

Activation de l'environnement:

```bash
source .venv/bin/activate
```

## Exécution du notebook

### Option 1: VS Code

1. Ouvrir `Projet.ipynb`.
2. Sélectionner le kernel Python `.venv/bin/python`.
3. Exécuter les cellules dans l'ordre.

### Option 2: Jupyter

```bash
uv run jupyter lab
```

Puis ouvrir `Projet.ipynb` et exécuter toutes les cellules séquentiellement.

## Plan du notebook

Le notebook suit le pipeline suivant:

1. **Introduction et présentation du dataset**
   Chargement du fichier CSV, description des variables et premières vérifications.
2. **Découpage train/test**
   Séparation des données pour isoler un jeu de test final.
3. **Exploration des données (EDA)**
   Analyse de la variable cible, distributions des variables explicatives, relations avec la cible et comparaison des échelles.
4. **Pré-traitement**
   Détection des valeurs atypiques avec Isolation Forest, puis standardisation des variables.
5. **Sélection et ingénierie de variables**
   Construction de ratios métier, puis comparaison de plusieurs méthodes de sélection pour retenir un sous-ensemble final de variables.
6. **Baseline et interprétabilité globale**
   Entraînement d'un modèle de référence Random Forest, calcul des métriques de régression, puis visualisations PDP et ALE.
7. **Modélisation avancée**
   Optimisation et évaluation de XGBoost, SVR, ACE et d'une approximation noyau via Nyström.
8. **Ensemble learning**
   Construction d'un `StackingRegressor` combinant plusieurs modèles de base avec une méta-régression Ridge.
9. **Interprétabilité SHAP**
   Analyse globale de l'importance des variables et explications locales sur des prédictions individuelles.
10. **Robustesse**
   Évaluation de la sensibilité du modèle final à du bruit injecté dans les variables d'entrée.

## Algorithmes utilisés

### Pré-traitement

- **Isolation Forest**: détection non supervisée d'observations atypiques dans l'ensemble d'entraînement.
- **StandardScaler**: centrage-réduction des variables pour rendre comparables les échelles et stabiliser les modèles sensibles à la normalisation.

### Ingénierie de variables

Des variables dérivées sont ajoutées pour injecter de l'information métier:

- `Water_Cement_Ratio`
- `Water_Binder_Ratio`
- `Aggregate_Ratio`

Le notebook retient ensuite un sous-ensemble final de 7 variables:

- `Cement`
- `Blast_Furnace_Slag`
- `Superplasticizer`
- `Water_Binder_Ratio`
- `Coarse_Aggregate`
- `Age`
- `Aggregate_Ratio`

### Sélection de variables

Plusieurs familles de méthodes sont comparées:

- **Corrélation linéaire (Pearson)**: pré-sélection rapide et lecture des dépendances linéaires.
- **CMIM**: méthode filtre basée sur l'information mutuelle conditionnelle.
- **Lasso / LassoCV**: méthode embarquée pénalisant les coefficients peu utiles.
- **Random Forest feature importance**: importance des variables via réduction d'impureté.
- **Boruta**: méthode wrapper adossée à une forêt aléatoire pour confirmer les variables vraiment informatives.
- **RFECV**: élimination récursive de variables avec validation croisée.
- **Stability Selection**: répétition de sélections Lasso sur sous-échantillons pour mesurer la stabilité des variables retenues.

### Modèles de régression

- **Random Forest Regressor**: modèle baseline, robuste et utilisé aussi pour certaines étapes de sélection.
- **XGBoost Regressor**: boosting d'arbres avec recherche d'hyperparamètres par grille.
- **Support Vector Regression (SVR)**: régression à noyau RBF, elle aussi optimisée par grille.
- **ACE (Alternating Conditional Expectations)**: recherche de transformations maximisant la corrélation entre variables explicatives et cible.
- **Nyström + Ridge**: approximation de noyau RBF à grande échelle suivie d'une régression linéaire régularisée.
- **StackingRegressor**: combinaison de `Random Forest`, `XGBoost` et `SVR`, avec `RidgeCV` comme méta-modèle.

### Interprétabilité

- **PDP (Partial Dependence Plots)**: effet marginal moyen d'une variable sur la prédiction.
- **ALE (Accumulated Local Effects)**: alternative plus robuste aux corrélations entre variables.
- **SHAP**: explications globales et locales des contributions des variables aux prédictions du modèle XGBoost.

## Métriques suivies

Les évaluations reposent sur des métriques classiques de régression:

- `MAE`
- `MSE`
- `RMSE`
- `R²`

## Export des figures

Le notebook inclut une configuration centralisée:

- `REPORT_EXPORT_MODE = False`: affichage interactif
- `REPORT_EXPORT_MODE = True`: export silencieux vers `figures/`
- `REPORT_FIG_DIR = Path("figures")`

Quand `REPORT_EXPORT_MODE = True`, les figures finales sont sauvegardées sans affichage interactif.

## Reproductibilité

- Exécuter le notebook dans l'ordre, car plusieurs cellules partagent un état global.
- Conserver le format de lecture du CSV: `sep=';'` et `decimal=','`.
- Utiliser les versions de dépendances définies dans [`pyproject.toml`](/Users/arthurdanjou/Workspace/Advanced-Machine-Learning-Concrete-Compressive-Strength-Prediction/pyproject.toml).
