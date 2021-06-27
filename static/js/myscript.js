// RainyDay My js code
function run() {
    var image = document.getElementById('background');
    image.onload = function () {
        var engine = new RainyDay({
            image: this,
            blur : 10,
            fps : 40
        });
        engine.rain([
            [3,2,2]
        ], 100);
    };
    image.crossOrigin = 'anonymous';
    image.src = 'https://images.pexels.com/photos/39811/pexels-photo-39811.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500';
}