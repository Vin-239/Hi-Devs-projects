import math

# Decorator to handle zero division / empty data edge cases cleanly
def safe_compute(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            return 0.0
    return wrapper

class SimilarityCalculator:
    
    @safe_compute
    def cosine_similarity(self, vec1, vec2):
        common = set(vec1.keys()) & set(vec2.keys())
        if not common: return 0.0
        
        dot_product = sum(vec1[i] * vec2[i] for i in common)
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
        
        return dot_product / (mag1 * mag2)

    @safe_compute
    def jaccard_similarity(self, set1, set2):
        if not set1 and not set2: return 0.0
        
        intersect = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersect / union

    @safe_compute
    def pearson_correlation(self, ratings1, ratings2):
        common = set(ratings1.keys()) & set(ratings2.keys())
        n = len(common)
        if n == 0: return 0.0
        
        sum1 = sum(ratings1[i] for i in common)
        sum2 = sum(ratings2[i] for i in common)
        
        sum1_sq = sum(ratings1[i]**2 for i in common)
        sum2_sq = sum(ratings2[i]**2 for i in common)
        
        p_sum = sum(ratings1[i] * ratings2[i] for i in common)
        
        num = p_sum - (sum1 * sum2 / n)
        den = math.sqrt((sum1_sq - sum1**2 / n) * (sum2_sq - sum2**2 / n))
        
        return num / den