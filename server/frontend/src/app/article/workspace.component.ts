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
          {{chunk[0]}}
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

    `]
})

export class WorkspaceComponent {
  @Input() goldTopic : string
  @Input() predTopic : string
  @Input() title : string
  @Input() entityTab: boolean
  @Input() sentences : any[];

  ngOnInit(): void{{
    this.sentences.forEach(sentence => {
      for (var i = 0; i < sentence.length; i++) {
        switch (sentence[i][1]){
          case "TP":
            sentence[i][1] = "bg-success";
            break;
          case "FP":
            sentence[i][1] = "bg-danger";
            break;
          case "TN":
            sentence[i][1] = "";
            break;
          case "FN":
            sentence[i][1] = "bg-warning";
            break;    
        }
      }
    });
  }

 
  

   
  
}
