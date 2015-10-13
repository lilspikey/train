

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

    def status_attrs(self):
        return ['power', 'forward', 'turnout', 'decoupler',
                'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5', 'sensor6',
                'light1', 'light2']


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
        return self._trainset.sensor1 and self._trainset.sensor2

    def auto_decouple(self):
        if self.state == self.IDLE:
            self.state = self.DECOUPLING

    def _trainset_changed(self, model, name):
        print(name)



