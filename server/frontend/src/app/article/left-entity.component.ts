import { Component, Input, Output,EventEmitter } from '@angular/core';



@Component({
  selector: 'left-entity',
  template: `
      <md-toolbar color="primary">
        <p>Showing only Criminal articles </p>
        <md-toolbar-row style="height:36px" >   
          <button md-button (click)="setTagAll()" >All</button>
          <button md-button (click)="setTagTagged()">Train</button>
          <button md-button (click)="setTagUntagged()">Test</button>
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