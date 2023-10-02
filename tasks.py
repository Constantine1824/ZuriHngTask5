import pika
from moviepy.editor import VideoFileClip
from django.conf import settings
import whisper
import selectors


selector = selectors.DefaultSelector()

print('working')
# connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL)
# )

# channel = connection.channel()
# channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME)

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

# def callback(ch, method, properties, body):
#     video_file = body.decode('utf-8')
#     transcribe(video_file)


# channel.basic_consume(queue=settings.RABBITMQ_QUEUE_NAME, on_message_callback=callback)


# channel.start_consuming()

def process_message(ch, method, properties, body):
    video_path = body.decode('utf-8')
    print(f"Transcribing video: {video_path}")

    transcription_result = transcribe(video_path)

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=transcription_result,
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

def handle_events():
    while True:
        for key, events in selector.select():
            callback = key.data
            callback()

def main():
    connection = pika.SelectConnection(pika.URLParameters(settings.RABBITMQ_URL)
    , on_open_callback=on_connected)

    selector.register(connection, selectors.EVENT_READ, connection.process_data_events)

    handle_events()

def on_connected(connection):
    connection.channel(on_channel_open)

def on_channel_open(channel):
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, callback=on_queue_declared)

def on_queue_declared(channel):
    channel.basic_consume(queue=settings.RABBITMQ_QUEUE_NAME, on_message_callback=process_message)

