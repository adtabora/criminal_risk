import { Component, Input, Output,EventEmitter } from '@angular/core';



@Component({
  selector: 'left-panel',
  template: `
      <md-tab-group (selectChange)="handleTabChange($event)">
        <md-tab label="Topic Explorer">
          <left-topic 
            [list]="topicList" 
            [count]="topicCount" 
            (setArticle)="selectArticle($event)"
            (filterArticles)="changeFilters($event)" 
          ></left-topic>
        </md-tab>
        <md-tab label="Entity Explorer">
          <left-entity 
            [list]="entityList" 
            [count]="entityCount"
            (setArticle)="selectArticle($event)"
            (filterArticles)="changeFilters($event)"
            ></left-entity>
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

  // Event emitters when the tab is changed

  handleTabChange( tab: any):void{
    if (tab.index == 0){
      this.selectTab.emit("topic");
    }else{
      this.selectTab.emit("entity");
    }
  }


  selectArticle(art_id:number):void{
    this.setArticle.emit(art_id)
  }
  
  changeFilters(filters: any):void{
    this.filterArticles.emit(filters);
  }



  
}
