import { Component, Input, Output,EventEmitter } from '@angular/core';
import { ArticlesService } from '../services/articles.service';


@Component({
  selector: 'article-editor',
  providers: [ArticlesService],
  template: `
  <md-sidenav-container style="height:100vh;">
    <md-sidenav #sidenav mode="side" opened="true">
      <left-panel
        [todo]="todo"
        [count]="count"
        (setArticle)="getArticle($event)"
        (filterArticles)="getArticleList($event)"
      ></left-panel>
    </md-sidenav>

    <md-sidenav #sidenav mode="side" opened="true" align="end">
      <right-panel
        (setTag)="setTag($event)"
      ></right-panel>
    </md-sidenav>

    <div class="workspace" *ngIf="article">
      <md-toolbar>
        <md-select placeholder="Category" 
          [(ngModel)]="article.category" >
            <md-option *ngFor="let category of categories" [value]="category">
              {{ category }}
            </md-option>
          </md-select>
        
        <md-input-container>
          <input mdInput placeholder="Location" [(ngModel)]="article.location" disabled="true">
        </md-input-container>
        <button md-raised-button color="primary" (click)="saveArticle()">
          Save
        </button>
      </md-toolbar>
      <workspace
        [tag]= "tag" 
        [color]= "color" 
        [article]= "article" 
      ></workspace>
    </div>

  </md-sidenav-container>
  
    
    `,
    styles:[`

    `]
})

export class ArticleEditorComponent {
    title = 'main';
    tag = "Per";
    color = "warn";

    todo : any[];
    count : number;

    article: any;
    filters: any;

    categories = [ "Criminal","Other","Criminal-Other" ];

    ngOnInit(): void{
    // this.getArticleList()
    }

    setTag(obj:any):void{
    this.tag = obj.tag;
    this.color = obj.color;
    }

    getArticleList(filters: any):void{
    this.filters = filters;
    var self = this;
    this.articleService.listArticles(filters).then(function(response){
        self.todo = response.data; 
        self.count = response.count;
        if( self.todo.length > 0 ){
        self.getArticle(self.todo[0].id);
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
