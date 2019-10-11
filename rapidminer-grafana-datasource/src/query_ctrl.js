import {QueryCtrl} from 'app/plugins/sdk';
import './css/query-editor.css!'

export class GenericDatasourceQueryCtrl extends QueryCtrl {

  constructor($scope, $injector)  {
    super($scope, $injector);

    this.scope = $scope;
    this.target.target = this.target.target || 'select metric';
    this.target.type = this.target.type || 'timeserie';
    // the available parameters for the given webservice
    this.target.params = [];

  }

  getOptions(query) {
    return this.datasource.metricFindQuery(query || '');
  }

  toggleEditorMode() {
    this.target.rawQuery = !this.target.rawQuery;
  }

  onChangeInternal() {
    this.panelCtrl.refresh(); // Asks the panel to refresh data.
  }

  onChangeTarget() {


    var that = this;

    let data = this.datasource.getParameterKeys(this.target.target);
    // 'data' is a Promise
    let parameters = data.then(function(value) {
      // 'value' is an array
      // let params = [];
      // value.forEach(parameter => {
      //   params.push(parameter);
      // });
      
      that.target.params = value;
      that.onChangeInternal();
      
    });
    // this.target.params = parameters.then();
    setTimeout(() => {
      console.log(this.target.params );
    }, 1000);
    
    // this.onChangeInternal();

  }

}

GenericDatasourceQueryCtrl.templateUrl = 'partials/query.editor.html';

