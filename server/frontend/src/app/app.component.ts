import { Component } from '@angular/core';


@Component({
  selector: 'my-app',
  providers: [],
  template: `
  <div>
  <md-toolbar color="primary">
    <md-icon md-list-icon>memory</md-icon>
    <button md-button routerLink="/results">Results</button>
    <button md-button routerLink="/article">Article Viewer</button>
    <button md-button routerLink="/map">Map Viewer</button>
  </md-toolbar>
  </div>

  <router-outlet></router-outlet>
    `,
  styles:[`
    my-app {
      position: absolute;
    }

    .container {
      display: flex; 
    }

    md-input-container{
      margin-left:10px
    }

    button{
      margin-left:20px
    }

    .right {
      background:lightcyan;
      min-width: 140px;
      max-width: 200px;
      padding: 1em;
    }

    .workspace {
      background:lightyellow;
      padding: 1em;
      width: 100%;
    }

  `]

})

export class AppComponent {
  
  
}
