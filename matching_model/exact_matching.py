def exact_match(resume_skills, job_skills):

    exact_matched = []
    exact_missing = []

    resume_set = set(resume_skills)

    for job_skill in job_skills:

        if job_skill in resume_set:

            exact_matched.append({
                "skill": job_skill
            })

        else:
            exact_missing.append(job_skill)

    return exact_matched, exact_missing