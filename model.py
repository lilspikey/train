import serialhandler


class Attr:
    def __init__(self, name, default=None):
        self._name = name
        self._default = default

    def __get__(self, instance, owner):
        return instance._attribs.get(self._name, self._default)

    def __set__(self, instance, value):
        old_value = instance._attribs.get(self._name, self._default)
        if old_value != value:
            instance._old[self._name] = old_value
            instance._attribs[self._name] = value
            instance._notify_listeners(self._name)


class Model:
    def __init__(self):
        self._attribs = {}
        self._old = {}
        self._listeners = []

    def add_listener(self, listener):
        self._listeners.append(listener)
        return listener

    def get_old_value(self, name):
        return self._old[name]

    def _notify_listeners(self, changed_attr):
        for listener in self._listeners:
            listener(self, changed_attr)


class TrainSet(Model):
    power = Attr('power', 0)
    forward = Attr('forward', True)
    turnout = Attr('turnout', 'left')
    decoupler = Attr('decoupler', 'down')
    sensor1 = Attr('sensor1', False)
    sensor2 = Attr('sensor2', False)
    sensor3 = Attr('sensor3', False)
    sensor4 = Attr('sensor4', False)
    sensor5 = Attr('sensor5', False)
    sensor6 = Attr('sensor6', False)
    light1 = Attr('light1', False)
    light2 = Attr('light2', False)

    def __init__(self, port, ioloop):
        super(TrainSet, self).__init__()
        def serial_callback(key, value):
            ioloop.add_callback(self._status_received, key, value)
        self.serial_protocol = serialhandler.SerialProtocol(port, serial_callback)
    
    def _status_received(self, key, value):
        setattr(self, key, value)

    def status_attrs(self):
        return ['power', 'forward', 'turnout', 'decoupler',
                'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5', 'sensor6',
                'light1', 'light2']

    def throttle_forward(self, power):
        self.serial_protocol.throttle_forward(power)

    def throttle_reverse(self, power):
        self.serial_protocol.throttle_reverse(power)

    def turnout_left(self):
        self.serial_protocol.turnout_left()

    def turnout_right(self):
        self.serial_protocol.turnout_right()

    def decoupler_up(self):
        self.serial_protocol.decoupler_up()

    def decoupler_down(self):
        self.serial_protocol.decoupler_down()

    def light1_on(self):
        self.serial_protocol.light1_on()

    def light1_off(self):
        self.serial_protocol.light1_off()

    def light2_on(self):
        self.serial_protocol.light2_on()

    def light2_off(self):
        self.serial_protocol.light2_off()


class AutoPilot(Model):
    IDLE = 'idle'
    DECOUPLING = 'decoupling'
    state = Attr('state', IDLE)

    def __init__(self, trainset, serial_protocol):
        super(AutoPilot, self).__init__()
        self._trainset = trainset
        self._serial_protocol = serial_protocol
        trainset.add_listener(self._trainset)
    
    def can_auto_decouple(self):
        if self.state != self.IDLE:
            return False
        # TODO need right sensors here
        return self._trainset.sensor1 and self._trainset.sensor2

    def auto_decouple(self):
        if self.can_auto_decouple():
            self.state = self.DECOUPLING
            self._serial_protocol.throttle_forward(900)

    def _trainset_changed(self, model, name):
        if self.state == self.DECOUPLING:
            # TODO need right sensors here
            if self._trainset.sensor3:
                self._serial_protocol.decoupler_up()



