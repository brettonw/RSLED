export let formatNumber = function (value, wholePlaces, decimalPlaces, unit = "") {
    const whole = Math.floor(value);
    const fraction = Math.round ((value - whole) * Math.pow(10, decimalPlaces)).toString().padStart(decimalPlaces, "0");
    return whole.toString().padStart(wholePlaces, " ") + "." + fraction + unit;
};

