from moviepy import *
from moviepy.video.io.VideoFileClip import VideoFileClip
import whisper
import string
from transformers import pipeline
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def preprocess_video(video_path):
    video_clip = VideoFileClip(video_path)

    # Extract audio
    audio_clip = video_clip.audio

    # Save the audio to a file
    audio_output_path = "output_audio.mp3"  # Specify output file path and format
    audio_clip.write_audiofile(audio_output_path)

    #Audio to text
    model = whisper.load_model("base")
    result = model.transcribe(audio_output_path)
    paragraph = result["text"]

    return paragraph


def get_articles(keywords, max_results=20, sort_by="relevance"):
    API_KEY = os.getenv('NEWSAPI_KEY')
    if not API_KEY:
        raise ValueError("NEWSAPI_KEY not found in environment variables. Please check your .env file.")
    BASE_URL = 'https://newsapi.org/v2/everything'

    articles = []
    page = 1
    query = ' OR '.join(keywords)  # Flexible matching: any keyword can appear

    while len(articles) < max_results:
        url = f"{BASE_URL}?q={query}&pageSize={min(100, max_results - len(articles))}&page={page}&sortBy={sort_by}&apiKey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            articles.extend(data.get("articles", []))
            if len(data.get("articles", [])) < 100:  # No more articles on next pages
                break
            page += 1
        else:
            print(f"Error fetching articles: {response.status_code} - {response.text}")
            break

    return articles[:max_results] if articles else None


def compare_similarities(text_embedding, articles_embeddings):
    # List to store cosine similarities
    similarities = []
    for article_embedding in articles_embeddings:
        similarity = util.cos_sim(text_embedding, article_embedding).item()
        similarities.append(similarity)

    # Sort articles by similarity (highest to lowest)
    sorted_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)

    return sorted_indices[:5]


def fake_news_detection(video_path):

    # get the transcribed text
    paragraph = preprocess_video(video_path)
    print(paragraph)

    # getting keywords
    model = KeyBERT()
    keywords = model.extract_keywords(paragraph, stop_words="english", top_n=5)
    keywords_updated = [keyword[0] for keyword in keywords]
    print("Keywords:", keywords_updated)

    try:
        # get Articles NewsAPI with keywords
        articles = get_articles(keywords_updated, max_results=50)
        if articles:
            for article in articles:
                print("Title:", article["title"])
                print("Source:", article["source"]["name"])
                print("URL:", article["url"])
                print("=" * 80)
        else:
            print("No articles found.")
            return None

        # summary of text
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(paragraph, max_length=70, min_length=50, do_sample=False)
        summarized_text = summary[0]['summary_text']

        # Semantic Embedding
        model = SentenceTransformer('all-MiniLM-L6-v2')  # Load the Sentence-BERT model
        text_embedding = model.encode(summarized_text, convert_to_tensor=True)  # Generate embedding for the input text

        # Generate embeddings for each article
        article_embeddings = []
        for article in articles:
            content_to_embed = f"{article['title']} {article['description']} {article.get('content', '')}"  # Combine title, description, and content
            embedding = model.encode(content_to_embed, convert_to_tensor=True)  # Generate embedding
            article_embeddings.append(embedding)

            # get the most similar articles
        best_five_articles = compare_similarities(text_embedding, article_embeddings)

        print("the most similar articles describing the content of your video are : ")

        summarized_articles = []
        for idx in best_five_articles:  # Display top 5 most similar articles
            summary = summarizer(articles[idx]['content'], max_length=100, min_length=100, do_sample=False)
            summarized_article = summary[0]['summary_text']

            summarized_articles.append({
                "title": articles[idx]['title'],
                "summary": summarized_article,
                "url": articles[idx]['url'],
                "source": articles[idx]['source']
            })

            print(f"Title: {articles[idx]['title']}")
            # print(f"Similarity Score: {similarities[idx]*100:.2f}%")
            print(f"Summarized Text: {summarized_article}")
            print(f"URL: {articles[idx]['url']}")
            print(f"SOURCE: {articles[idx]['source']}")
            print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        return None  # Return an appropriate fallback value

    return summarized_articles