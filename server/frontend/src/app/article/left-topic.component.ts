import { Component, Input, Output,EventEmitter } from '@angular/core';



@Component({
  selector: 'left-topic',
  template: `
    <div class="filter-header" style="display:grid;">
      <div class="filter-check">
      <md-checkbox [(ngModel)]="tp" (change)="changeFilters()" >True Positives</md-checkbox>
      <md-checkbox [(ngModel)]="fp" (change)="changeFilters()" >False Positives</md-checkbox>
      </div>
      <div class="filter-check">
      <md-checkbox [(ngModel)]="tn" (change)="changeFilters()" >True Negatives</md-checkbox>
      <md-checkbox [(ngModel)]="fn" (change)="changeFilters()" >False Negatives</md-checkbox>
      </div>
    </div>
    <div class="filter-header">
      <button md-button (click)="setTrain()">Train</button>
      <button md-button (click)="setTest()">Test</button>
    </div>

    <div class="filter-header" >
      <button md-button (click)="subtract()">
        <md-icon md-list-icon>chevron_left</md-icon>
      </button>      
      <p style="font-size:small;">  showing {{offset + "-" + (offset+limit)  }} of {{count}} </p>
      <button md-button (click)="add()">
        <md-icon md-list-icon>chevron_right</md-icon>
      </button>  
    </div>

  <md-list dense *ngIf="list" style="height:60%;overflow-y:scroll" >
    <h3 md-subheader>Search Result</h3>
    <md-list-item *ngFor="let article of list"
      (click)="selectArticle(article)">
        <md-icon md-list-icon>folder</md-icon>
        <p md-line class="demo-2"> {{article.title}} </p>
    </md-list-item>
  </md-list>
    
    `,
    styles:[`
      .filter-header {
        width: 100%;
        background-color: #00bcd4;
        color: #fff;
        display: flex;
        align-items: center;
      } 
      .filter-buttons {
        width: 100%;
        background-color: #00bcd4;
        color: #fff;
        display: flex;
        align-items: center;
      }
      
      .filter-check {
        margin-left: 10px;
      }

      label {
        font-weight: 100;
      }


      
    `]
})

export class LeftTopicComponent {
  @Input() list : any[];
  @Input() count : number;
  @Output() setArticle = new EventEmitter<Number>();
  @Output() filterArticles = new EventEmitter<any>();

  tp = true;
  fp = false;
  tn = false;
  fn = false;
  dataset = "train";

  
  offset = 0
  limit = 100

  selectArticle(article:any):void{
    this.setArticle.emit(article.id)
  }
  
  changeFilters():void{
    var self = this;
    this.filterArticles.emit({
        tp: self.tp,
        fp: self.fp,
        tn: self.tn,
        fn: self.fn,
        dataset: self.dataset
    })
  }

  subtract():void{
    if (this.offset != 0){
      this.offset -= 100
    }
    this.changeFilters()
  }

  add():void{
    if (this.offset+100 < this.count ){
      this.offset += 100
      this.changeFilters()
    }
  }

  setTrain():void{
    this.dataset = "train"
    this.changeFilters()
  }
  setTest():void{
    this.dataset = "test"
    this.changeFilters()
  }

 

  
}
