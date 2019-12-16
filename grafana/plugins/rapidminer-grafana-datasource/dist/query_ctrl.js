'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.GenericDatasourceQueryCtrl = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _sdk = require('app/plugins/sdk');

require('./css/query-editor.css!');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var GenericDatasourceQueryCtrl = exports.GenericDatasourceQueryCtrl = function (_QueryCtrl) {
  _inherits(GenericDatasourceQueryCtrl, _QueryCtrl);

  function GenericDatasourceQueryCtrl($scope, $injector) {
    _classCallCheck(this, GenericDatasourceQueryCtrl);

    var _this = _possibleConstructorReturn(this, (GenericDatasourceQueryCtrl.__proto__ || Object.getPrototypeOf(GenericDatasourceQueryCtrl)).call(this, $scope, $injector));

    _this.scope = $scope;
    _this.target.target = _this.target.target || 'select metric';
    _this.target.type = _this.target.type || 'timeserie';
    // the available parameters for the given webservice
    _this.target.parameters = [];

    return _this;
  }

  _createClass(GenericDatasourceQueryCtrl, [{
    key: 'getOptions',
    value: function getOptions(query) {

      // console.log(this.datasource.metricFindQuery(query || ''));

      return this.datasource.metricFindQuery(query || '');
    }
  }, {
    key: 'toggleEditorMode',
    value: function toggleEditorMode() {
      this.target.rawQuery = !this.target.rawQuery;
    }
  }, {
    key: 'onChangeInternal',
    value: function onChangeInternal() {
      console.log("ON CHANGE INTERNAL");
      this.panelCtrl.refresh(); // Asks the panel to refresh data.
    }
  }, {
    key: 'onChangeTarget',
    value: function onChangeTarget() {

      this.target.parameters = [];

      var that = this;

      //REWORK here to promise chain

      var data = this.datasource.getParameterKeys(this.target.target);
      var parameters = data.then(function (parameterArray) {

        parameterArray.forEach(function (element) {
          element['value'] = null;
        });

        that.target.parameters = parameterArray;
        console.log(that.target.parameters);
      }).finally(function (parameterArray) {
        that.onChangeInternal();
      });
    }
  }, {
    key: 'onChangeTargetParameters',
    value: function onChangeTargetParameters() {
      console.log("onChangeTargetParameters");
      console.log(this.target.parameters);
      console.log("Before updating the target");
      console.log(this.target.target);

      // clear the previous query parameter list

      var indexOfQueryParams = this.target.target.indexOf('?');
      // if there are parameters
      if (indexOfQueryParams >= 0) {
        this.target.target = this.target.target.substring(0, indexOfQueryParams);
      }

      this.target.target = this.target.target.concat('?');

      for (var i = 0; i < this.target.parameters.length; i++) {
        var parameter = this.target.parameters[i];

        if (parameter['value'] === null || parameter['value'] === '') {
          continue;
        }

        this.target.target = this.target.target.concat(parameter['key'] + '=' + parameter['value']);

        if (i !== this.target.parameters.length - 1) {
          this.target.target = this.target.target.concat('&');
        }
      }

      console.log("After updating the target");
      console.log(this.target.target);

      console.log("all targets");
      console.log(this.target);

      this.onChangeInternal();
    }
  }]);

  return GenericDatasourceQueryCtrl;
}(_sdk.QueryCtrl);

GenericDatasourceQueryCtrl.templateUrl = 'partials/query.editor.html';
//# sourceMappingURL=query_ctrl.js.map
