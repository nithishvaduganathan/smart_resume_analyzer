from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_resume_with_job(resume_text, job_description):
    texts = [resume_text, job_description]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return {
        'match_score': round(similarity * 100, 2),
        'feedback': 'Good match!' if similarity > 0.7 else 'Consider adding more relevant skills.'
    }
