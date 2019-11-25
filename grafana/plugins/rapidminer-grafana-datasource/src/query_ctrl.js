import {QueryCtrl} from 'app/plugins/sdk';
import './css/query-editor.css!'

export class GenericDatasourceQueryCtrl extends QueryCtrl {

  constructor($scope, $injector)  {
    super($scope, $injector);

    this.scope = $scope;
    this.target.target = this.target.target || 'select metric';
    this.target.type = this.target.type || 'timeserie';
    // the available parameters for the given webservice
    this.target.parameters = [];

  }

  getOptions(query) {

    // console.log(this.datasource.metricFindQuery(query || ''));

    return this.datasource.metricFindQuery(query || '');
  }

  toggleEditorMode() {
    this.target.rawQuery = !this.target.rawQuery;
  }

  onChangeInternal() {
    console.log("ON CHANGE INTERNAL")
    this.panelCtrl.refresh(); // Asks the panel to refresh data.
  }

  onChangeTarget() {

    this.target.parameters = [];

    var that = this;

    //REWORK here to promise chain

    let data = this.datasource.getParameterKeys(this.target.target);
    let parameters = data.then(function(parameterArray) {

      parameterArray.forEach(element => {
        element['value'] = null;
      });
      
      that.target.parameters = parameterArray;
      console.log(that.target.parameters);
      
    }).finally(function(parameterArray) {
      that.onChangeInternal();
    });
  }

  onChangeTargetParameters() {
    console.log("onChangeTargetParameters");
    console.log(this.target.parameters);
    console.log("Before updating the target");
    console.log(this.target.target);

    // clear the previous query parameter list

    let indexOfQueryParams = this.target.target.indexOf('?')
    // if there are parameters
    if (indexOfQueryParams >= 0) {
      this.target.target = this.target.target.substring(0, indexOfQueryParams);
    }

    this.target.target = this.target.target.concat('?');

    for (let i = 0; i < this.target.parameters.length; i++) {
      let parameter = this.target.parameters[i];

      if (parameter['value'] === null || parameter['value'] === '') {
        continue;
      }

      this.target.target = this.target.target.concat(
        parameter['key'] + '=' + parameter['value']
      )

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
}

GenericDatasourceQueryCtrl.templateUrl = 'partials/query.editor.html';

