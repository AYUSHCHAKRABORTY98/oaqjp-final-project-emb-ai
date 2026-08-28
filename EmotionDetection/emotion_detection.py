import requests
import json


def emotion_detector(text_to_analyze):
    WATSON_EMOTION_URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    WATSON_EMOTION_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
        }

    payload =        {
            "raw_document": {
                "text": text_to_analyze
            }
        }
    response = requests.post(
            WATSON_EMOTION_URL,
            headers=WATSON_EMOTION_HEADERS,
            json=payload,
        )
    emotions = dict(response.json())
    t=emotions['emotionPredictions'][0]['emotion']
    t['dominant_emotion']=max(t,key=t.get)
    print(t)
    return t


if __name__ == "__main__":
    emotion_detector("I hate working long hours")