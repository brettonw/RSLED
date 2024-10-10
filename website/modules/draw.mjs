import { Vector2, Vec2, V2 } from "./vector2.mjs"
import { formatNumber } from "./utility.mjs";

// not really a wrapper around a single draw element, a half hybrid of a global state and an object
export let Draw = function () {
    let _ = Object.create(null);

    // allowed states
    const STROKE_COLOR = "strokeColor";
    const STROKE_WIDTH = "strokeWidth";
    const FILL_COLOR = "fillColor";
    const OPACITY = "opacity";
    const TEXT_CLASS = "textClass";

    const DEFAULT_STATE = {
        strokeColor:    "black",
        strokeWidth:    0.1,
        fillColor:      "none",
        opacity:        1,
        textClass:      "number"
    };

    let copy_obj = function (obj) {
        return Object.assign (Object.create(null), obj)
    };

    let states = [copy_obj(DEFAULT_STATE)];

    _.clear = function () {
        states = [copy_obj(DEFAULT_STATE)];
    }

    _.push = function () {
        // create a new state object as a copy of the current state
        states.push(copy_obj(states[states.length - 1]));
        return this;
    };

    _.pop = function () {
        if (states.length > 1) {
            states.pop();
        }
        return this;
    };

    _.set = function(state, value) {
        if (state in DEFAULT_STATE) {
            states[states.length - 1][state] = value;
        }
        return this;
    };

    // helpers
    _.setStrokeColor = function (newValue) {
        return this.set(STROKE_COLOR, newValue);
    };

    _.setStrokeWidth = function (newValue) {
        return this.set(STROKE_WIDTH, newValue);
    };

    _.setFillColor = function (newValue) {
        return this.set(FILL_COLOR, newValue);
    };

    _.setOpacity = function (newValue) {
        return this.set(OPACITY, newValue);
    };

    _.setTextClass = function (newValue) {
        return this.set(TEXT_CLASS, newValue);
    };

    // internal function to get the requested state
    let get = function(state) {
        return states[states.length - 1][state];
    };

    // svg begin/end to clear the buffer and return the final built buffer
    let svg = "";

    _.begin = function () {
        _.clear ();
        svg = "";
        return this;
    };

    _.end = function () {
        return svg;
    };

    // svg drawing accumulation routines
    _.line = function (from, to) {
        svg += '<line x1="' + from.x + '" y1="' + from.y + '" x2="' + to.x + '" y2="' + to.y + '"';
        svg += ' stroke="' + get(STROKE_COLOR) + '" stroke-width="' + get(STROKE_WIDTH) + '"';
        svg += ' opacity="' + get(OPACITY) + '"';
        svg += ' />';
        return this;
    };

    _.polyline = function (pts) {
        svg += '<polyline stroke="' + get(STROKE_COLOR) + '" stroke-width=' + get(STROKE_WIDTH);
        svg += ' points="';
        let pad = '';
        for (let pt of pts) {
            svg += pad + pt.x + ',' + pt.y;
            pad = ' ';
        }
        svg += '" opacity="' + get(OPACITY) + '" fill="none" stroke-linejoin="round" />';
        return this;
    };

    _.circle = function (at, half, color, title) {
        color = (typeof (color) !== "undefined") ? color : get(FILL_COLOR);
        svg += '<circle cx="' + at.x + '" cy="' + at.y + '" r="' + half + '"';
        svg += ' stroke="' + get(STROKE_COLOR) + '" stroke-width="' + get(STROKE_WIDTH) + '"';
        svg += ' opacity="' + get(OPACITY) + '" fill="' + color + '"';
        if (typeof (title) === "undefined") {
            title = "(" + formatNumber(at.x, 1, 3) + ", " + formatNumber(at.y, 1, 3) + ")";
        }
       // svg += (typeof (title) !== "undefined") ? '><title>' + title + '</title></rect>' : ' />';
        svg += '><title>' + title + '</title></circle>';
        return this;
    };

    _.box = function (at, half, color, title) {
        color = (typeof (color) !== "undefined") ? color : get(FILL_COLOR);
        let size = half + half;
        svg += '<rect x="' + (at.x - half) + '" y="' + (at.y - half) + '" width="' + size + '" height="' + size + '"';
        svg += ' stroke="' + get(STROKE_COLOR) + '" stroke-width="' + get(STROKE_WIDTH) + '"';
        svg += ' opacity="' + get(OPACITY) + '" fill="' + color + '"';
        svg += (typeof (title) !== "undefined") ? '><title>' + title + '</title></rect>' : ' />';
        return this;
    };

    _.multi = function (func, pts, half, color) {
        // half is one size value or an array of sizes, color is one color value or an array of colors
        half = Array.isArray(half) ? half : Array(pts.length).fill (half);
        color = Array.isArray(color) ? color : Array(pts.length).fill (color);

        // loop over all the points to do the thing
        for (const [i, pt] of pts.entries()) {
            _[func](pt, half[i], color[i]);
        }
        return this;
    };

    _.text = function (txt, at) {
        svg += '<g transform="scale(1, -1)">';
        svg += '<text x="' + at.x + '" y="' + -at.y + '" dominant-baseline="middle" text-anchor="middle" class="text' + get(TEXT_CLASS) + '">' + txt + '</text>';
        svg += "</g>";
        return this;
    }

    // function to set up the drawing board
    _.graph = function (displaydivId, contentNodeId, gridSize = 10) {
        let displayDiv = document.getElementById (displaydivId);
        let displayWidth = displayDiv.offsetWidth;
        let displayHeight = displayDiv.offsetHeight;

        // create the raw SVG picture for display
        svg = '<div style="background-color: yellow; width: 100%; height: 100%; display: block;">';
        svg += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" ';

        // compute the viewbox from the desired size with a bit of buffer
        let buffer = 0.1;
        let l, t, w, h;
        if (displayWidth > displayHeight) {
            let ratio = displayWidth / displayHeight;
            t = -buffer * displayHeight;
            l = t * ratio;
            h = displayHeight * (1.0 + (buffer * 2.0));
            w = h * ratio;
        } else {
            let ratio = displayHeight / displayWidth;
            l = -buffer * displayWidth;
            t = l * ratio;
            w = displayWidth * (1.0 + (buffer * 2.0));
            h = w * ratio;
        }
        svg += 'viewBox="' + l + ', ' + t + ', ' + w + ', ' + h + '" ';
        svg += 'preserveAspectRatio="xMidYMid meet"';
        svg += '>';

        // set it up as a standard cartesian display, in the range (-180 ... 180, -90 ... 90)
        svg += '<g transform="translate(' + (displayWidth / 2.0) + ', ' + (displayHeight / 2.0) + ')">';
        svg += '<g transform="scale(' + (displayHeight / 180.0) + ')">';
        svg += '<g transform="scale(1, -1)">';
        svg += '<g transform="translate(-180, 0)">';
        svg += '<g>';

        // draw a grid, every gridSize x gridSize degrees
        if (gridSize >= 2) {
            _
                .setOpacity(0.5)
                .setStrokeWidth(0.1)
                .setStrokeColor("#999");
            for (let y = 0; y <= 90; y += gridSize) _.line(V2(0, y), V2(360, y));
            for (let y = 0; y >= -90; y -= gridSize) _.line(V2(0, y), V2(360, y));
            for (let x = 0; x <= 360; x += gridSize) _.line(V2(x, -90), V2(x, 90));
        }

        _
            .setOpacity (0.75)
            .setStrokeWidth (0.5)
            .setStrokeColor ("black");
        _.line(V2(-0, 0), V2(360, 0));
        _.line(V2(0, -90), V2(0, 90));

        _.text("0", V2(0, -98));
        _.text("180", V2(180, -98));
        _.text("360", V2(360, -98));

        _.text("-90", V2(-8, -90));
        _.text("0", V2(-8, 0));
        _.text("90", V2(-8, 90));

        // this is where the actual dynamic content goes...
        svg += '<g id="' + contentNodeId + '">';

        // close the SVG groups
        svg += '</g>';
        svg += '</g>';
        svg += '</g>';
        svg += '</g>';
        svg += '</g>';
        svg += '</g>';

        // close the plot
        svg += "</div><br>";
        displayDiv.innerHTML = svg;
        return document.getElementById (contentNodeId);
    };

    return _;
} ();
