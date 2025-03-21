from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Simulated user data (dummy data)
dummy_users = {
    'user1': {'preferences': {'interests': ['sign-in', 'feedback']}},
    'user2': {'preferences': {'interests': ['chat', 'profile']}},
    'user3': {'preferences': {'interests': ['chat', 'feedback']}}
}

# Simulated content data (dummy data)
dummy_content = [
    {'id': 1, 'title': 'Chatbot Feature', 'tags': ['chatbot']},
    {'id': 2, 'title': 'Chat Data Management', 'tags': ['chatData']},
    {'id': 3, 'title': 'Chat Cache System', 'tags': ['chatcache']},
    {'id': 4, 'title': 'Custom Chat Data', 'tags': ['customchatdata']},
    {'id': 5, 'title': 'Change Password Log', 'tags': ['changepwdlog']},
    {'id': 6, 'title': 'Login Log Management', 'tags': ['loginlog']},
    {'id': 7, 'title': 'Edit Log Tracking', 'tags': ['editlog']},
    {'id': 8, 'title': 'Manage Role Permissions', 'tags': ['mangerole']},
    {'id': 9, 'title': 'Role vs From Master', 'tags': ['rolevsfrommaster']},
    {'id': 10, 'title': 'Role vs From Master Data', 'tags': ['rolevsfrommasterdata']},
    {'id': 11, 'title': 'From Master', 'tags': ['frommaster']},
    {'id': 12, 'title': 'From Master Data', 'tags': ['fromMasterData']},
    {'id': 13, 'title': 'Role Master Management', 'tags': ['RoleMaster']},
    {'id': 14, 'title': 'Role Master Data', 'tags': ['RoleMasterData']},
    {'id': 15, 'title': 'Sub Menu Master Data', 'tags': ['SubMenuMasterData']},
    {'id': 16, 'title': 'Sub Menu Master', 'tags': ['SubMenuMaster']},
    {'id': 17, 'title': 'Menu Master Data', 'tags': ['MenuMasterData']},
    {'id': 18, 'title': 'Menu Master', 'tags': ['MenuMaster']},
    {'id': 19, 'title': 'Role Management', 'tags': ['Role']},
    {'id': 20, 'title': 'Role vs Admin Master', 'tags': ['RoleVsAdminMaster']},
    {'id': 21, 'title': 'New Student Academics', 'tags': ['NewStudentAcademics']},
    {'id': 22, 'title': 'Student Feedback System', 'tags': ['StudentFeedback']},
    {'id': 23, 'title': 'Feedback Management', 'tags': ['Feedback']},
    {'id': 24, 'title': 'Student Hobby Preferences', 'tags': ['Hobby']},
    {'id': 25, 'title': 'Class Master Details', 'tags': ['ClassMaster']},
    {'id': 26, 'title': 'Student Hobby Tracking', 'tags': ['StudentHobby']},
    {'id': 27, 'title': 'Subject Preference', 'tags': ['SubjectPreference']},
    {'id': 28, 'title': 'Student Login Data', 'tags': ['StudentLogin']},
    {'id': 29, 'title': 'Academic History Record', 'tags': ['AcademicHistory']},
    {'id': 30, 'title': 'Student Profile', 'tags': ['Student']},
    {'id': 31, 'title': 'Student Address Management', 'tags': ['StudentAddress']},
    {'id': 32, 'title': 'Contact Information', 'tags': ['Contact']},
    {'id': 33, 'title': 'Language Knowledge Base', 'tags': ['LanguageKnow']}
]


dummy_user_actions = {
    'user1': [1, 2],  
    'user2': [3, 4], 
    'user3': [1, 4]   
}

# Simulated visit frequencies
visit_frequencies = {
    'user1': {'chatbot': 10, 'feedback': 2},
    'user2': {'chat': 7, 'profile': 3},
    'user3': {'chatbot': 5, 'feedback': 8}
}

# Step 1: Build a user-item interaction matrix
def build_interaction_matrix(users, content, interactions):
    user_ids = list(users.keys())
    content_ids = [item['id'] for item in content]
    interaction_matrix = pd.DataFrame(0, index=user_ids, columns=content_ids)
    for user, items in interactions.items():
        for item_id in items:
            interaction_matrix.loc[user, item_id] = 1
    return interaction_matrix

interaction_matrix = build_interaction_matrix(dummy_users, dummy_content, dummy_user_actions)

# Step 2: Calculate cosine similarity between users based on interactions
user_similarity = cosine_similarity(interaction_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=interaction_matrix.index, columns=interaction_matrix.index)

# Step 3: Generate recommendations based on user similarity and visit frequencies
def recommend_content(username, top_n=2):
    if username not in user_similarity_df.index:
        return "User not found."

    # Find the most similar users to the given username
    similar_users = user_similarity_df[username].sort_values(ascending=False).index[1:]

    # Collect items interacted with by similar users, excluding items the target user has already interacted with
    target_user_interactions = set(dummy_user_actions.get(username, []))
    recommendations = []

    for similar_user in similar_users:
        similar_user_interactions = set(dummy_user_actions.get(similar_user, []))
        recommended_items = similar_user_interactions - target_user_interactions
        recommendations.extend(recommended_items)
        
        # Stop if we've reached the desired number of recommendations
        if len(recommendations) >= top_n:
            break

    # Convert recommended item IDs to titles
    recommended_titles = [item['title'] for item in dummy_content if item['id'] in recommendations[:top_n]]

    # Step 4: Adjust recommendations based on frequent visits to sections
    frequent_visits = visit_frequencies.get(username, {})
    prioritized_recommendations = []
    for section, count in frequent_visits.items():
        if count >= 5:  # Priority threshold, adjust as needed
            for item in dummy_content:
                if section in item['tags'] and item['title'] not in recommended_titles:
                    prioritized_recommendations.append(item['title'])

    # Combine and return prioritized and similarity-based recommendations
    final_recommendations = prioritized_recommendations + recommended_titles
    return final_recommendations[:top_n]

# Testing the recommendation system
def display_recommendations(username):
    recommendations = recommend_content(username)
    if isinstance(recommendations, str):  # If "User not found."
        print(recommendations)
    else:
        print(f"Recommendations for {username}: {recommendations}")

# Display recommendations for users
display_recommendations('user1')
display_recommendations('user2')
display_recommendations('user3')
display_recommendations('unknown_user')  # Test for a non-existent user