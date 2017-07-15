import { Injectable } from '@angular/core';

import { Headers, Http , RequestOptions} from '@angular/http';


import 'rxjs/add/operator/toPromise';

@Injectable()
export class ArticlesService {

   constructor(private http: Http) { }
     
   listTopicUrl = "http://127.0.0.1:5000/topic/list"
   getTopicUrl = "http://127.0.0.1:5000/topic/get/"

   listEntityUrl = "http://127.0.0.1:5000/entity/list"
   getEntityUrl = "http://127.0.0.1:5000/entity/get/"

    listTopicArticles(filters: any): Promise<any>{
        let headers = new Headers({ 'Content-Type': 'application/json' });
        let body = filters;
        let options = new RequestOptions({ 
            headers: headers,
            params: body,
         });

        return this.http.get(this.listTopicUrl, options)
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

        return this.http.get(this.listEntityUrl, options)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }
   
    getTopicArticle(id:number): any{
        return this.http.get(this.getTopicUrl+id)
               .toPromise()
               .then(function(response){
                    
                    return response.json();
               })
               .catch(this.handleError);
    }

    getEntityArticle(id:number): any{
        return this.http.get(this.getEntityUrl+id)
               .toPromise()
               .then(function(response){
                    
                    return response.json();
               })
               .catch(this.handleError);
    }

    handleError(error: any){
        console.log("HTTP ERROR")
        console.log(error)
    }



}