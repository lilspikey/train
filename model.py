import serialhandler


class Attr:
    def __init__(self, default=None, alias=None):
        self.name = None
        self._default = default
        self.alias = alias

    def __get__(self, instance, owner):
        return instance._attribs.get(self.name, self._default)

    def __set__(self, instance, value):
        old_value = instance._attribs.get(self.name, self._default)
        if old_value != value:
            instance._old[self.name] = old_value
            instance._attribs[self.name] = value
            instance._notify_listeners(self.name)


class ModelMeta(type):
    def __init__(cls, name, bases, namespace):
        super(ModelMeta, cls).__init__(name, bases, namespace)
        cls.status_attrs = []
        for name, value in namespace.items():
            if isinstance(value, Attr):
                value.name = name
                cls.status_attrs.append(name)
                if value.alias:
                    setattr(cls, value.alias, value)


class Model(metaclass=ModelMeta):
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
    AUTO_STATE_IDLE = 'idle'
    AUTO_STATE_DECOUPLING = 'decoupling'
    auto_state = Attr(AUTO_STATE_IDLE)

    power = Attr(0)
    forward = Attr(True)
    turnout = Attr('left')
    decoupler = Attr('down')
    sensor1 = Attr(False, alias='sensor_buffer')
    sensor2 = Attr(False, alias='sensor_predecoupler')
    sensor3 = Attr(False, alias='sensor_postdecoupler')
    sensor4 = Attr(False)
    sensor5 = Attr(False)
    sensor6 = Attr(False)
    light1 = Attr(False)
    light2 = Attr(False)

    def __init__(self, port, ioloop):
        super(TrainSet, self).__init__()
        def serial_callback(key, value):
            ioloop.add_callback(self._status_received, key, value)
        self.serial_protocol = serialhandler.SerialProtocol(port, serial_callback)
        self.ioloop = ioloop
        @self.add_listener
        def _update_autopilot(model, name):
            if name.startswith('sensor'):
                self.update_autopilot()
    
    def _status_received(self, key, value):
        setattr(self, key, value)

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

    def update_autopilot(self):
        if self.auto_state == self.AUTO_STATE_DECOUPLING:
            self.throttle_forward(900)
            if self.sensor_postdecoupler:
                if self.decoupler == 'down':
                    self.decoupler_up()
                    self.auto_state = self.AUTO_STATE_IDLE

    def can_auto_decouple(self):
        if self.auto_state != self.AUTO_STATE_IDLE:
            return False
        return self.sensor_buffer and self.sensor_predecoupler
    
    def auto_decouple(self):
        if self.can_auto_decouple():
            self.auto_state = self.AUTO_STATE_DECOUPLING
            self.update_autopilot()
            def _reset_autopilot():
                self.auto_state = self.AUTO_STATE_IDLE
                self.decoupler_down()
                self.throttle_forward(0)
            self.ioloop.add_timeout(self.ioloop.time()+3, _reset_autopilot)

