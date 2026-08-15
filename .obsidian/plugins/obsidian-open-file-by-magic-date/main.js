'use strict';

var obsidian = require('obsidian');

/******************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
/* global Reflect, Promise */

var extendStatics = function(d, b) {
    extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
    return extendStatics(d, b);
};

function __extends(d, b) {
    if (typeof b !== "function" && b !== null)
        throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
    extendStatics(d, b);
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
}

var __assign = function() {
    __assign = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};

function __awaiter(thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
}

function __generator(thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
}

// How many files are allowed to be configured?
var FILE_LIMIT = 10;
// iso weekday spec
var DAYS = {
    mon: 1,
    tue: 2,
    wed: 3,
    thu: 4,
    fri: 5,
    sat: 6,
    sun: 7,
};
var ICONS = [
    '🔮',
    '💎',
    '🍏',
    '🌼',
    '🍎',
    '💜',
    '🌀',
    '🐉',
    '⭐',
    '🚗',
];
var DEFAULT_SETTINGS = {
    files: [
        'journal/{YYYY-MM-DD}.md'
    ],
    useExistingPane: true,
};
// ---------------------------------------------------- Plugin Definition
var MagicFileHotkeyPlugin = /** @class */ (function (_super) {
    __extends(MagicFileHotkeyPlugin, _super);
    function MagicFileHotkeyPlugin() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MagicFileHotkeyPlugin.prototype.onload = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.loadSettings()];
                    case 1:
                        _a.sent();
                        console.log('loading ' + this.manifest.name);
                        this.addSettingTab(new SettingsTab(this.app, this));
                        this.resetCommands();
                        return [2 /*return*/];
                }
            });
        });
    };
    MagicFileHotkeyPlugin.prototype.onunload = function () {
        console.log('unloading ' + this.manifest.name);
    };
    MagicFileHotkeyPlugin.prototype.loadSettings = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        // this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
                        _a = this;
                        _b = [__assign({}, DEFAULT_SETTINGS)];
                        return [4 /*yield*/, this.loadData()];
                    case 1:
                        // this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
                        _a.settings = __assign.apply(void 0, _b.concat([_c.sent()]));
                        return [2 /*return*/];
                }
            });
        });
    };
    // note: this is called ~every keystroke, so be aware
    MagicFileHotkeyPlugin.prototype.saveSettings = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.saveData(this.settings)];
                    case 1:
                        _a.sent();
                        // update the commands, which is what hotkeys are set against
                        this.resetCommands();
                        return [2 /*return*/];
                }
            });
        });
    };
    MagicFileHotkeyPlugin.prototype.resetCommands = function () {
        var _this = this;
        var _loop_1 = function (i) {
            var id = "open-file-".concat(i); // should not change over time. app name automatically added to prefix
            var fileNameSpec = (this_1.settings.files[i] || '').trim();
            // const fileNameSpecNoExt = fileNameSpec.substring(0, fileNameSpec.lastIndexOf(".")) || fileNameSpec;
            var egName = lockInDate(fileNameSpec);
            // repeatedly calling with the same ID appears to be effectively an "update" operation
            if (fileNameSpec) {
                this_1.addCommand({
                    id: id,
                    name: "".concat(i + 1, " ").concat(ICONS[i], "  '").concat(egName, "'"),
                    callback: function () {
                        var fileName = lockInDate(fileNameSpec);
                        _this.openFile(fileName);
                    },
                    // doesn't prevent from showing as an available hotkey:
                    // checkCallback: (checking) => {
                    // 	if (!fileNameSpec) return false; // not available
                    // 	return true;
                    // }
                });
            }
        };
        var this_1 = this;
        for (var i = 0; i < FILE_LIMIT; i++) {
            _loop_1(i);
        }
    };
    // Desired behavior: focus the tab if it's already open. Open a new tab if it's not.
    // This would be simple, except for one thing:
    // the file you want to open might ALREADY be open in another tab.
    // That's the reason for "iterateAllLeaves"
    MagicFileHotkeyPlugin.prototype.openFile = function (fileName) {
        var _this = this;
        // See if there's a tab open with this file in it:
        var found = false;
        this.app.workspace.iterateAllLeaves(function (leaf) {
            var file = leaf.view.file;
            if ((file === null || file === void 0 ? void 0 : file.path) === fileName) {
                _this.app.workspace.revealLeaf(leaf);
                if (leaf.view instanceof obsidian.MarkdownView) {
                    leaf.view.editor.focus();
                }
                found = true;
                // console.log('FOUND A LEAF!', leaf);
                return; // don't keep looking
            }
        });
        // Case: there isn't already a tab open with this file
        if (!found) {
            /*
            docs:
            https://marcus.se.net/obsidian-plugin-docs/reference/typescript/classes/Workspace#openlinktext
            openLinkText(
                linktext: string,
                sourcePath: string,
                newLeaf?: PaneType | boolean, // PaneType = 'tab' | 'split' | 'window'; // 2023-01-28: out of date docs. "Argument of type 'string' is not assignable to parameter of type 'boolean'"
                openViewState?: OpenViewState // no idea. https://marcus.se.net/obsidian-plugin-docs/reference/typescript/interfaces/OpenViewState
                )
            */
            this.app.workspace.openLinkText(fileName, "", true);
        }
    };
    return MagicFileHotkeyPlugin;
}(obsidian.Plugin));
// ---------------------------------------------------- Settings Tab
var SettingsTab = /** @class */ (function (_super) {
    __extends(SettingsTab, _super);
    function SettingsTab(app, plugin) {
        var _this = _super.call(this, app, plugin) || this;
        _this.plugin = plugin;
        return _this;
    }
    SettingsTab.prototype.display = function () {
        var _this = this;
        // limit number of files allowed
        this.plugin.settings.files = this.plugin.settings.files.slice(0, FILE_LIMIT);
        this.plugin.saveSettings();
        // remove empty entries
        // this.plugin.settings.files = this.plugin.settings.files.filter(file => file != null && file != "");
        var containerEl = this.containerEl;
        containerEl.empty();
        var className = String(this.plugin.manifest.name).toLowerCase().replace(/\s/g, '-');
        containerEl.addClass(className);
        containerEl.createEl("h2", { text: this.plugin.manifest.name });
        var fileCount = this.plugin.settings.files.length || 1; // at least one, always.
        for (var i = 0; i < fileCount; i++) {
            this.renderSettingsRow(i);
        }
        if (this.plugin.settings.files.length < FILE_LIMIT) {
            new obsidian.Setting(this.containerEl).addButton(function (cb) {
                cb
                    // .setButtonText('Add another file') // can't have both icon and text?
                    .setTooltip('Add another file')
                    .setIcon('plus')
                    .onClick(onClickAdd.bind(_this));
            }).setClass('add-row');
        }
        function onClickAdd() {
            this.plugin.settings.files.push(''); // new empty file spec
            this.plugin.saveSettings();
            this.display();
        }
        containerEl.createEl("h2", { text: 'Tips', cls: 'margin-top' });
        // add an explanation, but with more room
        var descEl = containerEl.createEl('div', { cls: 'setting-item-description info-tips' }); // small text
        descEl.innerHTML = "\n\t\t<p>Use curly brackets to add date formats. eg: \"{YYYY-MM-DD}\".</p>\n\t\t<p>Any syntax from the <a href=\"https://momentjscom.readthedocs.io/en/latest/moment/04-displaying/01-format/\">moment.js</a> library will work.</p>\n\t\t<p>Additionally,  accepts a special format to indicate \"prior monday\". eg: \"{mon:YYYY-MM-DD}\"</p>\n\t\t<p>Include the '.md' extension in your filename if you use that.</p>\n\t\t";
    };
    SettingsTab.prototype.renderSettingsRow = function (idx) {
        var _this = this;
        var curVal = this.plugin.settings.files[idx];
        var setting = new obsidian.Setting(this.containerEl).setName("".concat(ICONS[idx], "  file:"));
        setting.controlEl.addClass('flex-kids-y');
        setting.controlEl.addClass('flex-start');
        setting.addText(function (cb) {
            cb
                .setPlaceholder("dir/{YYYY-MM-DD} file.md")
                .setValue(curVal)
                .onChange(onChange.bind(_this));
        });
        // add an element to print out the computed path
        var outputEl = setting.controlEl.createEl('div', {
            text: lockInDate(curVal),
            cls: 'setting-item-description', // small, muted
        });
        function onChange(value) {
            renderValidation(value, outputEl);
            this.onFileSettingChanged(idx, value);
        }
        // init the validation state
        // TODO: better way to get value of a setting?
        var curVal = setting.components[0].getValue();
        renderValidation(curVal, outputEl);
    };
    // whenever the user types and changes the file spec setting
    SettingsTab.prototype.onFileSettingChanged = function (idx, value) {
        this.plugin.settings.files[idx] = value;
        // remove any empty files and save:
        this.plugin.settings.files = this.plugin.settings.files.map(function (str) { return (str || '').trim(); }).filter(Boolean);
        this.plugin.saveSettings();
    };
    return SettingsTab;
}(obsidian.PluginSettingTab));
// For a given value, 
function renderValidation(value, outputEl) {
    if (!value)
        return outputEl.innerText = '';
    // Tell user how/if we parsed it
    var parsedName = lockInDate(value);
    outputEl.innerText = "\"".concat(parsedName, "\"");
    // Nothing Parsed, so we aren't using the date syntax
    if (parsedName === value) {
        outputEl.style.color = 'inherit';
        // Parser changed something, so date syntax is active
    }
    else {
        // colored purple if date syntax is active
        outputEl.style.color = 'var(--text-accent)';
    }
    // Checkmark if it also matches an existing file
    // this is a little funny, I think because Obsidian can match filenames with and without directories
    if (exists(parsedName)) {
        outputEl.innerText = "\"".concat(parsedName, "\" \u2705");
    }
}
// convert the input format YYYY to the current date
function lockInDate(inputString) {
    var now = obsidian.moment();
    var str = inputString;
    // If there's a weekday prefix, send that to the preceding, matching day
    // send anything in curlies "{mon:...}" to moment.format for the preceeding monday
    // eg: `Weekly Notes/{mon:YYYY-MM-DD} week.md`
    str = str.replace(/{mon:(.*)}/g, function (_match, captured) { return getPreviousWeekday(DAYS.mon).format(captured); });
    str = str.replace(/{tue:(.*)}/g, function (_match, captured) { return getPreviousWeekday(DAYS.tue).format(captured); });
    str = str.replace(/{wed:(.*)}/g, function (_match, captured) { return getPreviousWeekday(DAYS.wed).format(captured); });
    str = str.replace(/{thu:(.*)}/g, function (_match, captured) { return getPreviousWeekday(DAYS.thu).format(captured); });
    str = str.replace(/{fri:(.*)}/g, function (_match, captured) { return getPreviousWeekday(DAYS.fri).format(captured); });
    str = str.replace(/{sat:(.*)}/g, function (_match, captured) { return getPreviousWeekday(DAYS.sat).format(captured); });
    str = str.replace(/{sun:(.*)}/g, function (_match, captured) { return getPreviousWeekday(DAYS.sun).format(captured); });
    // send anything in curlies "{...}" to moment.format
    // eg: `Daily Notes/{YYYY-MM-DD}.md`
    // replace the entire match with a moment formatted version of the capture group
    str = str.replace(/{(.*)}/g, function (_match, captured) { return now.format(captured); });
    return str;
}
// Get the date of the previous day of the week you'd like. (eg: the most recent Monday)
// isoWeekday: 1 for Monday, 7 for Sunday.
function getPreviousWeekday(day) {
    var t = obsidian.moment();
    var guess = t.isoWeekday();
    var i = 0;
    while (day !== guess && i <= 7) {
        t.subtract(1, 'days');
        guess = t.isoWeekday();
        i++; // infinite loop blocker
    }
    return t;
}
// Check if a file exists. Depends on `app` global.
function exists(filename) {
    var ref = app.metadataCache.getFirstLinkpathDest(filename, "");
    return ref != null;
}

module.exports = MagicFileHotkeyPlugin;


/* nosourcemap */