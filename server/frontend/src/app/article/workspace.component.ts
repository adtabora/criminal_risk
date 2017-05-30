import { Component,Input } from '@angular/core';

@Component({
  selector: 'workspace',
  template: `
  <div class="workspace">
    <md-toolbar>
      <md-input-container>
        <input mdInput placeholder="Gold Category" [value]="goldTopic" disabled>
      </md-input-container>
      <md-input-container>
        <input mdInput placeholder="Predicted Category" [value]="predTopic" disabled>
      </md-input-container>
    </md-toolbar>

    <md-card style="margin:10px" *ngIf="entityTab">
        <h3> Legend </h3>
        <p>
          <span class="bg-success legend"> True Positive </span>
          <span class="legend"> True Negative </span>
          <span class="bg-danger legend"> False Positive </span>
          <span class="bg-warning legend"> False Negative </span>
        </p>

    </md-card>

    <md-card style="margin:10px">
      <h1> {{title}} </h1>
    <div class="article-content">
      <p *ngFor="let sentence of sentences">
        <span *ngFor="let chunk of sentence" [class]="chunk[1]">
          <span class="bracket-left-red" *ngIf="chunk[2]=='begin-red' ">[</span>
          <span class="bracket-left-green" *ngIf="chunk[2]=='begin-green' ">[</span>
        
          {{chunk[0]}}
          <span class="bracket-right-red" *ngIf="chunk[3]=='end-red' ">]</span>
          <span class="bracket-right-green" *ngIf="chunk[3]=='end-green' ">]</span>
          
        </span> 
      </p>
    </div>
    </md-card>
  </div>
    `,
    styles:[`
    .word:hover {
        background-color: lightblue;
    }
    label {
      font-weight: 100;
    }
    md-toolbar {
      margin: 16px
    }
    md-input-container {
      margin-right: 10px
    }
    span {
      padding: 5px;
    }
    .legend {
      margin-right: 20px
    }

    .TP {
      background-color: #dff0d8;
    }

    .FP {
      background-color: #f2dede;
    }

    .FN {
      background-color: #fcf8e3;
    }

    .TN {
      background-color: #ffffff;
    }

    .bracket-left-red {
      font-size: xx-large;
      color: red;
      margin-right: 0px;
    }
    .bracket-right-red {
      font-size: xx-large;
      color: red;
      margin-left: 0px;
    }
    .bracket-left-green {
      font-size: xx-large;
      color: green;
      margin-right: 0px;
    }
    .bracket-right-green {
      font-size: xx-large;
      color: green;
      margin-left: 0px;
    }

    `]
})

export class WorkspaceComponent {
  @Input() goldTopic : string
  @Input() predTopic : string
  @Input() title : string
  @Input() entityTab: boolean
  @Input() sentences : any[];

  ngOnInit(): void{
    
  }

 
  

   
  
}
