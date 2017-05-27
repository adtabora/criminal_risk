import { Component, Input, Output,EventEmitter } from '@angular/core';



@Component({
  selector: 'left-panel',
  template: `
      <md-tab-group (selectChange)="handleTabChange($event)">
        <md-tab label="Topic Explorer">
          <left-topic [list]="topicList" [count]="topicCount" ></left-topic>
        </md-tab>
        <md-tab label="Entity Explorer">
          <left-entity [list]="entityList" [count]="entityCount"></left-entity>
        </md-tab>
      </md-tab-group>
    `,
    styles:[`
      md-toolbar-row {
        height: 36px;
      }
      .test {
        height: 36px;
      }
     
    `]
})

export class LeftPanelComponent {
  @Input() topicList : any[];
  @Input() topicCount : number;
  @Input() entityList : any[];
  @Input() entityCount : number;

  @Output() setArticle = new EventEmitter<Number>();
  @Output() filterArticles = new EventEmitter<any>();
  @Output() selectTab = new EventEmitter<string>();

  categories = ["all","None", "Criminal","Other","Criminal-Other" ];

  categoryFilter: String
  tagFilter = "all"
  offset = 0
  limit = 100

  // Event emitters when the tab is changed

  handleTabChange( tab: any):void{
    if (tab.index == 0){
      this.selectTab.emit("topic");
    }else{
      this.selectTab.emit("entity");
    }
  }


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
