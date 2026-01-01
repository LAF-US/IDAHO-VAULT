import test from "node:test";
import assert from "node:assert/strict";
import { chartColorContext, colorNameFromHex, hexToHsv, hsvToHex } from "../src/components/chart-color-utils.js";

test("editor portals carry only referenced authored color tokens without changing the spec", () => {
  const spec = { type: "line", colors: { East: "var(--regional-east)", West: "color-mix(in srgb, var(--regional-west) 60%, var(--surface))" } };
  const before = JSON.stringify(spec);
  const values = { "--regional-east": " light-dark(#ff66ad, #ff8cc1) ", "--regional-west": "#0285ff", "--surface": "#fff", "--layout-width": "1600px" };
  assert.deepEqual(chartColorContext(spec, { getPropertyValue: key => values[key] ?? "" }), {
    "--regional-east": "light-dark(#ff66ad, #ff8cc1)", "--regional-west": "#0285ff", "--surface": "#fff",
  });
  assert.equal(JSON.stringify(spec), before);
  assert.deepEqual(chartColorContext(spec, null), {});
});

test("custom picker HSV coordinates round-trip the selected hex", () => {
  for (const hex of ["#2a6fcf", "#0285ff", "#000000", "#ffffff", "#808080", "#ff0000", "#00ff00", "#0000ff"]) {
    assert.equal(hsvToHex(hexToHsv(hex)), hex);
  }
});
test("custom picker field matches white, hue, and black corners", () => {
  assert.equal(hsvToHex({ hue: 240, saturation: 0, value: 100 }), "#ffffff");
  assert.equal(hsvToHex({ hue: 240, saturation: 100, value: 100 }), "#0000ff");
  assert.equal(hsvToHex({ hue: 240, saturation: 100, value: 0 }), "#000000");
});

test("theme palette labels describe the resolved color rather than the chart token position", () => {
  const colors = {
    "#b6ff3b": "Lime",
    "#ff4fd8": "Magenta",
    "#00e6ff": "Cyan",
    "#0285ff": "Blue",
    "#924ff7": "Purple",
    "#04b84c": "Green",
    "#fb6a22": "Orange",
    "#ff66ad": "Pink",
    "#ffc300": "Yellow",
    "#fa423e": "Red",
    "#8f8f8f": "Gray",
    "#ffffff": "White",
    "#000000": "Black",
  };
  for (const [color, expected] of Object.entries(colors)) {
    assert.equal(colorNameFromHex(color), expected, `${color} should be named for its actual hue`);
  }
  assert.equal(colorNameFromHex("var(--chart-1)"), "Theme color");
});
