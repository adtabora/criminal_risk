import { Component, Input, Output,EventEmitter } from '@angular/core';
import { ArticlesService } from '../services/articles.service';


@Component({
  selector: 'article-editor',
  providers: [ArticlesService],
  template: `
  <md-sidenav-container style="height:100vh;">
    <md-sidenav #sidenav mode="side" opened="true">
      <left-panel
        [topicList]= "topicList" 
        [topicCount]= "topicCount"
        [entityList]= "entityList"
        [entityCount]= "entityCount"

        (setArticle)="getArticle($event)"
        (filterArticles)="getArticleList($event)"
        (selectTab)="setTab($event)"
      ></left-panel>
    </md-sidenav>

    <div class="workspace" >      
      <workspace *ngIf="article" 
        [artId] = "article.art_id"
        [title] = "article.title"
        [sentences] = "article.sentences"
        [entityTab] = "entityTab"
        [goldTopic] = "article.gold" 
        [predTopic] = "article.pred" 
      ></workspace>
    </div>

  </md-sidenav-container>
  
    
    `,
    styles:[`

    `]
})

export class ArticleEditorComponent {
    article = {};
    
    entityTab: boolean;
    topicList: any[];
    topicCount: number;
    topicFilters = {
            tp: true,
            fp: false,
            tn: false,
            fn: false,
            dataset: "train"
        };
    entityList: any[];
    entityCount: number;
    entityFilters = { dataset: "train"};


    filters: any;


    ngOnInit(): void{
        this.getTopicList(this.topicFilters);
    }

    setTab(tab: string):void{
        if (tab == "entity"){
            this.entityTab = true;
            this.topicList= []
            this.getEntityList(this.entityFilters)
        }else{
            this.entityTab = false;
            this.entityList= []
            this.getTopicList(this.topicFilters)
        }
    }

    //general function
    getArticleList(filters: any ):void {
        
        if (this.entityTab){
            this.entityFilters = filters; 
            this.getEntityList(filters);
        }else{
            //save the filters to re-use them when changing tabs
            this.topicFilters = filters; 
            this.getTopicList(filters);
        }

    }

    getTopicList(filters: any):void{
        this.filters = filters;
        var self = this;
        this.articleService.listTopicArticles(filters).then(function(response){
            self.topicList = response.data; 
            self.topicCount = response.count;
            if( self.topicList.length > 0 ){
                self.getTopicArticle(self.topicList[0].id);
            } else {
                self.article = null
            }
        });
    }

    getTopicArticle(id:number):void{
        var self = this;
        this.articleService.getTopicArticle(id).then(function(article:any){
            self.article = article
        });
    }

    getEntityList(filters: any):void{
        this.filters = filters;
        var self = this;
        this.articleService.listEntityArticles(filters).then(function(response){
            self.entityList = response.data; 
            self.entityCount = response.count;
            if( self.entityList.length > 0 ){
                self.getArticle(self.entityList[0].id);
            } else {
                self.article = null
            }
        });
    }

    getArticle(id:number):void{
        var self = this;
        if (this.entityTab){
            this.articleService.getEntityArticle(id).then(function(article:any){
                self.article = article

            });
        } else {
            this.articleService.getTopicArticle(id).then(function(article:any){
                self.article = article
            });
        }
    }


    constructor(private articleService: ArticlesService) { }



  
}
