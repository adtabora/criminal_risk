import { Component } from '@angular/core';
import { ResultsService } from '../services/results.service';

@Component({
  selector: 'results',
  providers: [ResultsService],
  template: `
  <div class="container-fluid">
    
    <h3> Topic Classifier <small> </small>
      <button md-button md-raised-button (click)="runTopic()" color="primary">
        Run Classifier
      </button>
    </h3>
    <hr style="margin-top:0px">
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores" 
          [scores]="topicScore.train" 
          [labels]="['Criminal']"
        ></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores"
          [scores]="topicScore.test" 
          [labels]="['Criminal']"
        ></score>
      </div>
    </div>

    
    
    <h3> Location Identifier <small>Entity based</small>
      <button md-button md-raised-button (click)="runIdentifier()" color="primary">
        Run Identifier
      </button>
    </h3>
    
    <hr style="margin-top:0px">
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores" 
              [scores]="entityScore.train" 
              [labels]="['Location Entity']"
        ></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores" 
          [scores]="entityScore.test"
          [labels]="['Location Entity']"
        ></score>
      </div>
    </div>

    <h3> Location Identifier <small>IOB token based</small></h3>
    <hr style="margin-top:0px">
    <div class="row" >
      <div  class="col-sm-6">
        <score title="Train Scores" 
          [scores]="tokenScore.train"
          [labels]="['B-Loc','I-Loc']"
        ></score>
      </div>
      <div  class="col-sm-6">
        <score title="Test Scores" 
          [scores]="tokenScore.test"
          [labels]="['B-Loc','I-Loc']"
        ></score>
      </div>
    </div>

    <h3> Classifiers <small>IOB token classifiers</small></h3>
    <hr style="margin-top:0px">

    <div *ngFor="let clf of lvl1_scores; let i = index">
      <h4> Classifier {{i}} </h4>
      <div class="row" >
        <div  class="col-sm-6">
          <score title="Train Scores"
            [scores]="clf.train"
            [labels]="['B-Loc','I-Loc']"
          ></score>
        </div>
        <div  class="col-sm-6">
          <score title="Test Scores"
            [scores]="clf.test"
            [labels]="['B-Loc','I-Loc']"
          ></score>
        </div>
      </div>
    </div>


  </div>
  <div class="white-div" *ngIf="waiting" > 
    <md-progress-spinner mode="indeterminate"></md-progress-spinner>
  </div>
  
    `,
  styles:[`

  md-progress-spinner {
    position: absolute;
    left: 50%;
    top: 50%;
  }

  .white-div {
    position: fixed;
    top: 0%;
    left: 0%;
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.51);
  }
  


  `]

})

export class ResultsComponent {

  constructor(private resultsService: ResultsService) { }

  scores = [{
        class:"Criminal",
        precision: 93.43,
        recall: 85.45,
        fscore: 88.4
    }]

    entityScore = { train:<any>null, test: <any>null}
    tokenScore = { train:<any>null, test: <any>null}
    topicScore = { train:<any>null, test: <any>null}

    lvl1_scores = <any>[]

    waiting = false

  ngOnInit(): void{
    this.getResults();
  }

  getResults(): void{
    var self = this
    this.resultsService.getIdentifierResults().then(function(response){
        //formating for component input
        self.entityScore.train = [response.entity_score.train];
        self.entityScore.test = [response.entity_score.test];

        //token score
        self.tokenScore = response.lvl2;

        //lvl1
        self.lvl1_scores = response.lvl1;
    });

    this.resultsService.getTopicResults().then(function(response){
        self.topicScore = response.lvl2
    });
  }

  runIdentifier(): void{
    var self = this
    this.waiting = true
    this.resultsService.runIdentifier().then(function(response){
      self.waiting = false
      console.log(response)
      //formating for component input
      self.entityScore.train = [response.entity_score.train];
      self.entityScore.test = [response.entity_score.test];

      //token score
      self.tokenScore = response.lvl2;

      //lvl1
      self.lvl1_scores = response.lvl1;

    });
  }

  runTopic(): void{
    var self = this
    this.waiting = true
    this.resultsService.runTopic().then(function(response){
      self.waiting = false
      self.topicScore = response.lvl2
    });
  }

  
  
  
}
