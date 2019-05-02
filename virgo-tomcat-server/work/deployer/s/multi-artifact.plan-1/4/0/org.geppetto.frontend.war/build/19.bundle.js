webpackJsonp([19],{

/***/ 1063:
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {\n    __webpack_require__(3097);\n    var React = __webpack_require__(1);\n\n    var linkButton = React.createClass({\n        displayName: 'linkButton',\n\n        render: function render() {\n            var customStyle = {\n                left: this.props.left != undefined ? this.props.left : '41px',\n                top: this.props.top != undefined ? this.props.top : '415px'\n            };\n\n            var iconClass = \"fa {0}\".format(this.props.icon);\n\n            return React.createElement(\n                'div',\n                { id: 'github' },\n                React.createElement(\n                    'a',\n                    { href: this.props.url, target: '_blank' },\n                    React.createElement('icon', { className: iconClass, id: 'git', style: customStyle })\n                )\n            );\n        }\n    });\n\n    return linkButton;\n}.call(exports, __webpack_require__, exports, module),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/linkButton/LinkButton.js\n// module id = 1063\n// module chunks = 19\n\n//# sourceURL=webpack:///./js/components/interface/linkButton/LinkButton.js?");

/***/ }),

/***/ 3097:
/***/ (function(module, exports, __webpack_require__) {

eval("// style-loader: Adds some css to the DOM by adding a <style> tag\n\n// load the styles\nvar content = __webpack_require__(3098);\nif(typeof content === 'string') content = [[module.i, content, '']];\n// add the styles to the DOM\nvar update = __webpack_require__(25)(content, {});\nif(content.locals) module.exports = content.locals;\n// Hot Module Replacement\nif(false) {\n\t// When the styles change, update the <style> tags\n\tif(!content.locals) {\n\t\tmodule.hot.accept(\"!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\\\"modifyVars\\\":{\\\"url\\\":\\\"'../../../extensions/geppetto-default/colors'\\\"}}!./LinkButton.less\", function() {\n\t\t\tvar newContent = require(\"!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\\\"modifyVars\\\":{\\\"url\\\":\\\"'../../../extensions/geppetto-default/colors'\\\"}}!./LinkButton.less\");\n\t\t\tif(typeof newContent === 'string') newContent = [[module.id, newContent, '']];\n\t\t\tupdate(newContent);\n\t\t});\n\t}\n\t// When the module is disposed, remove the <style> tags\n\tmodule.hot.dispose(function() { update(); });\n}\n\n//////////////////\n// WEBPACK FOOTER\n// ./js/components/interface/linkButton/LinkButton.less\n// module id = 3097\n// module chunks = 19\n\n//# sourceURL=webpack:///./js/components/interface/linkButton/LinkButton.less?");

/***/ }),

/***/ 3098:
/***/ (function(module, exports, __webpack_require__) {

eval("exports = module.exports = __webpack_require__(24)(undefined);\n// imports\n\n\n// module\nexports.push([module.i, \".dark-orange {\\n  color: #fc401a;\\n}\\n.orange {\\n  color: #fc6320;\\n}\\n.orange-color {\\n  color: #fc6320;\\n}\\n.orange-color-bg {\\n  background-color: #fc6320;\\n}\\n#github icon {\\n  color: #fc6320;\\n  position: fixed;\\n  text-decoration: none;\\n  font-size: 20px;\\n}\\n#github icon:hover {\\n  color: #fc401a;\\n}\\n\", \"\"]);\n\n// exports\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./node_modules/css-loader!./node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-default/colors'\"}}!./js/components/interface/linkButton/LinkButton.less\n// module id = 3098\n// module chunks = 19\n\n//# sourceURL=webpack:///./js/components/interface/linkButton/LinkButton.less?./node_modules/css-loader!./node_modules/less-loader/dist/cjs.js?%7B%22modifyVars%22:%7B%22url%22:%22'../../../extensions/geppetto-default/colors'%22%7D%7D");

/***/ })

});