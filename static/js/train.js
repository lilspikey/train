(function(){
    var Status = Backbone.Model.extend({
    });
    
    var ThrottleView = Backbone.View.extend({
        initialize: function(options){
            this.throttle_range = options.throttle_range;
            this.listenTo(this.model, "change:forward", this.update);
            this.listenTo(this.model, "change:power", this.update);
            this.el.mousedown(_.bind(this.onMousedown, this));
            this.throttle_range.mousedown(_.bind(this.onMousedown, this));
            this.el.mouseup(_.bind(this.onMouseup, this));
            this.throttle_range.mouseup(_.bind(this.onMouseup, this));
        },
        onMousedown: function(event) {
            this.el.animate({r: 60, fill: "#866"}, 250, ">");
            var bnds = event.target.getBoundingClientRect();
            var mx = event.clientX - bnds.left
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

    var status = new Status({
        forward: true,
        power: 0,
        decoupler: 0,
        turnoutLeft: 0,
        turnoutRight: 0
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

    var throttle_forward = function(power) {
        ws.send('{ "forward": '+ Math.round(power) +' }');
    };

    var throttle_reverse = function(power) {
        ws.send('{ "reverse": '+ Math.round(power) +' }');
    };

    var view_port = { width: 640, height: 480 };
    var layout = Raphael('layout', "100%", "100%");
    layout.setViewBox(0, 0, view_port.width, view_port.height, true);
        
    layout.path('M320 0L320 480').attr("stroke", "#333");
    layout.path('M0 20L0 460').attr("stroke", "#999");
    layout.path('M160 40L160 440').attr("stroke", "#ccc");
    layout.path('M480 40L480 440').attr("stroke", "#ccc");
    layout.path('M640 20L640 460').attr("stroke", "#999");
    
    var throttle_range = layout.rect(0, 50, view_port.width, 100).
         attr({ fill: "#333", stroke: "#aaa", 'stroke-width': 40});

    var throttle = layout.circle(320, 100, 50).
         attr("fill", "#f00");

    var throttle_view = new ThrottleView({model: status, el: throttle, throttle_range: throttle_range});
    throttle_view.update();


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
