#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

function argValue(name) {
  const prefix = `--${name}=`;
  const inline = process.argv.find((arg) => arg.startsWith(prefix));
  if (inline) return inline.slice(prefix.length);
  const index = process.argv.indexOf(`--${name}`);
  return index >= 0 ? process.argv[index + 1] : "";
}

const inputPath = argValue("input");
const outputPath = argValue("output");
const pitch = argValue("pitch");
const speed = argValue("speed");
const mouth = argValue("mouth");
const throat = argValue("throat");

if (!inputPath || !outputPath) {
  console.error("Usage: hermes-sam-tts.js --input INPUT.txt --output OUTPUT.wav");
  process.exit(2);
}

const skillDir = "/Users/logan/.openclaw/workspace/skills/sam-tts";
const wrapper = path.join(skillDir, "scripts", "sam-tts-wrapper.js");

const text = fs.readFileSync(inputPath, "utf8").replace(/\s+/g, " ").trim();
if (!text) {
  console.error("Input text is empty");
  process.exit(2);
}

const result = spawnSync(
  process.execPath,
  [
    wrapper,
    text,
    `--output=${outputPath}`,
    "--quiet",
    ...(pitch ? [`--pitch=${pitch}`] : []),
    ...(speed ? [`--speed=${speed}`] : []),
    ...(mouth ? [`--mouth=${mouth}`] : []),
    ...(throat ? [`--throat=${throat}`] : []),
  ],
  {
    cwd: skillDir,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  },
);

if (result.status !== 0) {
  process.stderr.write(result.stderr || result.stdout || "SAM TTS failed");
  process.exit(result.status || 1);
}

if (!fs.existsSync(outputPath) || fs.statSync(outputPath).size === 0) {
  console.error("SAM TTS did not produce an output file");
  process.exit(1);
}

process.stdout.write(result.stdout || JSON.stringify({ success: true, outputPath }));
