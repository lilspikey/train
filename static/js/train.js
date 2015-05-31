(function(){
    var Status = Backbone.Model.extend({
    });
    
    var ThrottleView = Backbone.View.extend({
        initialize: function(options){
            this.throttle_range = options.throttle_range;
            this._down = false;
            this.listenTo(this.model, "change:forward", this.update);
            this.listenTo(this.model, "change:power", this.update);
            this.el.mousedown(_.bind(this.onMousedown, this));
            this.el.mousemove(_.bind(this.onMousemove, this));
            this.throttle_range.mousedown(_.bind(this.onMousedown, this));
            this.throttle_range.mousemove(_.bind(this.onMousemove, this));
            this.el.mouseup(_.bind(this.onMouseup, this));
            this.throttle_range.mouseup(_.bind(this.onMouseup, this));
        },
        onMousedown: function(event) {
            this.el.animate({r: 60, fill: "#866"}, 250, ">");
            this._down = true;
            this.handleThrottle(event);
        },
        onMousemove: function(event) {
            if ( this._down ) {
                this.handleThrottle(event);
            }
        },
        handleThrottle: function(event) {
            var x = event.clientX;
            var bnds = this.throttle_range[0].getBoundingClientRect();
            var mx = x - bnds.left;
            var fx = Math.max(0, Math.min(1, mx/bnds.width));
            if ( fx < 0.45 ) {
                throttle_reverse(2*1024*(0.5-fx));
            }
            else if ( fx > 0.55 ) {
                throttle_forward(2*1024*(fx-0.5));
            }
            else {
                throttle_forward(0);
            }
        },
        onMouseup: function() {
            this._down = false;
            this.el.animate({r: 50, fill: "#f00"}, 250, ">");
        },
        update: function() {
            var forward = this.model.get('forward');
            var power = this.model.get('power');
            var width = this.throttle_range.attr('width');
            var cx = this.throttle_range.attr('x') + width/2;
            var normalised = (power/1024) * (width/2);
            if ( forward ) {
                cx += normalised;
            }
            else {
                cx -= normalised;
            }
            this.el.attr('cx', cx);
        }
    });

    var TurnoutView = Backbone.View.extend({
        initialize: function(options){
            this.direction = options.direction;
            this.listenTo(this.model, "change:turnout", this.update);
            this.el.click(_.bind(this.onClick, this));
        },
        onClick: function() {
            turnout(this.direction);
        },
        update: function() {
            if ( this.model.get('turnout') == this.direction ) {
                this.el.animate({"fill": "#3f3"}, 250, ">");
            }
            else {
                this.el.animate({"fill": "#686"}, 250, ">");
            }
        }
    });

    var DecouplerView = Backbone.View.extend({
        initialize: function(options){
            this.direction = options.direction;
            this.listenTo(this.model, "change:decoupler", this.update);
            this.el.mousedown(_.bind(this.onMousedown, this));
            this.el.mouseup(_.bind(this.onMouseup, this));
        },
        onMousedown: function() {
            decoupler('up');
        },
        onMouseup: function() {
            decoupler('down');
        },
        update: function() {
            var state = this.model.get('decoupler');
            if ( state == 'up' ) {
                this.el.animate({"fill": "#668", y: 190}, 250, ">");
            }
            else if ( state == 'down' ) {
                this.el.animate({"fill": "#33f", y: 200}, 250, ">");
            }
        }
    });

    var SensorView = Backbone.View.extend({
        initialize: function(options) {
            this.name = options.name;
            this.listenTo(this.model, "change:" + this.name, this.update);
        },
        update: function() {
            var on = this.model.get(this.name);
            if ( on ) {
                this.el.animate({"fill": "#f90"}, 50, ">");
            }
            else {
                this.el.animate({"fill": "#630"}, 50, ">");
            }
        }
    });

    var LightView = Backbone.View.extend({
        initialize: function(options) {
            this.name = options.name;
            this.light_callback = options.light_callback;
            this.listenTo(this.model, "change:" + this.name, this.update);
            this.el.click(_.bind(this.onClick, this));
        },
        onClick: function() {
            var on = this.model.get(this.name);
            this.light_callback(!on);
        },
        update: function() {
            var on = this.model.get(this.name);
            if ( on ) {
                this.el.animate({"fill": "#ffd"}, 50, ">");
            }
            else {
                this.el.animate({"fill": "#333"}, 50, ">");
            }
        }
    });

    var status = new Status({
        forward: true,
        power: 0,
        decoupler: '',
        turnout: '',
        light1: false,
        light2: false
    });

    var host = window.location.host;
    var ws = new ReconnectingWebSocket("ws://"+host+"/ws");
    ws.onmessage = function(evt) {
        if ( evt.data ) {
            var json = JSON.parse(evt.data);
            if ( json.status ) {
                status.set(json.status);
            }
        }
    };

    var throttle_forward = _.throttle(function(power) {
        ws.send('{ "forward": '+ Math.round(power) +' }');
    }, 100);

    var throttle_reverse = _.throttle(function(power) {
        ws.send('{ "reverse": '+ Math.round(power) +' }');
    }, 100);

    var turnout = function(direction) {
        ws.send('{ "turnout": "' + direction + '" }');
    };
    var decoupler = function(direction) {
        ws.send('{ "decoupler": "' + direction + '" }');
    };
    var light1 = function(on) {
        ws.send('{ "light1": "' + (on? 'on' : 'off') + '" }');
    };
    var light2 = function(on) {
        ws.send('{ "light2": "' + (on? 'on' : 'off') + '" }');
    };
    
    var view_port = { width: 640, height: 480 };
    var layout = Raphael('layout', "100%", "100%");
    layout.setViewBox(0, 0, view_port.width, view_port.height, true);
        
    layout.path('M320 0L320 480').attr("stroke", "#333");
    layout.path('M0 20L0 460').attr("stroke", "#999");
    layout.path('M160 40L160 440').attr("stroke", "#ccc");
    layout.path('M480 40L480 440').attr("stroke", "#ccc");
    layout.path('M640 20L640 460').attr("stroke", "#999");
    
    var elements = layout.add([
        {
            type: 'rect',
            x: 0,
            y: 50,
            width: view_port.width,
            height: 100,
            fill: '#333',
            stroke: '#aaa',
            'stroke-width': 40
        },
        {
            type: 'circle',
            cx: 320,
            cy: 100,
            r: 50,
            fill: '#f00'
        },
        {
            type: 'rect',
            x: 0,
            y: 200,
            width: 100,
            height: 100,
            r: 5,
            fill: '#3f3'
        },
        {
            type: 'rect',
            x: 160,
            y: 200,
            width: 100,
            height: 100,
            r: 5,
            fill: '#686'
        },
        {
            type: 'rect',
            x: 540,
            y: 200,
            width: 100,
            height: 100,
            r: 5,
            fill: "#33f"
        },
        {
            type: 'rect',
            x: 0,
            y: 405,
            width: 100,
            height: 50,
            r: 5,
            fill: "#333"
        },
        {
            type: 'rect',
            x: 160,
            y: 405,
            width: 100,
            height: 50,
            r: 5,
            fill: "#333"
        }
    ]);
    var sensors = [];
    var sensors_width = 5 * view_port.width/6;
    var lx = (view_port.width - sensors_width)/2 - 25;
    for ( var i = 0; i < 6; i++ ) {
        var x = lx + (i * view_port.width)/6;
        sensors.push({
            type: 'rect',
            x: x,
            y: 330,
            width: 50,
            height: 50,
            r: 5,
            fill: '#630'
        });
    }
    sensors = layout.add(sensors);
    
    elements = {
        throttle_range: elements[0],
        throttle: elements[1],
        turnout_left: elements[2],
        turnout_right: elements[3],
        decoupler: elements[4],
        light1: elements[5],
        light2: elements[6],
        sensors: sensors
    };

    var throttle_view = new ThrottleView({model: status, el: elements.throttle, throttle_range: elements.throttle_range});
    throttle_view.update();

    var turnout_left_view = new TurnoutView({model: status, el: elements.turnout_left, direction: 'left'});
    var turnout_right_view = new TurnoutView({model: status, el:elements. turnout_right, direction: 'right'});
    
    var decoupler_view = new DecouplerView({model: status, el: elements.decoupler});

    for ( var i = 0; i < elements.sensors.length; i++ ) {
        var name = 'sensor' + (i+1);
        status.set(name, false);
        var sensor_view = new SensorView({model: status, el: elements.sensors[i], name: name});
    }

    var light1_view = new LightView({model: status, el: elements.light1, name: 'light1', light_callback: light1});
    var light2_view = new LightView({model: status, el: elements.light2, name: 'light2', light_callback: light2});
   
})();
