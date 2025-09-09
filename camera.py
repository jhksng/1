import picamera
from google.cloud import storage
import paho.mqtt.publish as publish
import datetime

# 사진 촬영
camera = picamera.PiCamera()
file_name = f'images/photo_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg'
camera.capture(file_name)

# GCS에 사진 업로드
client = storage.Client()
bucket = client.bucket("YOUR_BUCKET_NAME") # 버킷 이름
blob = bucket.blob(file_name)
blob.upload_from_filename(file_name)

# MQTT 메시지 발행
gcs_url = f"gs://YOUR_BUCKET_NAME/{file_name}"
print(f"File uploaded to GCS: {gcs_url}")

# 스프링 서버에 URL을 MQTT 메시지로 보냅니다.
# 라즈베리파이가 있는 네트워크에 따라 브로커 주소를 다르게 설정해야 할 수 있습니다.
# 같은 네트워크일 경우 브로커 IP 주소, 다른 네트워크일 경우 공인 IP 주소를 사용하세요.
publish.single("photo/uploaded", gcs_url, hostname="YOUR_BROKER_IP")
