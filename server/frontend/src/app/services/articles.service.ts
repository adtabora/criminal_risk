import { Injectable } from '@angular/core';
import {tagged_word} from '../article/word.class'
import { Headers, Http , RequestOptions} from '@angular/http';


import 'rxjs/add/operator/toPromise';

@Injectable()
export class ArticlesService {

   constructor(private http: Http) { }
     
   listUrl = "http://127.0.0.1:5000/article/list"
   getUrl = "http://127.0.0.1:5000/article/get/"
   saveUrl = "http://127.0.0.1:5000/article/save"

    listTopicArticles(filters: any): Promise<any>{
        let headers = new Headers({ 'Content-Type': 'application/json' });

        let body = filters;

        let options = new RequestOptions({ 
            headers: headers,
            params: body,
         });

        return this.http.get(this.listUrl, options)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }

    listEntityArticles(filters: any): Promise<any>{
        let headers = new Headers({ 'Content-Type': 'application/json' });

        let body = filters;

        let options = new RequestOptions({ 
            headers: headers,
            params: body,
         });

        return this.http.get(this.listUrl, options)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }

    getArticle(id:number): any{
        return this.http.get(this.getUrl+id)
               .toPromise()
               .then(function(response){
                    
                    return response.json();
               })
               .catch(this.handleError);
    }

   
    saveArticle(article:any): any{
        let headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });

        return this.http.post(this.saveUrl,article, options)
               .toPromise()
               .then(function(response){
                    
                    return response.json();
               })
               .catch(this.handleError);
    }

    handleError(){
        console.log("HTTP ERROR")
    }



}