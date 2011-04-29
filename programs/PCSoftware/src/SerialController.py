import messages
import network as net
import serial
import json
import select

class SerialController(net.MessageListener):

  def __init__(self, port, serialPort):
    net.MessageListener.__init__(self, port)
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
    self.send_msg(msg)

  def send_msg(self,msg):
    messages.send(msg,50000) 

  def serial_write(self,msg):
    self.writeable = True
    self.handle_mesg(msg)
    print 'Serial is ready'

  def serial_error(self):
    print 'Serial error!'

  def sock_read(self):
    msg = self.multisock.recv(1024)
    print 'Recv: %s' % repr(msg)
    self.handle_msg(msg)



  def ready_handlers(self):
    readers = {
      self.serial: self.serial_read,
      self.multisocket: self.sock_read,
    }
    writers = {
      self.serial: self.serial_write,
    }
    errors = {
      self.serial: self.serial_error,
    }
    return readers, writers, errors

  def run(self):
    self.serial.open()

    while True:
      try:
        socks = [self.multisocket, self.serial]

        ready = select.select(socks, [], [])
        handlers = self.ready_handlers()

        for h, r in zip(handlers, ready):
          if h in r:

            try:
              h[r]()
            except KeyError, e:
              pass
            except Exception, e:
              print 'Exception handling: %s' % repr(e)
              net.printtraceback()
          else: 
            pass  

      except Exception, e:
        print 'Exception: %s' % repr(e)
        net.printtraceback()

if __name__ == '__main__':
  sc = SerialController(50002, '/dev/ttyUSB1')
  sc.run()
