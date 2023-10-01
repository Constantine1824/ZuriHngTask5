import pika
from moviepy.editor import VideoFileClip
from django.conf import settings
import whisper

print('working')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    credentials=pika.PlainCredentials(
        username=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    ),
))

channel = connection.channel()
channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME)

def transcribe(video_file):
    def get_audio(video_file):
        video_clip = VideoFileClip(video_file)
        audio_clip = video_clip.audio
        path = '/media/audio/' + video_file.split('.') + '.wav'
        audio_clip.write_audiofile(path)
        return path
    audio = get_audio(video_file)
    model = whisper.load_model('base')
    transcript = model.transcribe(audio)
    with open(f'/media/transcript/{video_file}.txt','w') as file:
        file.write(transcript)

def callback(ch, method, properties, body):
    video_file = body.decode('utf-8')
    transcribe(video_file)


channel.basic_consume(queue=settings.RABBITMQ_QUEUE_NAME, on_message_callback=callback)


channel.start_consuming()