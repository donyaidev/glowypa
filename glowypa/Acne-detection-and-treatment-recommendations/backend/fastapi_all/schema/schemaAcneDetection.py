from datetime import datetime

def acneDetectionFormat(acne_detection) -> dict:
    return {
        "id": str(acne_detection['_id']),
        "user_id": acne_detection['user_id'],
        "images": [
            {"image_id": image["image_id"], "image_base64": image["image_base64"]} for image in acne_detection['images']
        ],
        "predicted_images": [
            {
                "image_id": predicted_image["image_id"],
                "predicted": predicted_image["predicted"],
                "architecture_ai_name": predicted_image["architecture_ai_name"],
                "total_acnes": predicted_image["total_acnes"]
            } for predicted_image in acne_detection['predicted_images']
        ],
        "date": acne_detection['date'].isoformat() if isinstance(acne_detection['date'], datetime) else acne_detection['date']
    }


def acneDetectionListFormat(acne_detections) -> list:
    return [acneDetectionFormat(acne_detection) for acne_detection in acne_detections]

