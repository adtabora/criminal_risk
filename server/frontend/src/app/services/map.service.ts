import { Injectable } from '@angular/core';

import { Headers, Http , RequestOptions} from '@angular/http';


import 'rxjs/add/operator/toPromise';

@Injectable()
export class MapService {

   constructor(private http: Http) { }
     
   listPointsUrl = "http://127.0.0.1:5000/map/list"
   


    listPoints(): Promise<any>{
        return this.http.get(this.listPointsUrl)
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