import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings  # Import settings
from .models import Interaction, Product
from django.core.cache import cache

def get_user_recommendations(user_id):
    # fetched the cached recommendations
    cached_recommendations = cache.get(f"user_recommendations_{user_id}")
    if cached_recommendations:
        return cached_recommendations  # Return cached data if available
    
    # If not cached, compute the recommendations
    interactions = Interaction.objects.all()
    interaction_data = list(interactions.values('user_id', 'item_id', 'score'))
    data = pd.DataFrame(interaction_data)
    pivot_table = data.pivot_table(index='user_id', columns='item_id', values='score').fillna(0)
    user_vector = pivot_table.loc[user_id].values.reshape(1, -1)
    similarity = cosine_similarity(user_vector, pivot_table)
    
    similar_users = similarity.argsort().flatten()[-6:-1]  # Excluding the first index (itself)
    recommended_item_ids = pivot_table.iloc[similar_users].mean().sort_values(ascending=False).index[:10]
    
    recommended_items = Product.objects.filter(item_id__in=recommended_item_ids).values('item_id', 'name', 'item_image')
    recommendations = [
        {
            'item_id': item['item_id'],
            'name': item['name'],
            'image_url': f"{settings.MEDIA_URL}{item['item_image']}" if item['item_image'] else None
        }
        for item in recommended_items
    ]
    
    # set the Cache for 1 hour
    cache.set(f"user_recommendations_{user_id}", recommendations, timeout=3600)  # Timeout is in seconds
    
    return recommendations
