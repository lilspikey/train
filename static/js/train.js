(function(){
    var onopen = function(ws) {
        var set_throttle = _.debounce(function(power) {
            ws.send('{ "power": '+ Math.round(power) +' }');
        }, 40);

        // TODO scale width height to full windows size
        var layout = Raphael('layout', 640, 480);
    
        var throttle = layout.circle(50, 100, 50).
            attr("fill", "#f00");

        var start = function () {
            this.ox = this.attr("cx");
            this.oy = this.attr("cy");
            this.animate({r: 60, opacity: .5}, 250, ">");
        },
        move = function (dx, dy) {
            this.attr({cx: this.ox + dx, cy: this.oy + dy});
            var cx = this.attr('cx');
            var width = layout.width;
            var power = 1024 * cx / width;
            set_throttle(power);
        },
        up = function () {
            this.animate({r: 50, opacity: 1}, 250, ">");
        };
        
        throttle.drag(move, start, up);
    };
    
    var host = window.location.host;
    var ws = new WebSocket("ws://"+host+"/ws");
    ws.onopen = function() {
        onopen(ws);
    };
    
})();
