export let Degrees = function (){
    let _ = Object.create(null);

    _.HALF_CIRCLE_DEGREES = 180;
    _.FULL_CIRCLE_DEGREES = _.HALF_CIRCLE_DEGREES * 2;
    _.HALF_CIRCLE_RADIANS = Math.PI;
    _.FULL_CIRCLE_RADIANS = _.HALF_CIRCLE_RADIANS * 2;

    _.cos = function (angleDegrees) {
        return Math.cos(angleDegrees * _.FULL_CIRCLE_RADIANS / _.FULL_CIRCLE_DEGREES);
    };

// map an angle to the range [-180 ... 180)
    _.wrap = function (angleDegrees) {
        while (angleDegrees >= _.HALF_CIRCLE_DEGREES) angleDegrees -= _.FULL_CIRCLE_DEGREES;
        return angleDegrees;
    };

    return _;
}();
