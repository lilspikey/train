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
            var bnds = throttle_range[0].getBoundingClientRect();
            var mx = event.x - bnds.left;
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

    var status = new Status({
        forward: true,
        power: 0,
        decoupler: 0,
        turnout: 'left'
    });

    var host = window.location.host;
    var ws = new WebSocket("ws://"+host+"/ws");
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
        }
    ]);
    var throttle_range = elements[0]
    var throttle = elements[1];
    var turnout_left = elements[2];
    var turnout_right = elements[3];

    var throttle_view = new ThrottleView({model: status, el: throttle, throttle_range: throttle_range});
    throttle_view.update();

    var turnout_left_view = new TurnoutView({model: status, el: turnout_left, direction: 'left'});
    var turnout_right_view = new TurnoutView({model: status, el: turnout_right, direction: 'right'});

    /*    var start = function () {
            this.ox = this.attr("cx");
            this.oy = this.attr("cy");
            this.animate({r: 60, fill: "#866"}, 250, ">");
            update_throttle();
        },
        move = function (dx, dy) {
            this.attr({cx: this.ox + dx});
            update_throttle();
        },
        up = function () {
            var cx = this.attr("cx");
            var midx = view_port.width/2;
            if ( Math.abs(cx - midx) <= 40 ) {
                this.attr("cx", midx);
            }
            this.animate({r: 50, fill: "#f00"}, 250, ">");
            update_throttle();
        };
        
        throttle.drag(move, start, up);

        var turnout_left = layout.rect(0, 200, 100, 100, 5).
            attr("fill", "#3f3");
        var turnout_right = layout.rect(160, 200, 100, 100, 5).
            attr("fill", "#686");

        turnout_left.click(function() {
            ws.send('{ "turnout": "left" }');
            turnout_left.animate({"fill": "#3f3"}, 250, ">");
            turnout_right.animate({"fill": "#686"}, 250, ">");
        });
        turnout_right.click(function() {
            ws.send('{ "turnout": "right" }');
            turnout_right.animate({"fill": "#3f3"}, 250, ">");
            turnout_left.animate({"fill": "#686"}, 250, ">");
        });

        var decoupler = layout.rect(540, 200, 100, 100, 5).
            attr("fill", "#33f");

        decoupler.mousedown(function() {
            ws.send('{ "decoupler": "up" }');
            decoupler.animate({"fill": "#668", y: 190}, 250, ">");
        });
        decoupler.mouseup(function() {
            ws.send('{ "decoupler": "down" }');
            decoupler.animate({"fill": "#33f", y: 200}, 250, ">");
        });
    };
    */
    
})();
