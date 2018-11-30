import { Injectable } from '@angular/core';

import { Headers, Http , RequestOptions} from '@angular/http';


import 'rxjs/add/operator/toPromise';

@Injectable()
export class ResultsService {

   constructor(private http: Http) { }
     
   identifierResultsUrl = "http://127.0.0.1:5000/identifier/results"
   runIdentifierUrl = "http://127.0.0.1:5000/identifier/run"

   topicResultsUrl = "http://127.0.0.1:5000/topic/results"
   runTopicUrl = "http://127.0.0.1:5000/topic/run"

   relationshipsResultsUrl = "http://127.0.0.1:5000/relationships/results"
   relationshipsTopicUrl = "http://127.0.0.1:5000/relationships/run"


    getIdentifierResults(): Promise<any>{
        return this.http.get(this.identifierResultsUrl)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }

    runIdentifier(): Promise<any>{
        return this.http.get(this.runIdentifierUrl)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }

    getTopicResults(): Promise<any>{
        return this.http.get(this.topicResultsUrl)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }

    runTopic(): Promise<any>{
        return this.http.get(this.runTopicUrl)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }

    getRelationshipsResults(): Promise<any>{
        return this.http.get(this.relationshipsResultsUrl)
               .toPromise()
               .then(function(response){
                    return response.json();
               })
               .catch(this.handleError);
    }

    runRelationships(): Promise<any>{
        return this.http.get(this.relationshipsTopicUrl)
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