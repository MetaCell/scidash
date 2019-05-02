webpackJsonp([18],{

/***/ 1045:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n\n    __webpack_require__(2796);\n\n    var React = __webpack_require__(1);\n    var GEPPETTO = __webpack_require__(132);\n\n    var logoDiv = React.createClass({\n        displayName: 'logoDiv',\n\n        componentDidMount: function componentDidMount() {\n            GEPPETTO.on('spin_logo', function (label) {\n                //TODO Fix this to use state instead and not touching the dom element with jQuery\n                $(\"#geppettologo\").addClass(\"fa-spin\").attr('title', 'Loading data');\n            }.bind($(\".\" + this.props.logo)));\n\n            GEPPETTO.on('stop_spin_logo', function (label) {\n                $(\"#geppettologo\").removeClass(\"fa-spin\").attr('title', '');\n            }.bind($(\".\" + this.props.logo)));\n        },\n\n        render: function render() {\n            return React.createElement('div', { id: this.props.id, className: this.props.logo, style: this.props.propStyle });\n        }\n    });\n\n    return logoDiv;\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/logo/Logo.js\n// module id = 1045\n// module chunks = 18\n\n//# sourceURL=webpack:///./js/components/interface/logo/Logo.js?");

/***/ }),

/***/ 2796:
/***/ (function(module, exports, __webpack_require__) {

eval("// style-loader: Adds some css to the DOM by adding a <style> tag\n\n// load the styles\nvar content = __webpack_require__(2797);\nif(typeof content === 'string') content = [[module.i, content, '']];\n// add the styles to the DOM\nvar update = __webpack_require__(25)(content, {});\nif(content.locals) module.exports = content.locals;\n// Hot Module Replacement\nif(false) {\n\t// When the styles change, update the <style> tags\n\tif(!content.locals) {\n\t\tmodule.hot.accept(\"!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\\\"modifyVars\\\":{\\\"url\\\":\\\"'../../../extensions/geppetto-default/colors'\\\"}}!./Logo.less\", function() {\n\t\t\tvar newContent = require(\"!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\\\"modifyVars\\\":{\\\"url\\\":\\\"'../../../extensions/geppetto-default/colors'\\\"}}!./Logo.less\");\n\t\t\tif(typeof newContent === 'string') newContent = [[module.id, newContent, '']];\n\t\t\tupdate(newContent);\n\t\t});\n\t}\n\t// When the module is disposed, remove the <style> tags\n\tmodule.hot.dispose(function() { update(); });\n}\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/logo/Logo.less\n// module id = 2796\n// module chunks = 18\n\n//# sourceURL=webpack:///./js/components/interface/logo/Logo.less?");

/***/ }),

/***/ 2797:
/***/ (function(module, exports, __webpack_require__) {

eval("exports = module.exports = __webpack_require__(24)(undefined);\n// imports\n\n\n// module\nexports.push([module.i, \".dark-orange {\\n  color: #fc401a;\\n}\\n.orange {\\n  color: #fc6320;\\n}\\n.orange-color {\\n  color: #fc6320;\\n}\\n.orange-color-bg {\\n  background-color: #fc6320;\\n}\\n#geppettologo {\\n  top: 12px;\\n  height: 37px;\\n  left: 33px;\\n  position: absolute;\\n  z-index: 3;\\n  color: #fc6320;\\n  font-size: 33px;\\n}\\n#geppettologo:hover {\\n  text-decoration: none;\\n  color: red;\\n  text-shadow: none;\\n  -webkit-transition: 2000ms linear 0s;\\n  -moz-transition: 2000ms linear 0s;\\n  -o-transition: 2000ms linear 0s;\\n  transition: 2000ms linear 0s;\\n  outline: 0 none;\\n}\\n@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {\\n  #geppettologo {\\n    background-size: 170px 37px;\\n  }\\n}\\n\", \"\"]);\n\n// exports\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./node_modules/css-loader!./node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-default/colors'\"}}!./js/components/interface/logo/Logo.less\n// module id = 2797\n// module chunks = 18\n\n//# sourceURL=webpack:///./js/components/interface/logo/Logo.less?./node_modules/css-loader!./node_modules/less-loader/dist/cjs.js?%7B%22modifyVars%22:%7B%22url%22:%22'../../../extensions/geppetto-default/colors'%22%7D%7D");

/***/ })

});