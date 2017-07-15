import { Component, Input } from '@angular/core';


@Component({
    selector: 'score',
    providers: [],
    template: `
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">{{title}}</h3>
        </div>
        <table class="table table-hover" *ngIf="scores">
            <thead>
                <tr>
                    <th> Label </th>
                    <th> Precision </th>
                    <th> Recall </th>
                    <th> f score </th>
                    <th> support </th>
                </tr>
            </thead>
            <tbody>
                <tr *ngFor="let score of scores; let i=index" >
                    <td>   
                        <b *ngIf="labels"> {{labels[i]}} </b> 
                        <b *ngIf="!labels"> {{i}} </b> 
                    </td>
                    <td> {{ (score.precision * 100.0).toFixed(2) }}% </td>
                    <td> {{ (score.recall * 100.0).toFixed(2) }}% </td>
                    <td> {{ (score.fscore * 100.0).toFixed(2) }}% </td>
                    <td> {{ score.support }} </td>
                </tr>
            <tbody>
        </table>
        <div class="panel-body" *ngIf="!scores">
            <p> There are no scores available </p>
        </div> 
    </div>
    `,
    styles:[`

    `]
})

export class ScoreComponent {
    @Input() title : string
    @Input() scores : any[]
    @Input() labels: any[]


  
  
}