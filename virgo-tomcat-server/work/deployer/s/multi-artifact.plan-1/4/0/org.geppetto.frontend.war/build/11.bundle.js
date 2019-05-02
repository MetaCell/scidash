webpackJsonp([11],{

/***/ 1049:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    __webpack_require__(2803);\n\n    var React = __webpack_require__(1);\n\n    var SpotlightButton = __webpack_require__(2805);\n    var ControlPanelButton = __webpack_require__(2806);\n    var QueryBuilderButton = __webpack_require__(2807);\n    var TutorialButton = __webpack_require__(2808);\n\n    var GEPPETTO = __webpack_require__(132);\n\n    var ForegroundControls = React.createClass({\n        displayName: 'ForegroundControls',\n\n\n        getInitialState: function getInitialState() {\n            return {\n                disableSpotlight: false,\n                showDropDown: false\n            };\n        },\n\n        componentDidMount: function componentDidMount() {},\n\n        componentWillMount: function componentWillMount() {\n            GEPPETTO.ForegroundControls = this;\n        },\n\n        refresh: function refresh() {\n            this.forceUpdate();\n        },\n\n        render: function render() {\n            var spotlightBtn = GEPPETTO.Spotlight != undefined ? React.createFactory(SpotlightButton)({ disabled: this.state.disableSpotlight }) : '';\n            var controlPanelBtn = GEPPETTO.ControlPanel != undefined ? React.createFactory(ControlPanelButton)({}) : '';\n\n            var queryBuilderBtn = GEPPETTO.QueryBuilder != undefined ? React.createFactory(QueryBuilderButton)({}) : '';\n\n            var tutorialBtn = GEPPETTO.Tutorial != undefined ? React.createFactory(TutorialButton)({}) : '';\n\n            return React.createElement(\n                'div',\n                { className: 'foreground-controls' },\n                controlPanelBtn,\n                React.createElement('br', null),\n                spotlightBtn,\n                queryBuilderBtn == \"\" ? '' : React.createElement('br', null),\n                queryBuilderBtn,\n                React.createElement('br', null),\n                tutorialBtn\n            );\n        }\n    });\n\n    return ForegroundControls;\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/foregroundControls/ForegroundControls.js\n// module id = 1049\n// module chunks = 11\n\n//# sourceURL=webpack:///./js/components/interface/foregroundControls/ForegroundControls.js?");

/***/ }),

/***/ 1131:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n    /**\n     * Button used as part of GEPPETTO Components\n     *\n     * @mixin Button\n     */\n    var React = __webpack_require__(1);\n\n    return {\n        displayName: 'Button',\n\n        render: function render() {\n            return React.DOM.button({\n                type: 'button',\n                id: this.props.id,\n                className: 'btn ' + this.props.className + (this.props.hidden === true ? ' hiddenElement' : ''),\n                'data-toggle': this.props['data-toggle'],\n                onClick: this.props.onClick,\n                disabled: this.props.disabled,\n                icon: this.props.icon\n            }, React.DOM.i({ className: this.props.icon }), \" \" + this.props.label);\n        }\n    };\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/controls/mixins/Button.js\n// module id = 1131\n// module chunks = 8 11 24\n\n//# sourceURL=webpack:///./js/components/controls/mixins/Button.js?");

/***/ }),

/***/ 2803:
/***/ (function(module, exports, __webpack_require__) {

eval("// style-loader: Adds some css to the DOM by adding a <style> tag\n\n// load the styles\nvar content = __webpack_require__(2804);\nif(typeof content === 'string') content = [[module.i, content, '']];\n// add the styles to the DOM\nvar update = __webpack_require__(25)(content, {});\nif(content.locals) module.exports = content.locals;\n// Hot Module Replacement\nif(false) {\n\t// When the styles change, update the <style> tags\n\tif(!content.locals) {\n\t\tmodule.hot.accept(\"!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\\\"modifyVars\\\":{\\\"url\\\":\\\"'../../../extensions/geppetto-default/colors'\\\"}}!./ForegroundControls.less\", function() {\n\t\t\tvar newContent = require(\"!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\\\"modifyVars\\\":{\\\"url\\\":\\\"'../../../extensions/geppetto-default/colors'\\\"}}!./ForegroundControls.less\");\n\t\t\tif(typeof newContent === 'string') newContent = [[module.id, newContent, '']];\n\t\t\tupdate(newContent);\n\t\t});\n\t}\n\t// When the module is disposed, remove the <style> tags\n\tmodule.hot.dispose(function() { update(); });\n}\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/foregroundControls/ForegroundControls.less\n// module id = 2803\n// module chunks = 11\n\n//# sourceURL=webpack:///./js/components/interface/foregroundControls/ForegroundControls.less?");

/***/ }),

/***/ 2804:
/***/ (function(module, exports, __webpack_require__) {

eval("exports = module.exports = __webpack_require__(24)(undefined);\n// imports\n\n\n// module\nexports.push([module.i, \"#foreground-toolbar {\\n  position: fixed;\\n  left: 52px;\\n  top: 320px;\\n}\\n.foreground-controls button {\\n  border: none;\\n  width: 24px;\\n  height: 24px;\\n  padding: 1px;\\n  margin-bottom: 4px;\\n}\\n\", \"\"]);\n\n// exports\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./node_modules/css-loader!./node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-default/colors'\"}}!./js/components/interface/foregroundControls/ForegroundControls.less\n// module id = 2804\n// module chunks = 11\n\n//# sourceURL=webpack:///./js/components/interface/foregroundControls/ForegroundControls.less?./node_modules/css-loader!./node_modules/less-loader/dist/cjs.js?%7B%22modifyVars%22:%7B%22url%22:%22'../../../extensions/geppetto-default/colors'%22%7D%7D");

/***/ }),

/***/ 2805:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    var React = __webpack_require__(1),\n        GEPPETTO = __webpack_require__(132);\n\n    return React.createClass({\n        mixins: [__webpack_require__(1131)],\n\n        componentDidMount: function componentDidMount() {},\n\n        getDefaultProps: function getDefaultProps() {\n            return {\n                label: '',\n                id: 'spotlightBtn',\n                className: 'squareB',\n                icon: 'fa fa-search',\n                onClick: function onClick() {\n                    if (GEPPETTO.Spotlight != undefined) {\n                        GEPPETTO.trigger('spin_logo');\n                        GEPPETTO.Spotlight.open(GEPPETTO.Resources.SEARCH_FLOW);\n                        GEPPETTO.trigger('stop_spin_logo');\n                    }\n                }\n            };\n        }\n\n    });\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/foregroundControls/buttons/SpotlightButton.js\n// module id = 2805\n// module chunks = 11\n\n//# sourceURL=webpack:///./js/components/interface/foregroundControls/buttons/SpotlightButton.js?");

/***/ }),

/***/ 2806:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    var React = __webpack_require__(1),\n        GEPPETTO = __webpack_require__(132);\n\n    return React.createClass({\n        mixins: [__webpack_require__(1131)],\n\n        componentDidMount: function componentDidMount() {},\n\n        getDefaultProps: function getDefaultProps() {\n            return {\n                label: '',\n                id: 'controlPanelBtn',\n                className: 'squareB',\n                icon: 'fa fa-list',\n                onClick: function onClick() {\n                    GEPPETTO.ControlPanel.open();\n                }\n            };\n        }\n\n    });\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/foregroundControls/buttons/ControlPanelButton.js\n// module id = 2806\n// module chunks = 11\n\n//# sourceURL=webpack:///./js/components/interface/foregroundControls/buttons/ControlPanelButton.js?");

/***/ }),

/***/ 2807:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    var React = __webpack_require__(1),\n        GEPPETTO = __webpack_require__(132);\n\n    return React.createClass({\n        mixins: [__webpack_require__(1131)],\n\n        componentDidMount: function componentDidMount() {},\n\n        getDefaultProps: function getDefaultProps() {\n            return {\n                label: '',\n                id: 'queryBuilderBtn',\n                className: 'squareB',\n                icon: 'fa fa-cogs',\n                onClick: function onClick() {\n                    GEPPETTO.QueryBuilder.open();\n                }\n            };\n        }\n\n    });\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/foregroundControls/buttons/QueryBuilderButton.js\n// module id = 2807\n// module chunks = 11\n\n//# sourceURL=webpack:///./js/components/interface/foregroundControls/buttons/QueryBuilderButton.js?");

/***/ }),

/***/ 2808:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    var React = __webpack_require__(1),\n        GEPPETTO = __webpack_require__(132);\n\n    return React.createClass({\n        mixins: [__webpack_require__(1131)],\n\n        componentDidMount: function componentDidMount() {},\n\n        getDefaultProps: function getDefaultProps() {\n            return {\n                label: '',\n                id: 'tutorialBtn',\n                className: 'squareB',\n                icon: 'fa fa-leanpub',\n                onClick: function onClick() {\n                    GEPPETTO.CommandController.execute(\"G.toggleTutorial()\", true);\n                }\n            };\n        }\n    });\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/foregroundControls/buttons/TutorialButton.js\n// module id = 2808\n// module chunks = 11\n\n//# sourceURL=webpack:///./js/components/interface/foregroundControls/buttons/TutorialButton.js?");

/***/ })

});