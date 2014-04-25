(function(){
    var onopen = function(ws) {
        var throttle_forward = function(power) {
            ws.send('{ "forward": '+ Math.round(power) +' }');
        };

        var throttle_reverse = function(power) {
            ws.send('{ "reverse": '+ Math.round(power) +' }');
        };

        var view_port = { width: 640, height: 480 };

        var update_throttle = _.throttle(function() {
            var cx = throttle.attr('cx');
            var width = view_port.width;
            var power = 1024 * 2*((cx/width) - 0.5);
            if ( power < 0 ) {
                throttle_reverse(-power);
            }
            else {
                throttle_forward(power);
            }
        }, 100);

        var layout = Raphael('layout', "100%", "100%");
        layout.setViewBox(0, 0, view_port.width, view_port.height, true);
        
        layout.path('M320 0L320 480').attr("stroke", "#333");
        layout.path('M0 20L0 460').attr("stroke", "#999");
        layout.path('M160 40L160 440').attr("stroke", "#ccc");
        layout.path('M480 40L480 440').attr("stroke", "#ccc");
        layout.path('M640 20L640 460').attr("stroke", "#999");
        var throttle = layout.circle(320, 100, 50).
            attr("fill", "#f00");

        var start = function () {
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
        var turnout_right = layout.rect(150, 200, 100, 100, 5).
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
    
    var host = window.location.host;
    var ws = new WebSocket("ws://"+host+"/ws");
    ws.onopen = function() {
        onopen(ws);
    };
    
})();
