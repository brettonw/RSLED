let Blackbody = function () {
    let _ = Object.create (null);

    // there are 41 steps at 10nm/step from 380nm to 780nm (inclusive) (the visible spectrum)
    const TEN_NM_STEPS = 41;
    const PI = Math.PI;

    // CIE standard   1       2       3       4       5       6       7       8       9      10       1       2       3       4       5       6       7       8       9      20       1       2       3       4       5       6       7       8       9      30       1       2       3       4       5       6       7       8       9      40       1
    let CIE_x = [0.0014, 0.0042, 0.0143, 0.0435, 0.1344, 0.2839, 0.3483, 0.3362, 0.2908, 0.1954, 0.0956, 0.0320, 0.0049, 0.0093, 0.0633, 0.1655, 0.2904, 0.4334, 0.5945, 0.7621, 0.9163, 1.0263, 1.0622, 1.0026, 0.8544, 0.6424, 0.4479, 0.2835, 0.1649, 0.0874, 0.0468, 0.0227, 0.0114, 0.0058, 0.0029, 0.0014, 7.0E-4, 3.0E-4, 2.0E-4, 1.0E-4, 0.0000];
    let CIE_y = [0.0000, 1.0E-4, 4.0E-4, 0.0012, 0.0040, 0.0116, 0.0230, 0.0380, 0.0600, 0.0910, 0.1390, 0.2080, 0.3230, 0.5030, 0.7100, 0.8620, 0.9540, 0.9950, 0.9950, 0.9520, 0.8700, 0.7570, 0.6310, 0.5030, 0.3810, 0.2650, 0.1750, 0.1070, 0.0610, 0.0320, 0.0170, 0.0082, 0.0041, 0.0021, 0.0010, 5.0E-4, 3.0E-4, 1.0E-4, 1.0E-4, 0.0000, 0.0000];
    let CIE_z = [0.0065, 0.0201, 0.0679, 0.2074, 0.6456, 1.3856, 1.7471, 1.7721, 1.6692, 1.2876, 0.8130, 0.4652, 0.2720, 0.1582, 0.0782, 0.0422, 0.0203, 0.0087, 0.0039, 0.0021, 0.0017, 0.0011, 8.0E-4, 3.0E-4, 2.0E-4, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000];
    let XYZW = [[0.67, 0.33], [0.21, 0.71], [0.14, 0.08], [0.31, 0.316]];

    // plot an energy curve for an ideal black body at the requested temperature
    let computeBlackbody = function (temperature) {
        let blackbody = [];
        let h = 6.626176E-34, k = 1.380662E-23, c = 2.997925E8;
        let hc = h * c, c1 = 2.0 * PI * hc * c, c2 = hc / k;
        for(let i = 0; i < TEN_NM_STEPS; ++i) {
            let wavelength = ((i * 10.0) + 380.0) * 1.0E-9;
            let value = c1 / (Math.pow(wavelength, 5.0) * (Math.pow(Math.exp(1.0), c2 / (wavelength * temperature)) - 1.0));
            blackbody.push (value);
        }
        return blackbody;
    };

    let normalizeRGBColor = function (red, green, blue) {
        let max = Math.max (Math.max (red, green), blue);
        return [red / max, green / max, blue / max];
    };

    let normalizeXYZColor = function (x, y, z) {
        let result = [];
        let xw = XYZW[3][0], yw = XYZW[3][1];
        let Xw = xw / yw, Yw = 1.0, Zw = (1.0 - xw - yw) / yw;
        result.push (x + ((Xw - x) * 0.005));
        result.push (y + ((Yw - y) * 0.005));
        result.push (z + ((Zw - z) * 0.005));
        return result;
    };

    let XYZtoRGB = function (x, y, z) {
        // XXX these should be matrix operations
        let xr = XYZW[0][0], xg = XYZW[1][0], xb = XYZW[2][0], xw = XYZW[3][0];
        let yr = XYZW[0][1], yg = XYZW[1][1], yb = XYZW[2][1], yw = XYZW[3][1];
        let Cr = 1.0 / yw * (xw * (yg - yb) - yw * (xg - xb) + xg * yb - xb * yg);
        let Cg = 1.0 / yw * (xw * (yb - yr) - yw * (xb - xr) - xr * yb + xb * yr);
        let Cb = 1.0 / yw * (xw * (yr - yg) - yw * (xr - xg) + xr * yg - xg * yr);
        let red = (x * ((yg - yb - xb * yg + yb * xg) / Cr)) + (y * ((xb - xg - xb * yg + xg * yb) / Cr)) + (z * ((xg * yb - xb * yg) / Cr));
        let green = (x * ((yb - yr - yb * xr + yr * xb) / Cg)) + (y * ((xr - xb - xr * yb + xb * yr) / Cg)) + (x * ((xb * yr - xr * yb) / Cg));
        let blue = (x * ((yr - yg - yr * xg + yg * xr) / Cb)) + (y * ((xg - xr - xg * yr + xr * yg) / Cb)) + (z * ((xr * yg - xg * yr) / Cb));
        if ((red >= 0.0) && (green >= 0.0) && (blue >= 0.0)) {
            return normalizeRGBColor(red, green, blue);
        } else {
            let normalizedColor = normalizeXYZColor (x, y, z);
            return XYZtoRGB(normalizedColor[0], normalizedColor[1], normalizedColor[2]);
        }
    };

    // compute the XYZ color by convolving the sensor response curves with the
    // (normalized) blackbody curve and then convert that to an RGB color
    let getColorOfCurve = function (curve) {
        let x = 0.0, y = 0.0, z = 0.0;
        for(let i = 0; i < TEN_NM_STEPS; ++i) {
            let value = curve[i];
            x += CIE_x[i] * value; y += CIE_y[i] * value; z += CIE_z[i] * value;
        }
        return XYZtoRGB(x, y, z);
    };

    let curveMax = function(curve) {
        let max = 0.0;
        for (let i = 0; i < TEN_NM_STEPS; ++i) {
            max = Math.max (max, curve[i]);
        }
        return max;
    };

    let scaleCurve = function (curve, multiplier) {
        let result = [];
        for(let i = 0; i < 41; ++i) {
            result.push (curve[i] * multiplier);
        }
        return result;
    };

    let normalizeCurve = function (curve) {
        return scaleCurve (curve, 1.0 / curveMax (curve));
    };

    _.colorAtTemperature = function (temperature) {
        let curve = computeBlackbody (temperature);
        curve = normalizeCurve (curve);
        return getColorOfCurve(curve);
    };

    _.makeBand = function (elementId, steps) {
        let innerHTML = '<div style="width:100%;height:100%;">';
        let min = 2000, max = 20000, delta = max - min, step = delta / steps;
        let width = (99 / steps);
        for (let i = 0; i < steps; ++i) {
            let temperature = min + (i * step);
            let c = _.colorAtTemperature(temperature);
            innerHTML += '<div style="display:inline-block;width:' + width + '%;height:100%;background-color:rgb(' + Math.floor (c[0] * 255) + ',' + Math.floor (c[1] * 255) + ',' + Math.floor (c[2] * 255) + ');">';
            innerHTML += '<span style="display:inline-block;transform:rotate(270deg);color:black;font-size:7px;margin-top:15px;margin-left:auto;margin-right:auto;"><span>' + Math.floor (temperature) + '°K</span></span>';
            innerHTML += '</div>';
        }
        document.getElementById(elementId).innerHTML = innerHTML + "</div>";
    };

    return _;
} ();

// reference for future adaptations:
// http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
// http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
