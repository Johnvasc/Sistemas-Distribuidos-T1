# ---------------------------- lógica RabbitMQ
from objects.queue_logic.publisher_queue_objects import PublisherQueueObjects
import threading
class SprinklerRabbit(PublisherQueueObjects):

    def send_frequency_updates(self, channel):
        send_att_thread = threading.Thread(target = self.send_attribute_updates, args = (channel, self.queue, "ambient_humidity"), daemon = True)
        send_att_thread.start()