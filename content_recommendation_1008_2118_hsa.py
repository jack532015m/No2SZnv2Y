# 代码生成时间: 2025-10-08 21:18:46
import celery
from celery import shared_task
import math
from collections import defaultdict
from typing import List, Dict, Tuple

# 假设有一个用户-项目评分数据集，这里我们使用一个简单的字典来模拟
user_item_ratings = {
    'user1': {'item1': 5, 'item2': 3},
    'user2': {'item1': 4, 'item3': 1},
    'user3': {'item2': 2, 'item3': 5},
    'user4': {'item4': 4, 'item3': 1},
}

# 推荐算法类
class ContentRecommendation:
    def __init__(self):
        self.user_item_ratings = user_item_ratings

    def calculate_similarity(self, user1: str, user2: str) -> float:
        """
        计算两个用户之间的余弦相似度
        """
        ratings1 = self.user_item_ratings.get(user1, {})
        ratings2 = self.user_item_ratings.get(user2, {})
        common_items = set(ratings1) & set(ratings2)
        if not common_items:
            return 0.0

        sum1 = sum(ratings1.values())
        sum2 = sum(ratings2.values())
        sum1_sq = sum([val ** 2 for val in ratings1.values()])
        sum2_sq = sum([val ** 2 for val in ratings2.values()])
        p_sum = sum([ratings1[item] * ratings2[item] for item in common_items])

        numerator = p_sum
        denominator = math.sqrt(sum1_sq) * math.sqrt(sum2_sq)
        if denominator == 0:
            return 0.0
        else:
            return float(numerator) / denominator

    def get_recommendations(self, user: str, num_recommendations: int = 5) -> List[str]:
        """
        为用户生成推荐列表
        """
        scores = defaultdict(list)
        user_ratings = self.user_item_ratings[user]
        total_similarities = defaultdict(float)
        for other in self.user_item_ratings:
            if other == user:
                continue
            sim = self.calculate_similarity(user, other)
            total_similarities[other] = sim
            for item in self.user_item_ratings[other]:
                if item not in user_ratings:
                    scores[item].append(sim)

        # 按评分排序并返回推荐列表
        ranked_items = sorted(scores, key=lambda k: sum(scores[k]), reverse=True)
        return ranked_items[:num_recommendations]

# Celery配置
app = celery.Celery('tasks',
                   broker='amqp://guest@localhost//')

# 定义一个异步任务，用于生成推荐
@app.task
def generate_recommendations(user: str, num_recommendations: int = 5) -> List[str]:
    recommendation_engine = ContentRecommendation()
    try:
        recommendations = recommendation_engine.get_recommendations(user, num_recommendations)
        return {
            'user': user,
            'recommendations': recommendations,
        }
    except Exception as e:
        return {'error': str(e)}
