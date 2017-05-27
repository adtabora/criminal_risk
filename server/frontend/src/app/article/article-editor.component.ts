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
      <workspace
        [title] = "article.title"
        [sentences] = "article.sentences"
        [entityTab] = "entityTab"
        [goldTopic] = "article.goldTopic" 
        [predTopic] = "article.predTopic" 
      ></workspace>
    </div>

  </md-sidenav-container>
  
    
    `,
    styles:[`

    `]
})

export class ArticleEditorComponent {
    article = {
        title:  "Un perrito se escapa de su casa!" ,
        goldTopic: "Criminal",
        predTopic: "Criminal",
        sentences :[ 
            [
            ["En horas de la madrugada se encontró en la colonia", "TN"],
            ["Miramontes","TP"],
            ["el prerrito", "TN"],
            ["Sean", "FP"],
            ["quien se habia escapado de su casa en", "TN"],
            ["Loarque", "FN"],
            [".", "TN"]
            ]
        ]
    };
    
    entityTab: boolean;
    topicList: any[];
    topicCount: number;
    entityList: any[];
    entityCount: number;


    filters: any;


    ngOnInit(): void{
    // this.getArticleList()
    }

    setTab(tab: string):void{
        if (tab == "entity"){
            this.entityTab = true;
            this.topicList= []
        }else{
            this.entityTab = false;
            this.entityList= []
        }
    }

    getTopicList(filters: any):void{
        this.filters = filters;
        var self = this;
        this.articleService.listTopicArticles(filters).then(function(response){
            self.topicList = response.data; 
            self.topicCount = response.count;
            if( self.topicList.length > 0 ){
                self.getArticle(self.topicList[0].id);
            } else {
                self.article = null
            }
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
    this.articleService.getArticle(id).then(function(article:any){
        // console.log("----")
        // console.log(article)
        self.article = article

    });
    }

    saveArticle():void{
    var self = this;
    this.article.reviewed = this.isArticleTagged();
    this.articleService.saveArticle(this.article )
    .then(function(response:any){
        // console.log("----")
        // console.log(response)
        self.getArticleList(self.filters);

    });
    }

    //TODO: implement this function
    isArticleTagged():Boolean{
    for (var i = 0; i < this.article.sentences.length; i++) {
        var sentence = this.article.sentences[i];
        for (var j = 0; j < sentence.length; j++) {
        if(sentence[j].tag != "none"){
            return true;
        }
        }
    }
    return false
    }

    moveToDone(article: any){


    let index = this.todo.findIndex(art=> art.id = article.id);
    console.log("INDEX-----")
    console.log(index)
    if (index > -1) {
        this.todo.splice(index, 1);
    }

    this.getArticle(this.todo[0].id)
    }

    constructor(private articleService: ArticlesService) { }



  
}
