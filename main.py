#%%
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
df_suicides_france = pd.read_csv(
    Path(__file__).parent / "data" / "suicides-deces-france.csv",
)
df_suicides_france.columns = df_suicides_france.columns.str.lstrip("\ufeff").str.strip()


deces_par_sexe_et_age_2023 = (
	df_suicides_france.loc[
		(df_suicides_france["Année"] == 2023)
		& df_suicides_france["Sexe"].isin(["Hommes", "Femmes"])
		& (df_suicides_france["Classe d'âge"] != "Tous")
	]
	.pivot(index="Sexe", columns="Classe d'âge", values="Nombre de décès")
	.reindex(["Hommes", "Femmes"])
)
classes_age_par_representation = (
	deces_par_sexe_et_age_2023.sum().sort_values(ascending=False).index
)
tableau_effectifs_2023 = (
	deces_par_sexe_et_age_2023.T
	.reindex(classes_age_par_representation)[["Hommes", "Femmes"]]
)
tableau_effectifs_2023["Total"] = tableau_effectifs_2023.sum(axis=1)
tableau_effectifs_2023.loc["Total"] = tableau_effectifs_2023.sum()
print("Effectifs de suicides en France en 2023 par tranche d'âge et sexe :")
print(tableau_effectifs_2023.to_string(
	float_format=lambda valeur: f"{valeur:,.1f}".replace(",", " ").replace(".", ","),
))
couleurs_par_tranche_age = dict(zip(classes_age_par_representation, plt.get_cmap("tab10").colors[:len(classes_age_par_representation)]))
fig_suicides_sexes, ax_suicides_sexes = plt.subplots(
	figsize=(8, 5), layout="constrained",
)
base_barres_sexes = pd.Series(0.0, index=deces_par_sexe_et_age_2023.index)
for classe_age in classes_age_par_representation:
	valeurs_classe_age = deces_par_sexe_et_age_2023[classe_age]
	ax_suicides_sexes.bar(
		deces_par_sexe_et_age_2023.index,
		valeurs_classe_age,
		bottom=base_barres_sexes,
		label=classe_age,
		color=couleurs_par_tranche_age[classe_age],
	)
	base_barres_sexes += valeurs_classe_age

ax_suicides_sexes.bar_label(
	ax_suicides_sexes.containers[-1],
	fmt="%.1f", padding=3, label_type="edge",
)
ax_suicides_sexes.set_ylabel("Nombre de décès")
ax_suicides_sexes.set_title("Suicides en France en 2023 selon le sexe et l'âge")
ax_suicides_sexes.set_ylim(0, base_barres_sexes.max() * 1.12)
ax_suicides_sexes.legend(
	title="Tranche d'âge", loc="upper left", bbox_to_anchor=(1.02, 1),
)
ax_suicides_sexes.grid(axis="y", alpha=0.25)
ax_suicides_sexes.set_axisbelow(True)

df_hospitalisations_france = pd.read_csv(
	Path(__file__).parent / "data" / "gestes-auto-infliges-hospitalisations-france.csv",
)
df_hospitalisations_france.columns = (
	df_hospitalisations_france.columns.str.lstrip("\ufeff").str.strip()
)
sejours_par_sexe_et_age_2023 = (
	df_hospitalisations_france.loc[
		(df_hospitalisations_france["Année"] == 2023)
		& df_hospitalisations_france["Sexe"].isin(["Hommes", "Femmes"])
		& (df_hospitalisations_france["Classe d'âge"] != "Tous")
	]
	.pivot(
		index="Sexe",
		columns="Classe d'âge",
		values="Nombre de séjours pour geste auto-infligé",
	)
	.reindex(["Hommes", "Femmes"])
)
classes_age_hospit_par_representation = (
	sejours_par_sexe_et_age_2023.sum().sort_values(ascending=False).index
)
tableau_hospitalisations_2023 = (
	sejours_par_sexe_et_age_2023.T
	.reindex(classes_age_hospit_par_representation)[["Hommes", "Femmes"]]
)
tableau_hospitalisations_2023["Total"] = tableau_hospitalisations_2023.sum(axis=1)
tableau_hospitalisations_2023.loc["Total"] = tableau_hospitalisations_2023.sum()
print("Séjours hospitaliers en France en 2023 par tranche d'âge et sexe :")
print(tableau_hospitalisations_2023.to_string(
	float_format=lambda valeur: f"{valeur:,.1f}".replace(",", " ").replace(".", ","),
))

fig_hospitalisations_sexes, ax_hospitalisations_sexes = plt.subplots(
	figsize=(8, 5), layout="constrained",
)
base_barres_hospitalisations = pd.Series(
	0.0, index=sejours_par_sexe_et_age_2023.index,
)
for classe_age in classes_age_hospit_par_representation:
	valeurs_classe_age = sejours_par_sexe_et_age_2023[classe_age]
	ax_hospitalisations_sexes.bar(
		sejours_par_sexe_et_age_2023.index,
		valeurs_classe_age,
		bottom=base_barres_hospitalisations,
		label=classe_age,
		color=couleurs_par_tranche_age[classe_age],
	)
	base_barres_hospitalisations += valeurs_classe_age

ax_hospitalisations_sexes.bar_label(
	ax_hospitalisations_sexes.containers[-1],
	fmt="%.1f", padding=3, label_type="edge",
)
ax_hospitalisations_sexes.set_ylabel("Nombre de séjours hospitaliers")
ax_hospitalisations_sexes.set_title(
	"Hospitalisations en France en 2023 selon le sexe et l'âge",
)
ax_hospitalisations_sexes.set_ylim(0, base_barres_hospitalisations.max() * 1.12)
ax_hospitalisations_sexes.legend(
	title="Tranche d'âge", loc="upper left", bbox_to_anchor=(1.02, 1),
)
ax_hospitalisations_sexes.grid(axis="y", alpha=0.25)
ax_hospitalisations_sexes.set_axisbelow(True)

plt.show()
# %%
