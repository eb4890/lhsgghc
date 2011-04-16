import messages
import network
import serial
import json


class SerialController(MessageListener):

  def __init__(self, port, serialPort):
    MessageListener.__init__(self, port)
    self.serial = serial.Serial(serialPort)
    valid_msgs = [
      'setlight',
      'startregistration',
    ]
    self.controller = dict.fromkeys(valid_msgs, self.handle_msg)

  def handle_msg(self, msg):
    self.serial.write(json.dumps(msg))

  def serial_read(self):
    msg = self.serial.readline()
    print 'Received on serial: %s' % repr(msg)
    self.handle_msg(msg)

  def serial_write(self):
    self.writeable = True
    print 'Serial is ready'

  def serial_error(self):
    print 'Serial error!'

  def sock_read(self):
    msg = readers[0][0].recv(1024)
    print 'Recv: %s' % repr(msg)
    self.handle_msg(msg)



  def ready_handlers(self):
    readers = {
      self.serial: serial_read,
      self.multisocket: sock_read,
    }
    writers = {
      self.serial: serial_write,
    }
    errors = {
      self.serial: serial_error,
    }
    return readers, writers, errors

  def run(self):
    self.serial.open()

    while True:
      try:
        socks = [self.multisocket, self.serialsocket]

        ready = select.select(socks, [], [])
        handlers = self.ready_handlers()

        for h, r in zip(handlers, ready):
          if r in h:

            try:
              h[r]()
            except KeyError, e:
              pass
            except Exception, e:
              print 'Exception handling: %s' % repr(e)

      except Exception, e:
        print 'Exception: %s' % repr(e)

if __name__ == '__main__':
  sc = SerialController(50002, '/dev/ttyUSB0')
  sc.run()
