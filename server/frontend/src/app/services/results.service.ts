import { Injectable } from '@angular/core';

import { Headers, Http , RequestOptions} from '@angular/http';


import 'rxjs/add/operator/toPromise';

@Injectable()
export class ResultsService {

   constructor(private http: Http) { }
     
   resultsUrl = "http://127.0.0.1:5000/results"
   runIdentifierUrl = "http://127.0.0.1:5000/runIdentifier"


    getResults(): Promise<any>{

        return this.http.get(this.resultsUrl)
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



    handleError(){
        console.log("HTTP ERROR")
    }



}