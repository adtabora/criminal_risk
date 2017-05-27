import { Component, Input, Output,EventEmitter } from '@angular/core';



@Component({
  selector: 'left-topic',
  template: `
    <div class="filter-header" style="display:grid;">
      <div class="filter-check">
      <md-checkbox>True Positives</md-checkbox>
      <md-checkbox>False Positives</md-checkbox>
      </div>
      <div class="filter-check">
      <md-checkbox>True Negatives</md-checkbox>
      <md-checkbox>False Negatives</md-checkbox>
      </div>
    </div>
    <div class="filter-header">
      <button md-button (click)="setTagAll()" >All</button>
      <button md-button (click)="setTagTagged()">Train</button>
      <button md-button (click)="setTagUntagged()">Test</button>
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

  categoryFilter: String
  tagFilter = "all"
  offset = 0
  limit = 100

  selectArticle(article:any):void{
    this.setArticle.emit(article.id)
  }
  
  changeFilters():void{
    var category = this.categoryFilter
    
    
    this.filterArticles.emit({
      category: category,
      tag: this.tagFilter,
      offset: this.offset,
      limit: this.limit
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

  setTagAll():void{
    this.tagFilter = "all"
    this.changeFilters()
  }

  setTagTagged():void{
    this.tagFilter = "tagged"
    this.changeFilters()
  }

  setTagUntagged():void{
    this.tagFilter = "untagged"
    this.changeFilters()
  }

  
}
