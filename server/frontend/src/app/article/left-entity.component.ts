import { Component, Input, Output,EventEmitter } from '@angular/core';



@Component({
  selector: 'left-entity',
  template: `
      <md-toolbar color="primary">
        <p>Showing only Criminal articles </p>
        <md-toolbar-row style="height:36px" >   
          <button md-button (click)="setTrain()">Train</button>
          <button md-button (click)="setTest()">Test</button>
        </md-toolbar-row>

        <md-toolbar-row style="height:36px" >    
          <button md-button (click)="subtract()">
            <md-icon md-list-icon>chevron_left</md-icon>
          </button>      
          <p style="font-size:small;">  showing {{offset + "-" + (offset+limit)  }} of {{count}} </p>
          <button md-button (click)="add()">
            <md-icon md-list-icon>chevron_right</md-icon>
          </button>  
        </md-toolbar-row>
      </md-toolbar>

      <md-nav-list dense *ngIf="list" style="height:60%;overflow-y:scroll" >
        <h3 md-subheader>Search Result</h3>
        <md-list-item *ngFor="let article of list"
          (click)="selectArticle(article)">
            <md-icon md-list-icon>folder</md-icon>
            <p md-line class="demo-2"> {{article.title}} </p>
        </md-list-item>
      </md-nav-list >
    
  
    
    `,
    styles:[`
      md-toolbar-row: {
        height: 36px;
      }
      .test: {
        height: 36px;
      }
    `]
})

export class LeftEntityComponent {
  @Input() list : any[];
  @Input() count : number;
  @Output() setArticle = new EventEmitter<Number>();
  @Output() filterArticles = new EventEmitter<any>();

  categories = ["all","None", "Criminal","Other","Criminal-Other" ];

  datasetFilter = "train";
  offset = 0;
  limit = 100;

  selectArticle(article:any):void{
    this.setArticle.emit(article.id)
  }
  
  changeFilters():void{    
    this.filterArticles.emit({
      dataset: this.datasetFilter
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
    this.datasetFilter = "train"
    this.changeFilters()
  }
  setTest():void{
    this.datasetFilter = "test"
    this.changeFilters()
  }




  
}
