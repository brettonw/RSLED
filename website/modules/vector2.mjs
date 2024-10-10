export let Vector2 = function () {
    let _ = Object.create (null);

    _.perp = function (left) {
        return Vec2.new (-left.y, left.x);
    };

    _.add = function (left, right) {
        return Vec2.new (left.x + right.x, left.y + right.y);
    };

    _.subtract = function (left, right) {
        return Vec2.new (left.x - right.x, left.y - right.y);
    };

    _.scale = function (left, right) {
        return Vec2.new (left.x * right, left.y * right);
    };

    _.dot = function (left, right) {
        return (left.x * right.x) + (left.y * right.y);
    };

    _.normSq = function (left) {
        return (left.x * left.x) + (left.y * left.y);
    };

    _.norm = function (left) {
        return Math.sqrt ((left.x * left.x) + (left.y * left.y));
    };

    _.normalize = function (left) {
        return _.scale (left, 1.0 / _.norm (left));
    };

    return _;
} ();

export let Vec2 = function () {
    let _ = Object.create (null);

    _.construct = function (x, y) {
        this.x = x;
        this.y = y;
        return this;
    };

    _.perp = function () {
        return Vector2.perp (this);
    };

    _.add = function (right) {
        return Vector2.add (this, right);
    };

    _.subtract = function (right) {
        return Vector2.subtract (this, right);
    };

    _.scale = function (right) {
        return Vector2.scale (this, right);
    };

    _.dot = function (right) {
        return Vector2.dot (this, right);
    };

    _.normSq = function () {
        return Vector2.normSq (this);
    };

    _.norm = function () {
        return Vector2.norm (this);
    };

    _.normalize = function () {
        let norm = Vector2.normalize (this);
    };

    _.new = function (x, y) {
        return Object.create (_).construct (x, y);
    };

    return _;
} ();

export let V2 = function (x, y) {
    return Vec2.new (x, y);
};
