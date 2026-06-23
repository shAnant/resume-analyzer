from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')


def semantic_match(
    resume_skills,
    ontology_missing,
    threshold=0.75
):

    semantic_matched = []
    semantic_missing = []

    resume_embeddings = {
        skill: model.encode(skill)
        for skill in resume_skills
    }

    for job_skill in ontology_missing:

        job_embedding = model.encode(job_skill)

        best_score = -1
        best_skill = None

        for resume_skill, resume_embedding in resume_embeddings.items():

            score = cosine_similarity(
                [job_embedding],
                [resume_embedding]
            )[0][0]

            if score > best_score:
                best_score = score
                best_skill = resume_skill

        if best_score >= threshold:

            semantic_matched.append({
                "job_skill": job_skill,
                "resume_skill": best_skill,
                "score": round(float(best_score), 4)
            })

        else:

            semantic_missing.append(job_skill)

    return semantic_matched, semantic_missing