import { Component } from '@angular/core';


@Component({
  selector: 'results',
  providers: [],
  template: `
  
  <div class="container-fluid">
    
    <h3> Topic Classifier <small> </small></h3>
    <hr style="margin-top:0px">
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores" [scores]="scores"></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"></score>
      </div>
    </div>

    
    <h3> Location Identifier <small>Entity based</small></h3>
    <hr style="margin-top:0px">
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores"></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"></score>
      </div>
    </div>

    <h3> Location Identifier <small>IOB token based</small></h3>
    <hr style="margin-top:0px">
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores"></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"></score>
      </div>
    </div>

    <h3> Classifiers <small>IOB token classifiers</small></h3>
    <hr style="margin-top:0px">

    <h4> Classifier 1 </h4>
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores"></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"></score>
      </div>
    </div>

    <h4> Classifier 2 </h4>
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores"></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"></score>
      </div>
    </div>

    <h4> Classifier 3 </h4>
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores"></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"></score>
      </div>
    </div>

    <h4> Stacked Classifier </h4>
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores"></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"></score>
      </div>
    </div>

  </div>
    `,
  styles:[`


  `]

})

export class ResultsComponent {

  scores = [{
        class:"Criminal",
        precision: 93.43,
        recall: 85.45,
        f1: 88.4
    }]
  
  
}
