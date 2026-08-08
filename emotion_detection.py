import requests
import json

# Watson Emotion API Configuration
WATSON_EMOTION_URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
WATSON_EMOTION_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}

def detect_emotion(text):
    """
    Detect emotion from the given text using IBM Watson NLP API.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        dict: A dictionary containing the detected emotion and confidence scores
              Returns None if API call fails
              
    Example:
        >>> result = detect_emotion("I am very happy today!")
        >>> print(result)
    """
    if not text or not isinstance(text, str):
        return {"error": "Invalid input. Please provide a non-empty string."}
    
    try:
        # Prepare the request payload
        payload = {
            "raw_document": {
                "text": text
            }
        }
        
        # Make the API request
        response = requests.post(
            WATSON_EMOTION_URL,
            headers=WATSON_EMOTION_HEADERS,
            json=payload,
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return format_emotion_response(result)
        else:
            return {
                "error": f"API request failed with status code {response.status_code}",
                "details": response.text
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}",
            "details": "Could not connect to Watson Emotion API"
        }
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse API response: {str(e)}",
            "details": "Invalid JSON response from API"
        }

def format_emotion_response(response):
    """
    Format the Watson API response into a readable format.
    
    Args:
        response (dict): Raw response from Watson API
        
    Returns:
        dict: Formatted emotion detection results
    """
    try:
        emotions = response.get("emotionPredictions", [{}])[0].get("emotion", {})
        
        # Sort emotions by score (highest first)
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "success": True,
            "emotions": dict(sorted_emotions),
            "dominant_emotion": sorted_emotions[0][0] if sorted_emotions else None,
            "confidence": sorted_emotions[0][1] if sorted_emotions else None,
            "raw_response": response
        }
    except (KeyError, IndexError, AttributeError) as e:
        return {
            "success": False,
            "error": f"Failed to parse emotion response: {str(e)}",
            "raw_response": response
        }

# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_texts = [
        "I am very happy today!",
        "This is so frustrating and annoying.",
        "I feel sad and disappointed.",
        "I am excited about this amazing opportunity!",
        "This is a neutral statement about the weather."
    ]
    
    print("=" * 60)
    print("Watson Emotion Detection - Test Results")
    print("=" * 60)
    
    for text in test_texts:
        print(f"\nAnalyzing: '{text}'")
        result = detect_emotion(text)
        
        if result.get("success"):
            print(f"  Dominant Emotion: {result['dominant_emotion']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  All Emotions:")
            for emotion, score in result['emotions'].items():
                print(f"    - {emotion}: {score:.2%}")
        else:
            print(f"  Error: {result.get('error')}")
        print("-" * 60)
