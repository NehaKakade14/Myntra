# from flask import Flask, request, jsonify
# from datetime import datetime
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics.pairwise import cosine_similarity
# import firebase_admin
# from firebase_admin import credentials, firestore

# import logging
# logging.basicConfig(level=logging.DEBUG)

# # Initialize Flask application
# app = Flask(__name__)

# # Initialize Firebase Admin SDK with service account credentials
# cred = credentials.Certificate(r'C:\Users\nehak\Desktop\FirebaseServiceKey\fashion-rental-ee377-firebase-adminsdk-22yee-bf124bb20a.json')
# firebase_admin.initialize_app(cred)

# # Access Firestore database
# firestore_db = firestore.client()

# # Load dataset and prepare the recommendation system
# df = pd.read_csv('DummyMyntraDataset2.csv')  # Replace with your dataset file path
# columns_to_combine = ['name', 'colour', 'brand', 'Body Shape ID', 'Body or Garment Size', 'Bottom Closure',
#                       'Bottom Fabric', 'Bottom Pattern', 'Bottom Type', 'Dupatta', 'Dupatta Border',
#                       'Dupatta Fabric', 'Dupatta Pattern', 'Main Trend', 'Neck', 'Number of Pockets',
#                       'Occasion', 'Pattern Coverage', 'Print or Pattern Type', 'Sleeve Length',
#                       'Sleeve Styling', 'Slit Detail', 'Stitch', 'Sustainable', 'Top Design Styling',
#                       'Top Fabric', 'Top Hemline', 'Top Length', 'Top Pattern', 'Top Shape', 'Top Type',
#                       'Waistband', 'Wash Care', 'Weave Pattern', 'Weave Type', 'Ornamentation']
# df[columns_to_combine] = df[columns_to_combine].fillna('')
# df['description'] = df[columns_to_combine].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# original_numeric_columns = ['No of Right Swipes', 'No of rents', 'ratingCount', 'avg_rating']
# df[original_numeric_columns] = df[original_numeric_columns].fillna(0)
# numeric_columns = ['No of Right Swipes', 'No of rents', 'ratingCount', 'avg_rating']
# scaler = MinMaxScaler()
# df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# tfidf = TfidfVectorizer(stop_words='english')
# tfidf_matrix = tfidf.fit_transform(df['description'])
# tfidf_df = pd.DataFrame(tfidf_matrix.toarray())
# combined_features = pd.concat([tfidf_df, df[numeric_columns].reset_index(drop=True)], axis=1)
# cosine_sim = cosine_similarity(combined_features)

# def get_recommendations(product_index):
#     sim_scores = list(enumerate(cosine_sim[product_index]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:11]
#     product_indices = [i[0] for i in sim_scores]
#     return df.iloc[product_indices]

# @app.route('/', methods=['GET'])
# def landing():
#     return "Welcome to the Fashion Rental App!"

# @app.route('/swipe', methods=['POST'])
# def swipe():
#     data = request.get_json()
#     user_id = data['user_id']
#     product_id = data['product_id']
#     swipe_direction = data['swipe_direction']

#     swipe_ref = firestore_db.collection('swipes').add({
#         'user_id': user_id,
#         'product_id': product_id,
#         'swipe_direction': swipe_direction,
#         'timestamp': datetime.utcnow()
#     })

#     return jsonify({"message": "Swipe data received"})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import firebase_admin
from firebase_admin import credentials, firestore

from flask_cors import CORS, cross_origin

firebaseConfig = {
    'apiKey': "AIzaSyDJ8E2YWRxF06QSxXa-q3Bx6faqfJXabRY",
    'authDomain': "recommendationtest-dc470.firebaseapp.com",
    'databaseURL': "https://recommendationtest-dc470-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "recommendationtest-dc470",
    'storageBucket': "recommendationtest-dc470.appspot.com",
    'messagingSenderId': "111255511810",
    'appId': "1:111255511810:web:a63a33159feec6a844181b",
    'measurementId': "G-ZTE2J19NQZ"
}
import logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate(r'C:\Users\nehak\Downloads\recommendationtest-dc470-firebase-adminsdk-nm4z9-84ab710293.json')
firebase_admin.initialize_app(cred)

# Access Firestore database
firestore_db = firestore.client()

# Load dataset and prepare the recommendation system
df = pd.read_csv('DummyMyntraDataset2.csv')  # Replace with your dataset file path
columns_to_combine = ['name', 'colour', 'brand', 'Body Shape ID', 'Body or Garment Size', 'Bottom Closure',
                      'Bottom Fabric', 'Bottom Pattern', 'Bottom Type', 'Dupatta', 'Dupatta Border',
                      'Dupatta Fabric', 'Dupatta Pattern', 'Main Trend', 'Neck', 'Number of Pockets',
                      'Occasion', 'Pattern Coverage', 'Print or Pattern Type', 'Sleeve Length',
                      'Sleeve Styling', 'Slit Detail', 'Stitch', 'Sustainable', 'Top Design Styling',
                      'Top Fabric', 'Top Hemline', 'Top Length', 'Top Pattern', 'Top Shape', 'Top Type',
                      'Waistband', 'Wash Care', 'Weave Pattern', 'Weave Type', 'Ornamentation']
df[columns_to_combine] = df[columns_to_combine].fillna('')
df['description'] = df[columns_to_combine].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

original_numeric_columns = ['No of Right Swipes', 'No of rents', 'ratingCount', 'avg_rating']
df[original_numeric_columns] = df[original_numeric_columns].fillna(0)
numeric_columns = ['No of Right Swipes', 'No of rents', 'ratingCount', 'avg_rating']
scaler = MinMaxScaler()
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['description'])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray())
combined_features = pd.concat([tfidf_df, df[numeric_columns].reset_index(drop=True)], axis=1)
cosine_sim = cosine_similarity(combined_features)

def get_recommendations(product_id):
    product_index = df[df['p_id'] == product_id].index
    if product_index.empty:
        raise IndexError("Product ID not found in the dataset")
    product_index = product_index[0]
    sim_scores = list(enumerate(cosine_sim[product_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get the top 10 recommendations
    product_indices = [i[0] for i in sim_scores]
    return df.iloc[product_indices]

@app.route('/', methods=['GET'])
def landing():
    return "Welcome to the Fashion Rental App!"

@app.route('/swipe', methods=['POST'])
def swipe():
    data = request.get_json()
    user_id = data['user_id']
    product_id = data['product_id']
    swipe_direction = data['swipe_direction']

    swipe_ref = firestore_db.collection('swipes').add({
        'user_id': user_id,
        'product_id': product_id,
        'swipe_direction': swipe_direction,
        'timestamp': datetime.utcnow()
    })

    return jsonify({"message": "Swipe data received"})

@app.route('/recommendations/<int:product_id>', methods=['GET'])
def recommendations(product_id):
    try:
        recommendations_df = get_recommendations(product_id)
        recommendations_list = recommendations_df.to_dict('records')

        # Save recommendations to Firebase
        firestore_db.collection('recommendations').document(str(product_id)).set({
            'product_id': product_id,
            'recommendations': recommendations_list,
            'timestamp': datetime.utcnow()
        })

        return jsonify(recommendations_list)
    except IndexError as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
