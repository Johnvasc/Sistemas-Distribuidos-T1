
from objects.queue_logic.publisher_queue_objects import PublisherQueueObjects
import threading


class AcRabbit(PublisherQueueObjects):

    def send_temperature_updates(self, channel):
        #Thread para envio constante da temperatura atual
        send_att_thread = threading.Thread(target = self.send_attribute_updates, args = (channel, self.queue, "ambient_temperature"), daemon = True)
        send_att_thread.start()