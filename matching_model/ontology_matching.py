import networkx as nx
import pandas as pd


def build_ontology_graph():

    df_skills = pd.read_csv("datasets/skills_en.csv")
    df_broader = pd.read_csv(
        "datasets/broaderRelationsSkillPillar_en.csv"
    )
    df_peer = pd.read_csv(
        "datasets/skillSkillRelations_en.csv"
    )
    df_tech = pd.read_csv(
        "datasets/digitalSkillsCollection_en.csv"
    )

    valid_tech_uris = set(
        df_tech["conceptUri"].dropna().unique()
    )

    G = nx.Graph()
    text_to_uri = {}

    for _, row in df_skills.iterrows():

        uri = row["conceptUri"]

        if uri not in valid_tech_uris:
            continue

        label = str(
            row["preferredLabel"]
        ).lower().strip()

        G.add_node(uri, label=label)

        text_to_uri[label] = uri

        if pd.notna(row["altLabels"]):

            alt_labels = (
                str(row["altLabels"])
                .replace("\n", ",")
                .split(",")
            )

            for alt in alt_labels:

                alt = alt.lower().strip()

                if alt:
                    text_to_uri[alt] = uri

    for _, row in df_broader.iterrows():

        child = row["conceptUri"]
        parent = row["broaderUri"]

        if (
            child in valid_tech_uris
            and parent in valid_tech_uris
        ):
            G.add_edge(child, parent)

    for _, row in df_peer.iterrows():

        a = row["originalSkillUri"]
        b = row["relatedSkillUri"]

        if (
            a in valid_tech_uris
            and b in valid_tech_uris
        ):
            G.add_edge(a, b)

    return G, text_to_uri


G, TEXT_TO_URI = build_ontology_graph()

def ontology_similarity(
    resume_skill,
    job_skill,
    graph,
    lookup,
    max_hops=3
):

    uri_r = lookup.get(
        resume_skill.lower().strip()
    )

    uri_j = lookup.get(
        job_skill.lower().strip()
    )

    if not uri_r or not uri_j:
        return 0.0

    if uri_r == uri_j:
        return 1.0

    try:

        distance = nx.shortest_path_length(
            graph,
            source=uri_r,
            target=uri_j
        )

        if distance > max_hops:
            return 0.0

        return round(
            1/(1+distance),
            3
        )

    except nx.NetworkXNoPath:

        return 0.0
    


def ontology_match(
    resume_skills,
    missing_job_skills
):

    ontology_matched = []
    ontology_missing = []

    threshold = 0.3

    for job_skill in missing_job_skills:

        best_score = 0
        best_resume_skill = None

        for resume_skill in resume_skills:

            score = ontology_similarity(
                resume_skill,
                job_skill,
                G,
                TEXT_TO_URI
            )

            if score > best_score:

                best_score = score
                best_resume_skill = resume_skill

        if best_score >= threshold:

            ontology_matched.append({
                "job_skill": job_skill,
                "resume_skill": best_resume_skill,
                "score": best_score
            })

        else:

            ontology_missing.append(
                job_skill
            )

    return ontology_matched, ontology_missing