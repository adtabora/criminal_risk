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
                    <th> Class </th>
                    <th> Precision </th>
                    <th> Recall </th>
                    <th> f1 </th>
                </tr>
            </thead>
            <tbody>
                <tr *ngFor="let score of scores" >
                    <td> <b>Criminal </b> </td>
                    <td> {{score.precision}}% </td>
                    <td> {{score.recall}}% </td>
                    <td> {{score.f1}}% </td>
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


  
  
}