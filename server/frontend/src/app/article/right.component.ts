import { Component,Output,EventEmitter } from '@angular/core';



@Component({
  selector: 'right-panel',
  template: `
  <div style="margin:10px">
    <md-chip-list class="mat-chip-list-stacked">
      <md-chip color="warn" selected="true" (click)="selectLoc()" >
        Loc
      </md-chip>
      <md-chip color="accent" selected="true" (click)="selectPer()" >
        Per
      </md-chip>
      <md-chip color="primary" selected="true" (click)="selectOrg()" >
        Org
      </md-chip>
      <md-chip color="none" selected="true" (click)="selectMisc()" >
        Misc
      </md-chip>
    </md-chip-list>
  </div>
    
    `
})

export class RightPanelComponent {
  title = 'right';

  @Output() setTag = new EventEmitter<any>();

  selectLoc():void{
    this.setTag.emit({
      tag:"Loc",
      color:"warn"
    });
  }

  selectPer():void{
    this.setTag.emit({
      tag:"Per",
      color:"accent"
    });
  }

  selectOrg():void{
    this.setTag.emit({
      tag:"Org",
      color:"primary"
    });
  }

  selectMisc():void{
    this.setTag.emit({
      tag:"Misc",
      color:"none"
    });
  }
  
}
