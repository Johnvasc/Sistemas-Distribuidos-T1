
from objects.queue_logic.publisher_queue_objects import PublisherQueueObjects
import threading


class LampRabbit(PublisherQueueObjects):

    def send_luminosity_updates(self, channel):
        #Thread para envio constante da luminosidade atual
        send_att_thread = threading.Thread(target = self.send_attribute_updates, args = (channel, self.queue, "ambient_luminosity"), daemon = True)
        send_att_thread.start()