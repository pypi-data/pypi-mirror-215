(self["webpackChunkjupysql_plugin"] = self["webpackChunkjupysql_plugin"] || []).push([["lib_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/connector.css":
/*!*******************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/connector.css ***!
  \*******************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _icons_delete_outline_black_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./icons/delete_outline_black.svg */ "./style/icons/delete_outline_black.svg");
/* harmony import */ var _icons_delete_outline_black_svg__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_icons_delete_outline_black_svg__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _icons_add_primary_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./icons/add_primary.svg */ "./style/icons/add_primary.svg");
/* harmony import */ var _icons_add_primary_svg__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_icons_add_primary_svg__WEBPACK_IMPORTED_MODULE_4__);
// Imports





var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()((_icons_delete_outline_black_svg__WEBPACK_IMPORTED_MODULE_3___default()));
var ___CSS_LOADER_URL_REPLACEMENT_1___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()((_icons_add_primary_svg__WEBPACK_IMPORTED_MODULE_4___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ":root {\n    --danger: #f53649;\n    --white: #ffffff;\n    --margin: 10px;\n    --primary: #206eef;\n  }\n\n.connector-widget .connection-button-container .connection-button-actions {\n    display: inline-flex;\n    width: 100%;\n}\n\n.connector-widget #connectionsButtonsContainer {\n    display: grid;\n}\n\n.connector-widget .connection-button-container .delete-connection-button {\n    margin-left: 10px;\n    background-repeat: no-repeat;\n    background-size: 24px;\n    background-position: center;\n    background-image: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ");\n    background-color: transparent;\n    border: none;\n    width: 24px;\n}\n\n.create-new-connection {\n    display: inline-flex;\n    color: var(--primary)\n}\n\n.create-new-connection:hover {\n    cursor: pointer;\n}\n\n.create-new-connection .icon{\n    background-image: url(" + ___CSS_LOADER_URL_REPLACEMENT_1___ + ");\n    min-width: 30px;\n    height: 30px;\n    background-repeat: no-repeat;\n    background-size: 15px;\n    background-position: center;\n    background-color: transparent;\n    margin: 0;    \n}\n\n.create-new-connection div {\n    margin: auto var(--margin);\n    margin-top: 2px;\n}\n\n.create-new-connection div:nth-child(2) {\n    margin-left: 2px;\n}\n\n.connector-widget .connection-button-container {\n    margin: var(--margin) 0;\n}\n\n.connector-widget hr.divider {\n    margin: 0;\n    margin-top:20px;\n}\n\n.connector-widget button {\n    width: fit-content;\n    border: none;\n    padding: 5px 10px;\n    border: 1px solid transparent;\n    border-radius: 5px;\n}\n\n.connector-widget button.secondary {\n    background-color: transparent;\n    border: 1px solid var(--primary);\n    color: var(--primary);\n}\n\n.connector-widget button.primary {\n    background-color: var(--primary);\n    color: #fff;\n    border: 1px solid var(--primary);\n}\n\n.connector-widget .connection-button-actions .connection-name {\n    margin: auto 30px;\n    margin-left: 0;\n    width: 100%;\n    font-weight: 500;\n}\n\nbutton.danger {\n    background-color: var(--danger);\n    color: var(--white);\n    margin-left: var(--margin);\n}\n\nform#connectionForm .field-container {\n    display: inline-flex;\n    width: 100%;\n    margin: var(--margin) 0;\n}\n\nform#connectionForm label {\n    width: 50%;\n    margin: auto 0;\n}\n\nform#connectionForm .field {\n    width: -webkit-fill-available;\n    margin-left: var(--margin);\n    padding: 5px 10px;\n}\n\nform#connectionForm input:not(input[type='submit']) {\n    /* margin: 10px;\n    padding: 5px 10px; */\n}\n\n#selectConnection {\n    width: 100%;\n    padding: 6px 10px;\n    margin-bottom: var(--margin);\n}\n\n.warning-message {\n    margin-bottom: var(--margin);\n}\n\n.block {\n    margin: 30px 0px;\n    /* border: 1px solid #000; */\n    width: 600px;\n}\n\nform#connectionForm .buttons-container {\n    text-align: right;\n    margin: var(--margin) 0;\n}\n\nform#connectionForm .buttons-container button:first-child {\n    margin-right: var(--margin);\n}", "",{"version":3,"sources":["webpack://./style/connector.css"],"names":[],"mappings":"AAAA;IACI,iBAAiB;IACjB,gBAAgB;IAChB,cAAc;IACd,kBAAkB;EACpB;;AAEF;IACI,oBAAoB;IACpB,WAAW;AACf;;AAEA;IACI,aAAa;AACjB;;AAEA;IACI,iBAAiB;IACjB,4BAA4B;IAC5B,qBAAqB;IACrB,2BAA2B;IAC3B,yDAAuD;IACvD,6BAA6B;IAC7B,YAAY;IACZ,WAAW;AACf;;AAEA;IACI,oBAAoB;IACpB;AACJ;;AAEA;IACI,eAAe;AACnB;;AAEA;IACI,yDAA8C;IAC9C,eAAe;IACf,YAAY;IACZ,4BAA4B;IAC5B,qBAAqB;IACrB,2BAA2B;IAC3B,6BAA6B;IAC7B,SAAS;AACb;;AAEA;IACI,0BAA0B;IAC1B,eAAe;AACnB;;AAEA;IACI,gBAAgB;AACpB;;AAEA;IACI,uBAAuB;AAC3B;;AAEA;IACI,SAAS;IACT,eAAe;AACnB;;AAEA;IACI,kBAAkB;IAClB,YAAY;IACZ,iBAAiB;IACjB,6BAA6B;IAC7B,kBAAkB;AACtB;;AAEA;IACI,6BAA6B;IAC7B,gCAAgC;IAChC,qBAAqB;AACzB;;AAEA;IACI,gCAAgC;IAChC,WAAW;IACX,gCAAgC;AACpC;;AAEA;IACI,iBAAiB;IACjB,cAAc;IACd,WAAW;IACX,gBAAgB;AACpB;;AAEA;IACI,+BAA+B;IAC/B,mBAAmB;IACnB,0BAA0B;AAC9B;;AAEA;IACI,oBAAoB;IACpB,WAAW;IACX,uBAAuB;AAC3B;;AAEA;IACI,UAAU;IACV,cAAc;AAClB;;AAEA;IACI,6BAA6B;IAC7B,0BAA0B;IAC1B,iBAAiB;AACrB;;AAEA;IACI;wBACoB;AACxB;;AAEA;IACI,WAAW;IACX,iBAAiB;IACjB,4BAA4B;AAChC;;AAEA;IACI,4BAA4B;AAChC;;AAEA;IACI,gBAAgB;IAChB,4BAA4B;IAC5B,YAAY;AAChB;;AAEA;IACI,iBAAiB;IACjB,uBAAuB;AAC3B;;AAEA;IACI,2BAA2B;AAC/B","sourcesContent":[":root {\n    --danger: #f53649;\n    --white: #ffffff;\n    --margin: 10px;\n    --primary: #206eef;\n  }\n\n.connector-widget .connection-button-container .connection-button-actions {\n    display: inline-flex;\n    width: 100%;\n}\n\n.connector-widget #connectionsButtonsContainer {\n    display: grid;\n}\n\n.connector-widget .connection-button-container .delete-connection-button {\n    margin-left: 10px;\n    background-repeat: no-repeat;\n    background-size: 24px;\n    background-position: center;\n    background-image: url('icons/delete_outline_black.svg');\n    background-color: transparent;\n    border: none;\n    width: 24px;\n}\n\n.create-new-connection {\n    display: inline-flex;\n    color: var(--primary)\n}\n\n.create-new-connection:hover {\n    cursor: pointer;\n}\n\n.create-new-connection .icon{\n    background-image: url('icons/add_primary.svg');\n    min-width: 30px;\n    height: 30px;\n    background-repeat: no-repeat;\n    background-size: 15px;\n    background-position: center;\n    background-color: transparent;\n    margin: 0;    \n}\n\n.create-new-connection div {\n    margin: auto var(--margin);\n    margin-top: 2px;\n}\n\n.create-new-connection div:nth-child(2) {\n    margin-left: 2px;\n}\n\n.connector-widget .connection-button-container {\n    margin: var(--margin) 0;\n}\n\n.connector-widget hr.divider {\n    margin: 0;\n    margin-top:20px;\n}\n\n.connector-widget button {\n    width: fit-content;\n    border: none;\n    padding: 5px 10px;\n    border: 1px solid transparent;\n    border-radius: 5px;\n}\n\n.connector-widget button.secondary {\n    background-color: transparent;\n    border: 1px solid var(--primary);\n    color: var(--primary);\n}\n\n.connector-widget button.primary {\n    background-color: var(--primary);\n    color: #fff;\n    border: 1px solid var(--primary);\n}\n\n.connector-widget .connection-button-actions .connection-name {\n    margin: auto 30px;\n    margin-left: 0;\n    width: 100%;\n    font-weight: 500;\n}\n\nbutton.danger {\n    background-color: var(--danger);\n    color: var(--white);\n    margin-left: var(--margin);\n}\n\nform#connectionForm .field-container {\n    display: inline-flex;\n    width: 100%;\n    margin: var(--margin) 0;\n}\n\nform#connectionForm label {\n    width: 50%;\n    margin: auto 0;\n}\n\nform#connectionForm .field {\n    width: -webkit-fill-available;\n    margin-left: var(--margin);\n    padding: 5px 10px;\n}\n\nform#connectionForm input:not(input[type='submit']) {\n    /* margin: 10px;\n    padding: 5px 10px; */\n}\n\n#selectConnection {\n    width: 100%;\n    padding: 6px 10px;\n    margin-bottom: var(--margin);\n}\n\n.warning-message {\n    margin-bottom: var(--margin);\n}\n\n.block {\n    margin: 30px 0px;\n    /* border: 1px solid #000; */\n    width: 600px;\n}\n\nform#connectionForm .buttons-container {\n    text-align: right;\n    margin: var(--margin) 0;\n}\n\nform#connectionForm .buttons-container button:first-child {\n    margin-right: var(--margin);\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/widget.css":
/*!****************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/widget.css ***!
  \****************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".custom-widget {\n    background-color: lightseagreen;\n    padding: 0px 2px;\n}", "",{"version":3,"sources":["webpack://./style/widget.css"],"names":[],"mappings":"AAAA;IACI,+BAA+B;IAC/B,gBAAgB;AACpB","sourcesContent":[".custom-widget {\n    background-color: lightseagreen;\n    padding: 0px 2px;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./lib/comm.js":
/*!*********************!*\
  !*** ./lib/comm.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   registerCommTargets: () => (/* binding */ registerCommTargets)
/* harmony export */ });
// Opens a comm from the frontend to the kernel
const registerCommTargets = (context) => {
    var _a;
    const sessionContext = context.sessionContext;
    const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    if (!kernel)
        return;
    // Listen to updateTableWidget event
    document.addEventListener("onUpdateTableWidget", async (event) => {
        const customEvent = event;
        const data = customEvent.detail.data;
        // Register to table_widget handler in the JupySQL kernel
        const comm = kernel.createComm("comm_target_handle_table_widget");
        await comm.open('initializing connection').done;
        // Send data to the Kernel to recevice rows to display
        comm.send(data);
        // Handle recevied rows
        comm.onMsg = (msg) => {
            const content = msg.content;
            const data = content.data;
            // Raise event to update table with new rows
            let customEvent = new CustomEvent('onTableWidgetRowsReady', {
                bubbles: true,
                cancelable: true,
                composed: false,
                detail: {
                    data: data
                }
            });
            document.body.dispatchEvent(customEvent);
        };
    });
};


/***/ }),

/***/ "./lib/connector.js":
/*!**************************!*\
  !*** ./lib/connector.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CompletionConnector: () => (/* binding */ CompletionConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// Modified from jupyterlab/packages/completer/src/connector.ts

/**
 * A multi-connector connector for completion handlers.
 */
class CompletionConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new connector for completion requests.
     *
     * @param connectors - Connectors to request matches from, ordered by metadata preference (descending).
     */
    constructor(connectors) {
        super();
        this._connectors = connectors;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        return Promise.all(this._connectors.map((connector) => connector.fetch(request))).then((replies) => {
            const definedReplies = replies.filter((reply) => !!reply);
            return Private.mergeReplies(definedReplies);
        });
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Merge results from multiple connectors.
     *
     * @param replies - Array of completion results.
     * @returns IReply with a superset of all matches.
     */
    function mergeReplies(replies) {
        // Filter replies with matches.
        const repliesWithMatches = replies.filter((rep) => rep.matches.length > 0);
        // If no replies contain matches, return an empty IReply.
        if (repliesWithMatches.length === 0) {
            return replies[0];
        }
        // If only one reply contains matches, return it.
        if (repliesWithMatches.length === 1) {
            return repliesWithMatches[0];
        }
        // Collect unique matches from all replies.
        const matches = new Set();
        repliesWithMatches.forEach((reply) => {
            reply.matches.forEach((match) => matches.add(match));
        });
        // Note that the returned metadata field only contains items in the first member of repliesWithMatches.
        return { ...repliesWithMatches[0], matches: [...matches] };
    }
    Private.mergeReplies = mergeReplies;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/customconnector.js":
/*!********************************!*\
  !*** ./lib/customconnector.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CustomConnector: () => (/* binding */ CustomConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _keywords_json__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./keywords.json */ "./lib/keywords.json");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A custom connector for completion handlers.
 */
class CustomConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new custom connector for completion requests.
     *
     * @param options - The instatiation options for the custom connector.
     */
    constructor(options) {
        super();
        this._editor = options.editor;
        this._sessionContext = options.sessionContext;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        if (!this._editor) {
            return Promise.reject('No editor');
        }
        return new Promise((resolve) => {
            resolve(Private.completionHint(this._editor, this._sessionContext));
        });
    }
}
/**
 * A namespace for Private functionality.
 */
var Private;
(function (Private) {
    /**
     * Get a list of mocked completion hints.
     *
     * @param editor Editor
     * @returns Completion reply
     */
    function completionHint(editor, sessionContext) {
        // Find the token at the cursor
        const cursor = editor.getCursorPosition();
        const token = editor.getTokenForPosition(cursor);
        var newTokenList = _keywords_json__WEBPACK_IMPORTED_MODULE_1__.keywords;
        const completionList = newTokenList.filter((t) => t.value.startsWith(token.value.toUpperCase())).map((t) => t.value);
        // Remove duplicate completions from the list
        const matches = Array.from(new Set(completionList));
        return {
            start: token.offset,
            end: token.offset + token.value.length,
            matches,
            metadata: {},
        };
    }
    Private.completionHint = completionHint;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/formatter.js":
/*!**************************!*\
  !*** ./lib/formatter.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JupyterlabNotebookCodeFormatter: () => (/* binding */ JupyterlabNotebookCodeFormatter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sql_formatter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sql-formatter */ "webpack/sharing/consume/default/sql-formatter/sql-formatter");
/* harmony import */ var sql_formatter__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sql_formatter__WEBPACK_IMPORTED_MODULE_1__);


class JupyterlabNotebookCodeFormatter {
    constructor(notebookTracker) {
        this.notebookTracker = notebookTracker;
    }
    async formatAllCodeCells(config, formatter, notebook) {
        return this.formatCells(false, config, formatter, notebook);
    }
    getCodeCells(selectedOnly = true, notebook) {
        if (!this.notebookTracker.currentWidget) {
            return [];
        }
        const codeCells = [];
        notebook = notebook || this.notebookTracker.currentWidget.content;
        notebook.widgets.forEach((cell) => {
            if (cell.model.type === 'code') {
                if (!selectedOnly || notebook.isSelectedOrActive(cell)) {
                    codeCells.push(cell);
                }
            }
        });
        return codeCells;
    }
    async formatCells(selectedOnly, config, formatter, notebook) {
        if (this.working) {
            return;
        }
        try {
            this.working = true;
            const selectedCells = this.getCodeCells(selectedOnly, notebook);
            if (selectedCells.length === 0) {
                this.working = false;
                return;
            }
            for (let i = 0; i < selectedCells.length; ++i) {
                const cell = selectedCells[i];
                const text = cell.model.value.text;
                if (text.startsWith("%%sql")) {
                    const lines = text.split("\n");
                    const sqlCommand = lines.shift();
                    try {
                        const query = (0,sql_formatter__WEBPACK_IMPORTED_MODULE_1__.format)(lines.join("\n"), { language: 'sql', keywordCase: 'upper' });
                        cell.model.value.text = sqlCommand + "\n" + query;
                    }
                    catch (error) {
                    }
                }
            }
        }
        catch (error) {
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Jupysql plugin formatting', error);
        }
        this.working = false;
    }
    applicable(formatter, currentWidget) {
        const currentNotebookWidget = this.notebookTracker.currentWidget;
        // TODO: Handle showing just the correct formatter for the language later
        return currentNotebookWidget && currentWidget === currentNotebookWidget;
    }
}


/***/ }),

/***/ "./lib/index-widgets.js":
/*!******************************!*\
  !*** ./lib/index-widgets.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   widgetExports: () => (/* binding */ widgetExports)
/* harmony export */ });
/* harmony import */ var _widgets_form__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./widgets/form */ "./lib/widgets/form.js");
/* harmony import */ var _widgets_table__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widgets/table */ "./lib/widgets/table.js");
/* harmony import */ var _widgets_connector__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widgets/connector */ "./lib/widgets/connector.js");



const widgetExports = {
    ..._widgets_form__WEBPACK_IMPORTED_MODULE_0__,
    ..._widgets_table__WEBPACK_IMPORTED_MODULE_1__,
    ..._widgets_connector__WEBPACK_IMPORTED_MODULE_2__
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FormattingExtension: () => (/* binding */ FormattingExtension),
/* harmony export */   MODULE_NAME: () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_NAME),
/* harmony export */   MODULE_VERSION: () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_VERSION),
/* harmony export */   RegisterNotebookCommListener: () => (/* binding */ RegisterNotebookCommListener),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _connector__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./connector */ "./lib/connector.js");
/* harmony import */ var _customconnector__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./customconnector */ "./lib/customconnector.js");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore");
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(underscore__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _formatter__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./formatter */ "./lib/formatter.js");
/* harmony import */ var _comm__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./comm */ "./lib/comm.js");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _index_widgets__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./index-widgets */ "./lib/index-widgets.js");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./version */ "./lib/version.js");




// for syntax highlighting









/**
 * The command IDs used by the console plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.invoke = 'completer:invoke';
    CommandIDs.invokeNotebook = 'completer:invoke-notebook';
    CommandIDs.select = 'completer:select';
    CommandIDs.selectNotebook = 'completer:select-notebook';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the extension.
 */
const extension = {
    id: 'completer',
    autoStart: true,
    requires: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: async (app, completionManager, notebooks) => {
        console.log('JupyterLab extension jupysql-plugin is activated!');
        // Modelled after completer-extension's notebooks plugin
        notebooks.widgetAdded.connect((sender, panel) => {
            var _a, _b;
            let editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
            const session = panel.sessionContext.session;
            const sessionContext = panel.sessionContext;
            const options = { session, editor, sessionContext };
            const connector = new _connector__WEBPACK_IMPORTED_MODULE_7__.CompletionConnector([]);
            const handler = completionManager.register({
                connector,
                editor,
                parent: panel,
            });
            const updateConnector = () => {
                var _a, _b;
                editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
                options.session = panel.sessionContext.session;
                options.sessionContext = panel.sessionContext;
                options.editor = editor;
                handler.editor = editor;
                const kernel = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.KernelConnector(options);
                const context = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ContextConnector(options);
                const custom = new _customconnector__WEBPACK_IMPORTED_MODULE_8__.CustomConnector(options);
                handler.connector = new _connector__WEBPACK_IMPORTED_MODULE_7__.CompletionConnector([
                    kernel,
                    context,
                    custom
                ]);
            };
            // Update the handler whenever the prompt or session changes
            panel.content.activeCellChanged.connect(updateConnector);
            panel.sessionContext.sessionChanged.connect(updateConnector);
        });
        // Add notebook completer command.
        app.commands.addCommand(CommandIDs.invokeNotebook, {
            execute: () => {
                var _a;
                const panel = notebooks.currentWidget;
                if (panel && ((_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.type) === 'code') {
                    return app.commands.execute(CommandIDs.invoke, { id: panel.id });
                }
            },
        });
        // Add notebook completer select command.
        app.commands.addCommand(CommandIDs.selectNotebook, {
            execute: () => {
                const id = notebooks.currentWidget && notebooks.currentWidget.id;
                if (id) {
                    return app.commands.execute(CommandIDs.select, { id });
                }
            },
        });
        // Set enter key for notebook completer select command.
        app.commands.addKeyBinding({
            command: CommandIDs.selectNotebook,
            keys: ['Enter'],
            selector: '.jp-Notebook .jp-mod-completer-active',
        });
    },
};
// %%sql highlighting
class SqlCodeMirror {
    constructor(app, tracker, code_mirror) {
        var _a, _b;
        this.app = app;
        this.tracker = tracker;
        this.code_mirror = code_mirror;
        (_b = (_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCellChanged) === null || _b === void 0 ? void 0 : _b.connect(() => {
            var _a;
            if (((_a = this.tracker) === null || _a === void 0 ? void 0 : _a.activeCell) !== null) {
                const cell = this.tracker.activeCell;
                if (cell !== null && (cell === null || cell === void 0 ? void 0 : cell.model.type) === 'code') {
                    const code_mirror_editor = cell === null || cell === void 0 ? void 0 : cell.editor;
                    const debounced_on_change = underscore__WEBPACK_IMPORTED_MODULE_3__.debounce(() => {
                        var _a;
                        // check for editor with first line starting with %%sql
                        const line = (_a = code_mirror_editor
                            .getLine(code_mirror_editor.firstLine())) === null || _a === void 0 ? void 0 : _a.trim();
                        if (line === null || line === void 0 ? void 0 : line.startsWith('%%sql')) {
                            code_mirror_editor.editor.setOption('mode', 'text/x-sql');
                        }
                        else {
                            code_mirror_editor.editor.setOption('mode', 'text/x-ipython');
                        }
                    }, 300);
                    code_mirror_editor.editor.on('change', debounced_on_change);
                    debounced_on_change();
                }
            }
        });
    }
}
function activate_syntax(app, tracker, code_mirror) {
    new SqlCodeMirror(app, tracker, code_mirror);
    console.log('SQLCodeMirror loaded.');
}
/**
 * Initialization data for the jupyterlabs_sql_codemirror extension.
 * this is based on:
 * https://github.com/surdouski/jupyterlabs_sql_codemirror
 */
const extension_sql = {
    id: '@ploomber/sql-syntax-highlighting',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.ICodeMirror],
    optional: [],
    activate: activate_syntax
};
/**
 * A notebook widget extension that adds a button to the toolbar.
 */
class FormattingExtension {
    constructor(tracker) {
        this.notebookCodeFormatter = new _formatter__WEBPACK_IMPORTED_MODULE_9__.JupyterlabNotebookCodeFormatter(tracker);
    }
    createNew(panel, context) {
        const clearOutput = () => {
            this.notebookCodeFormatter.formatAllCodeCells(undefined, undefined, panel.content);
        };
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.ToolbarButton({
            className: 'format-sql-button',
            label: 'Format SQL',
            onClick: clearOutput,
            tooltip: 'Format all %%sql cells',
        });
        panel.toolbar.insertItem(10, 'formatSQL', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
class RegisterNotebookCommListener {
    /**
     * Register notebook comm
     *
     * @param panel Notebook panel
     * @param context Notebook context
     * @returns Disposable on the added button
     */
    createNew(panel, context) {
        setTimeout(() => {
            (0,_comm__WEBPACK_IMPORTED_MODULE_10__.registerCommTargets)(context);
        }, 5000);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableDelegate(() => {
        });
    }
}
/**
 * Activate the extension.
 *
 * @param app Main application object
 */
const formatting_plugin = {
    activate: (app, tracker) => {
        app.docRegistry.addWidgetExtension('Notebook', new FormattingExtension(tracker));
        app.docRegistry.addWidgetExtension('Notebook', new RegisterNotebookCommListener());
    },
    autoStart: true,
    id: "formatting",
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker,
    ]
};
const EXTENSION_ID = 'jupysql-plugin:plugin';
/**
 * The example plugin.
 */
const examplePlugin = {
    id: EXTENSION_ID,
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_6__.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true,
};
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_NAME,
        version: _version__WEBPACK_IMPORTED_MODULE_11__.MODULE_VERSION,
        exports: _index_widgets__WEBPACK_IMPORTED_MODULE_12__.widgetExports,
    });
}

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([extension, extension_sql, formatting_plugin, examplePlugin]);


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MODULE_NAME: () => (/* binding */ MODULE_NAME),
/* harmony export */   MODULE_VERSION: () => (/* binding */ MODULE_VERSION)
/* harmony export */ });
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
const MODULE_VERSION = data.version;
/*
 * The current package name.
 */
const MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widgets/connector.js":
/*!**********************************!*\
  !*** ./lib/widgets/connector.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ConnectorModel: () => (/* binding */ ConnectorModel),
/* harmony export */   ConnectorView: () => (/* binding */ ConnectorView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../version */ "./lib/version.js");
/* harmony import */ var _style_connector_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/connector.css */ "./style/connector.css");


// Import the CSS

class ConnectorModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: ConnectorModel.model_name,
            _model_module: ConnectorModel.model_module,
            _model_module_version: ConnectorModel.model_module_version,
            _view_name: ConnectorModel.view_name,
            _view_module: ConnectorModel.view_module,
            _view_module_version: ConnectorModel.view_module_version,
            connections: ConnectorModel.connections,
            connections_templates: ConnectorModel.connections_templates
        };
    }
}
ConnectorModel.serializers = {
    ..._jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel.serializers,
};
ConnectorModel.model_name = 'ConnectorModel';
ConnectorModel.model_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME;
ConnectorModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
ConnectorModel.view_name = 'ConnectorModel'; // Set to null if no view
ConnectorModel.view_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME; // Set to null if no view
ConnectorModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
ConnectorModel.connections = [];
ConnectorModel.connections_templates = [];
class ConnectorView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetView {
    constructor() {
        super(...arguments);
        // availble connections
        this.connections = JSON.parse(this.model.get('connections'));
        // connections templates for creating a new connection
        this.connectionsTemplates = JSON.parse(this.model.get('connections_templates'));
        this.activeConnection = "";
    }
    render() {
        this.el.classList.add('connector-widget');
        this.drawConnectorUI(this.connections);
        // Listen for messages from the Python backend
        this.model.on('msg:custom', this.handleMessage.bind(this));
    }
    /**
     * Draws the connection UI
     *
     * @param connection : The availble connections
     */
    drawConnectorUI(connections) {
        this.el.innerHTML = "";
        const template = `
        <div id="connectionsManager">
            <div id="connectionsContainer" class="block">
                <h3>
                    Connections
                </h3>

                <div class="connections-guidelines block">
                    <i>
                        * Connections are loaded from connections.ini file
                    </i>

                    <i class="no-config-file" style = "display: none;">
                        * No connections.ini file found. You may need to restart the kernel.
                    </i>

                    <i class="restart-kernel" style = "display: none;">
                        * No connections found in connections.ini file. You may need to restart the kernel.
                    </i>                    
                </div>

                <div id="connectionsButtonsContainer" class="block">
                </div>

                <div class="block">
                    <div class="create-new-connection" id="createNewConnectionButton">
                        <div class="icon"></div>
                        <div>
                            Create new connection
                        </div>
                    </div>
                </div>
         
            </div>

            <div class="user-error-message lm-Widget p-Widget lm-Panel p-Panel jp-OutputArea-child" style = "display: none">
            <div class="lm-Widget jp-RenderedText" data-mime-type="application/vnd.jupyter.stderr">
            <pre></pre>
            </div>
            </div>


            <div id="newConnectionContainer" class="block" style = "display: none">
                <h3>Create new connection</h3>
                <div class="block">
                    <select id="selectConnection"></select>

                    <div id="connectionFormContainer">
                    </div>
                </div>
            </div>
        </div>
        `;
        this.el.innerHTML = template;
        // Draw connection buttons
        connections.forEach((connection) => {
            const { name } = connection;
            const name_without_spaces = name.replace(/ /g, "_");
            const buttonContainer = document.createElement("DIV");
            buttonContainer.className = "connection-button-container";
            const actionsContainer = document.createElement("DIV");
            actionsContainer.className = "connection-button-actions";
            const connectionName = document.createElement("DIV");
            connectionName.className = "connection-name";
            connectionName.innerText = name;
            actionsContainer.appendChild(connectionName);
            const connectButton = document.createElement("BUTTON");
            connectButton.id = `connBtn_${name_without_spaces}`;
            connectButton.className = "secondary";
            connectButton.innerHTML = "Connect";
            connectButton.onclick = this.handleConnectionClick.bind(this, connection);
            const deleteConnection = document.createElement("BUTTON");
            deleteConnection.className = `delete-connection-button`;
            deleteConnection.id = `deleteConnBtn_${name_without_spaces}`;
            deleteConnection.onclick = this.handleDeleteConnectionClick.bind(this, connection);
            let connectionsButtonsContainer = this.el.querySelector('#connectionsButtonsContainer');
            actionsContainer.appendChild(connectButton);
            actionsContainer.appendChild(deleteConnection);
            buttonContainer.appendChild(actionsContainer);
            connectionsButtonsContainer.appendChild(buttonContainer);
            let divider = document.createElement("HR");
            divider.className = "divider";
            buttonContainer.appendChild(divider);
        });
        // Draw new connection select
        const select = this.el.querySelector("#selectConnection");
        Object.keys(this.connectionsTemplates).forEach(key => {
            const option = document.createElement("OPTION");
            option.setAttribute("value", key);
            option.innerHTML = key;
            select.appendChild(option);
        });
        select.addEventListener("change", this.handleCreateNewConnectionChange.bind(this));
        const newConnectionButton = this.el.querySelector("#createNewConnectionButton");
        newConnectionButton.addEventListener("click", this.handleCreateNewConnectionClick.bind(this));
        if (this.activeConnection) {
            this.markConnectedButton(this.activeConnection);
        }
        setTimeout(() => {
            const message = {
                method: 'check_config_file'
            };
            this.send(message);
        }, 500);
    }
    /**
     * Connects to a database
     *
     * @param connection - connection object
     */
    handleConnectionClick(connection) {
        const message = {
            method: 'connect',
            data: connection
        };
        this.send(message);
    }
    deleteConnection(connection) {
        const message = {
            method: 'delete_connection',
            data: connection
        };
        this.send(message);
    }
    handleDeleteConnectionClick(connection) {
        this.hideDeleteMessageApproval();
        // create new message
        const deleteConnectionMessage = document.createElement("DIV");
        deleteConnectionMessage.id = "deleteConnectionMessage";
        // const warningMessage = `<h4>Delete connection from ini file</h4>
        // <div>Are you sure you want to delete <strong>${connection["name"]}</strong>?<div> 
        // <div>Please note that by doing so, you will permanently remove <strong>${connection["name"]}</strong> from the ini file.<div>`
        const warningMessage = `<h4>Delete ${connection["name"]} from ini file</h4>
        <div>Please note that by doing so, you will permanently remove <strong>${connection["name"]}</strong> from the ini file.<div>
        <div>Are you sure?</div>
        `;
        deleteConnectionMessage.innerHTML = `${warningMessage} <div class='actions' style = 'margin-top: 20px; display: inline-flex'></div>`;
        const cancelButton = document.createElement("BUTTON");
        cancelButton.innerHTML = "Cancel";
        cancelButton.addEventListener("click", this.hideDeleteMessageApproval.bind(this));
        deleteConnectionMessage.querySelector(".actions").appendChild(cancelButton);
        const approveButton = document.createElement("BUTTON");
        approveButton.innerHTML = "Delete";
        approveButton.className = "danger";
        approveButton.addEventListener("click", this.deleteConnection.bind(this, connection));
        deleteConnectionMessage.querySelector(".actions").appendChild(approveButton);
        // hide controllers
        const deleteConnBtn = this.el.querySelector(`#deleteConnBtn_${connection["name"].replace(/ /g, "_")}`);
        const actionsContainer = deleteConnBtn.parentNode;
        actionsContainer.style.display = "none";
        // show buttons
        const buttonsContainer = actionsContainer.parentNode;
        buttonsContainer.prepend(deleteConnectionMessage);
    }
    hideDeleteMessageApproval() {
        var _a;
        (_a = this.el.querySelector("#deleteConnectionMessage")) === null || _a === void 0 ? void 0 : _a.remove();
        this.el.querySelectorAll(".connection-button-actions")
            .forEach(c => c.style.display = "inline-flex");
    }
    /**
     * Handle create new connection click
     */
    handleCreateNewConnectionClick() {
        // hide connectionsContainer
        this.el.querySelector("#connectionsContainer").style.display = "none";
        // show newConnectionContainer
        this.el.querySelector("#newConnectionContainer").style.display = "block";
        // select first value
        this.handleCreateNewConnectionChange();
    }
    /**
     * Handle select new connection
     */
    handleCreateNewConnectionChange() {
        const select = this.el.querySelector("#selectConnection");
        const key = select.value;
        const connectionTemplate = this.connectionsTemplates[key];
        this.drawNewConnectionForm(connectionTemplate);
    }
    /**
     * Draws a form to create a new connection
     *
     * @param connectionTemplate - new connection template
     */
    drawNewConnectionForm(connectionTemplate) {
        const { fields } = connectionTemplate;
        const connectionFormContainer = this.el.querySelector("#connectionFormContainer");
        connectionFormContainer.innerHTML = "";
        const connectionForm = document.createElement("FORM");
        connectionForm.id = "connectionForm";
        connectionFormContainer.appendChild(connectionForm);
        fields.forEach(field => {
            const fieldContainer = document.createElement("DIV");
            fieldContainer.className = "field-container";
            const label = document.createElement("LABEL");
            label.setAttribute("for", field.id);
            label.innerHTML = field.label;
            const input = document.createElement("INPUT");
            input.id = field.id;
            input.name = field.id;
            input.className = "field";
            input.setAttribute("type", field.type);
            fieldContainer.appendChild(label);
            fieldContainer.appendChild(input);
            connectionForm.appendChild(fieldContainer);
        });
        const buttonsContainer = document.createElement("DIV");
        buttonsContainer.className = "buttons-container";
        // cancel button
        const cancelButton = document.createElement("BUTTON");
        cancelButton.innerHTML = "Cancel";
        cancelButton.className = "secondary";
        cancelButton.addEventListener("click", this.drawConnectorUI.bind(this, this.connections));
        buttonsContainer.appendChild(cancelButton);
        // submit form button
        const submitButton = document.createElement("BUTTON");
        submitButton.className = "primary";
        submitButton.innerHTML = "Create";
        connectionForm.addEventListener("submit", this.handleSubmitNewConnection.bind(this));
        buttonsContainer.appendChild(submitButton);
        connectionForm.appendChild(buttonsContainer);
    }
    /**
     * Submits new connection form
     *
     * @param event - Submit event
     */
    handleSubmitNewConnection(event) {
        event.preventDefault();
        let allFieldsFilled = true;
        // Extract form data
        const form = event.target;
        const formData = new FormData(form);
        // Convert form data to a plain object
        const formValues = {};
        for (const [key, value] of formData.entries()) {
            const _value = value.toString();
            formValues[key] = _value;
            if (_value.length === 0) {
                allFieldsFilled = false;
            }
        }
        const select = this.el.querySelector("#selectConnection");
        const driver = this.connectionsTemplates[select.value].driver;
        formValues["driver"] = driver;
        // todo: validate all inputs are filled
        if (allFieldsFilled) {
            this.sendFormData(formValues);
        }
        else {
            this.showErrorMessage("Error : Please fill in all fields.");
        }
    }
    /**
     * Sends form data to the backend
     *
     * @param formData - FormData object
     */
    sendFormData(formData) {
        // Create a message to send to the Python backend
        const message = {
            method: 'submit_new_connection',
            data: formData
        };
        // Send the message to the Python backend
        this.send(message);
    }
    /**
     * Handle messages from the backend
     *
     * @param content - The method to invoke with data
     */
    handleMessage(content) {
        if (content.method === "update_connections") {
            this.connections = JSON.parse(content.message);
            this.drawConnectorUI(this.connections);
        }
        if (content.method === "connected") {
            const connectionName = content.message;
            this.activeConnection = connectionName;
            this.markConnectedButton(connectionName);
        }
        if (content.method === "connection_name_exists_error") {
            const connectionName = content.message;
            const error = `${connectionName} is already exists`;
            this.showErrorMessage(error);
        }
        if (content.method === "connection_error") {
            const error = content.message;
            this.showErrorMessage(error);
        }
        if (content.method === "check_config_file") {
            const isExist = content.message;
            const i = this.el.querySelector(".connections-guidelines .no-config-file");
            if (isExist) {
                i.style.display = "none";
                const iKernelMessage = this.el.querySelector(".connections-guidelines .no-config-file");
                iKernelMessage.style.display = (this.connections.length === 0) ? "block" : "none";
            }
            else {
                i.style.display = "block";
            }
        }
    }
    /**
     * Marks active connection button
     *
     * @param connectionName - Active connection name
     */
    markConnectedButton(connectionName) {
        this.el.querySelectorAll(`.connection-button-actions button:not(.delete-connection-button)`)
            .forEach((button) => {
            const buttonEl = button;
            buttonEl.innerHTML = "Connect";
            buttonEl.classList.remove("primary");
            buttonEl.classList.add("secondary");
        });
        const selectedButtonEl = this.el.querySelector(`#connBtn_${connectionName.replace(/ /g, "_")}`);
        selectedButtonEl.innerText = "Connected";
        selectedButtonEl.classList.add("primary");
    }
    showErrorMessage(error) {
        const errorEl = this.el.querySelector(".user-error-message");
        const errorMessageContainer = errorEl.querySelector("pre");
        errorMessageContainer.innerHTML = `${error}`;
        errorEl.style.display = "block";
    }
}


/***/ }),

/***/ "./lib/widgets/form.js":
/*!*****************************!*\
  !*** ./lib/widgets/form.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FormModel: () => (/* binding */ FormModel),
/* harmony export */   FormView: () => (/* binding */ FormView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../version */ "./lib/version.js");
/* harmony import */ var _style_widget_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/widget.css */ "./style/widget.css");
// Form widget. Python backend is implemented in FormWidget


// Import the CSS

class FormModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: FormModel.model_name,
            _model_module: FormModel.model_module,
            _model_module_version: FormModel.model_module_version,
            _view_name: FormModel.view_name,
            _view_module: FormModel.view_module,
            _view_module_version: FormModel.view_module_version,
            value: 'Hello World',
        };
    }
}
FormModel.serializers = {
    ..._jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel.serializers,
};
FormModel.model_name = 'FormModel';
FormModel.model_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME;
FormModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
FormModel.view_name = 'FormView'; // Set to null if no view
FormModel.view_module = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME; // Set to null if no view
FormModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION;
class FormView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        const template = `
        <form id="myForm">
        <label for="protocol">Select a protocol:</label>
        <select id="protocol" name="protocol">
          <option value="HTTP">HTTP</option>
          <option value="HTTPS">HTTPS</option>
        </select>
      
        <label for="port">Enter a port:</label>
        <input type="number" id="port" name="port">

        <div id="confirmationMessage"></div>
      
        <button type="submit">Submit</button>
      </form>
      
`;
        this.el.innerHTML = template;
        // Add event listener for form submission
        const form = this.el.querySelector('#myForm');
        form.addEventListener('submit', this.handleFormSubmit.bind(this));
        // Listen for messages from the Python backend
        this.model.on('msg:custom', this.handleMessage.bind(this));
    }
    handleFormSubmit(event) {
        event.preventDefault();
        // Extract form data
        const form = event.target;
        const formData = new FormData(form);
        // Convert form data to a plain object
        const formValues = {};
        for (const [key, value] of formData.entries()) {
            formValues[key] = value.toString();
        }
        // Call the function to send form data to the Python backend
        this.sendFormData(formValues);
    }
    sendFormData(formData) {
        // Create a message to send to the Python backend
        const message = {
            method: 'submit_form',
            data: formData
        };
        // Send the message to the Python backend
        this.send(message);
    }
    handleMessage(content) {
        if (content.method === 'display_confirmation_message') {
            const confirmationMessage = this.el.querySelector('#confirmationMessage');
            if (confirmationMessage) {
                confirmationMessage.textContent = content.message;
            }
        }
    }
}


/***/ }),

/***/ "./lib/widgets/table.js":
/*!******************************!*\
  !*** ./lib/widgets/table.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TableModel: () => (/* binding */ TableModel),
/* harmony export */   TableView: () => (/* binding */ TableView)
/* harmony export */ });
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../version */ "./lib/version.js");
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! bootstrap */ "webpack/sharing/consume/default/bootstrap/bootstrap");
/* harmony import */ var bootstrap__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(bootstrap__WEBPACK_IMPORTED_MODULE_2__);
// Table widget. Python backend is implemented in TableWidget




class TableModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: TableModel.model_name,
            _model_module: TableModel.model_module,
            _model_module_version: TableModel.model_module_version,
            _view_name: TableModel.view_name,
            _view_module: TableModel.view_module,
            _view_module_version: TableModel.view_module_version,
            value: 'Hello World',
        };
    }
}
TableModel.serializers = {
    ..._jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetModel.serializers,
};
TableModel.model_name = 'TableModel';
TableModel.model_module = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_NAME;
TableModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_VERSION;
TableModel.view_name = 'TableView'; // Set to null if no view
TableModel.view_module = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_NAME; // Set to null if no view
TableModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_3__.MODULE_VERSION;
class TableView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetView {
    render() {
        const stockData = [
            { symbol: 'AAPL', price: 142.34, change: 1.25 },
            { symbol: 'GOOGL', price: 2725.45, change: -4.56 },
            { symbol: 'MSFT', price: 259.43, change: 2.78 },
            { symbol: 'AMZN', price: 3310.98, change: -7.92 },
        ];
        this.el.innerHTML = `
      <table class="table">
        <thead>
          <tr>
            <th data-bs-toggle="tooltip" data-bs-placement="top" title="symbol">Symbol</th>
            <th data-bs-toggle="tooltip" data-bs-placement="top" title="price">Price</th>
            <th data-bs-toggle="tooltip" data-bs-placement="top" title="change">Change</th>
          </tr>
        </thead>
        <tbody>
          ${stockData.map((stock) => `
            <tr>
              <td>${stock.symbol}</td>
              <td>${stock.price}</td>
              <td>${stock.change}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
        const tooltipTriggerList = Array.from(this.el.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach((tooltipTriggerEl) => {
            const column = tooltipTriggerEl.getAttribute('title');
            const tooltipContent = stockData.map((stock) => stock[column]).join(', ');
            new bootstrap__WEBPACK_IMPORTED_MODULE_2__.Tooltip(tooltipTriggerEl, {
                title: tooltipContent,
            });
        });
    }
}


/***/ }),

/***/ "./style/connector.css":
/*!*****************************!*\
  !*** ./style/connector.css ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_connector_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./connector.css */ "./node_modules/css-loader/dist/cjs.js!./style/connector.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_connector_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_connector_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./style/widget.css":
/*!**************************!*\
  !*** ./style/widget.css ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./style/widget.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./style/icons/add_primary.svg":
/*!*************************************!*\
  !*** ./style/icons/add_primary.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3Csvg width='14' height='14' viewBox='0 0 14 14' fill='none' xmlns='http://www.w3.org/2000/svg'%3E %3Cpath d='M14 8H8V14H6V8H0V6H6V0H8V6H14V8Z' fill='%23206EEF'/%3E %3C/svg%3E"

/***/ }),

/***/ "./style/icons/delete_outline_black.svg":
/*!**********************************************!*\
  !*** ./style/icons/delete_outline_black.svg ***!
  \**********************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='24px' viewBox='0 0 24 24' width='24px' fill='%23000000'%3E%3Cpath d='M0 0h24v24H0V0z' fill='none'/%3E%3Cpath d='M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9zm7.5-5l-1-1h-5l-1 1H5v2h14V4z'/%3E%3C/svg%3E"

/***/ }),

/***/ "./lib/keywords.json":
/*!***************************!*\
  !*** ./lib/keywords.json ***!
  \***************************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"keywords":[{"value":"ADD"},{"value":"ADD CONSTRAINT"},{"value":"ALL"},{"value":"ALTER"},{"value":"ALTER COLUMN"},{"value":"ALTER TABLE"},{"value":"AND"},{"value":"ANY"},{"value":"AS"},{"value":"ASC"},{"value":"BACKUP DATABASE"},{"value":"BETWEEN"},{"value":"CASE"},{"value":"CHECK"},{"value":"COLUMN"},{"value":"CONSTRAINT"},{"value":"CREATE"},{"value":"CREATE DATABASE"},{"value":"CREATE INDEX"},{"value":"CREATE OR REPLACE VIEW"},{"value":"CREATE TABLE"},{"value":"CREATE PROCEDURE"},{"value":"CREATE UNIQUE INDEX"},{"value":"CREATE VIEW"},{"value":"DATABASE"},{"value":"DEFAULT"},{"value":"DELETE"},{"value":"DESC"},{"value":"DISTINCT"},{"value":"DROP"},{"value":"DROP COLUMN"},{"value":"DROP CONSTRAINT"},{"value":"DROP DATABASE"},{"value":"DROP DEFAULT"},{"value":"DROP INDEX"},{"value":"DROP TABLE"},{"value":"DROP VIEW"},{"value":"EXEC"},{"value":"EXISTS"},{"value":"FOREIGN KEY"},{"value":"FROM"},{"value":"FULL OUTER JOIN"},{"value":"GROUP BY"},{"value":"HAVING"},{"value":"IN"},{"value":"INDEX"},{"value":"INNER JOIN"},{"value":"INSERT INTO"},{"value":"INSERT INTO SELECT"},{"value":"IS NULL"},{"value":"IS NOT NULL"},{"value":"JOIN"},{"value":"LEFT JOIN"},{"value":"LIKE"},{"value":"LIMIT"},{"value":"NOT"},{"value":"NOT NULL"},{"value":"OR"},{"value":"ORDER BY"},{"value":"OUTER JOIN"},{"value":"PRIMARY KEY"},{"value":"PROCEDURE"},{"value":"RIGHT JOIN"},{"value":"ROWNUM"},{"value":"SELECT"},{"value":"SELECT DISTINCT"},{"value":"SELECT INTO"},{"value":"SELECT TOP"},{"value":"SET"},{"value":"TABLE"},{"value":"TOP"},{"value":"TRUNCATE TABLE"},{"value":"UNION"},{"value":"UNION ALL"},{"value":"UNIQUE"},{"value":"UPDATE"},{"value":"VALUES"},{"value":"VIEW"},{"value":"WHERE"}]}');

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"jupysql-plugin","version":"0.1.4","description":"Jupyterlab extension for JupySQL","private":true,"keywords":["jupyter","jupyterlab","jupyterlab-extension"],"homepage":"https://github.com/ploomber/jupysql-plugin.git","bugs":{"url":"https://github.com/ploomber/jupysql-plugin.git/issues"},"license":"BSD-3-Clause","author":{"name":"Ploomber","email":"contact@ploomber.io"},"files":["lib/**/*.{d.ts,eot,gif,html,jpg,js,js.map,json,png,svg,woff2,ttf}","style/**/*.{css,js,eot,gif,html,jpg,json,png,svg,woff2,ttf}"],"main":"lib/index.js","types":"lib/index.d.ts","style":"style/index.css","repository":{"type":"git","url":"https://github.com/ploomber/jupysql-plugin.git.git"},"workspaces":{"packages":["jupysql_plugin","ui-tests"]},"scripts":{"build":"jlpm build:lib && jlpm build:labextension:dev","build:prod":"jlpm clean && jlpm build:lib:prod && jlpm build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc --sourceMap","build:lib:prod":"tsc","clean":"jlpm clean:lib","clean:lib":"rimraf lib tsconfig.tsbuildinfo","clean:lintcache":"rimraf .eslintcache .stylelintcache","clean:labextension":"rimraf jupysql_plugin/labextension jupysql_plugin/_version.py","clean:all":"jlpm clean:lib && jlpm clean:labextension && jlpm clean:lintcache","eslint":"jlpm eslint:check --fix","eslint:check":"eslint . --cache --ext .ts,.tsx","install:extension":"jlpm build","lint":"jlpm stylelint && jlpm prettier && jlpm eslint","lint:check":"jlpm stylelint:check && jlpm prettier:check && jlpm eslint:check","prettier":"jlpm prettier:base --write --list-different","prettier:base":"prettier \\"**/*{.ts,.tsx,.js,.jsx,.css,.json,.md}\\"","prettier:check":"jlpm prettier:base --check","stylelint":"jlpm stylelint:check --fix","stylelint:check":"stylelint --cache \\"style/**/*.css\\"","test":"jest --coverage","watch":"run-p watch:src watch:labextension","watch:src":"tsc -w","watch:labextension":"jupyter labextension watch ."},"@comment":{"dependencies":{"@lumino/widgets":"An official library to implement the frontend of the widgets: https://github.com/jupyterlab/lumino"}},"dependencies":{"@jupyter-widgets/base":"^6.0.4","@jupyterlab/application":"^3.6.2","@jupyterlab/codeeditor":"^3.6.2","@jupyterlab/codemirror":"^3.6.3","@jupyterlab/completer":"^3.6.2","@jupyterlab/notebook":"^3.6.2","@jupyterlab/statedb":"^3.6.2","@lumino/widgets":"<2.0.0","@types/codemirror":"^5.60.7","@types/underscore":"^1.11.4","bootstrap":"^5.2.3","sql-formatter":"^12.2.0","underscore":"^1.13.6"},"devDependencies":{"@babel/core":"^7.0.0","@babel/preset-env":"^7.0.0","@jupyterlab/builder":"^3.1.0","@jupyterlab/testutils":"^3.0.0","@types/bootstrap":"^5.2.6","@types/jest":"^26.0.0","@typescript-eslint/eslint-plugin":"^4.8.1","@typescript-eslint/parser":"^4.8.1","eslint":"^7.14.0","eslint-config-prettier":"^6.15.0","eslint-plugin-prettier":"^3.1.4","jest":"^26.0.0","npm-run-all":"^4.1.5","prettier":"^2.1.1","rimraf":"^3.0.2","stylelint":"^14.3.0","stylelint-config-prettier":"^9.0.4","stylelint-config-recommended":"^6.0.0","stylelint-config-standard":"~24.0.0","stylelint-prettier":"^2.0.0","ts-jest":"^26.0.0","typescript":"~4.1.3"},"sideEffects":["style/*.css","style/index.js"],"styleModule":"style/index.js","publishConfig":{"access":"public"},"jupyterlab":{"extension":true,"outputDir":"jupysql_plugin/labextension","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.f2f7fb5f90f53f96899d.js.map