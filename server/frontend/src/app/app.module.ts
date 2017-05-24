import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms'; // <-- NgModel lives here
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { HttpModule }    from '@angular/http';
import { RouterModule, Routes }   from '@angular/router';

// material
import {MdButtonModule, MdButtonToggleModule, MdListModule} from '@angular/material';
import {MdIconModule} from '@angular/material';
import {MdSidenavModule} from '@angular/material'
import {MdToolbarModule} from '@angular/material';


import { AppComponent }  from './app.component';
import { ArticleEditorComponent }  from './article/article-editor.component';
import { LeftPanelComponent }  from './article/left.component';
import { RightPanelComponent }  from './article/right.component';
import { WorkspaceComponent }  from './article/workspace.component';
import { WordComponent }  from './article/word.component';

import { MapComponent }  from './map/map.component';
import { ResultsComponent }  from './result/results.component';
import { ScoreComponent }  from './result/score.component';

import {MdChipsModule} from '@angular/material'
import {MdInputModule, MdSelectModule} from '@angular/material';

const appRoutes: Routes = [
  {
    path: 'article',
    component: ArticleEditorComponent
  },{
    path: 'map',
    component: MapComponent
  },{
    path: 'results',
    component: ResultsComponent
  }
]

@NgModule({
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule, // <-- import the FormsModule before binding with [(ngModel)]
    HttpModule,
    //material
    MdButtonModule,MdButtonToggleModule,
    MdListModule,
    MdIconModule,MdSidenavModule,
    MdChipsModule, MdToolbarModule,
    MdInputModule, MdSelectModule,
    RouterModule.forRoot(appRoutes)
  ],
  declarations: [
    AppComponent,
    ArticleEditorComponent, LeftPanelComponent, RightPanelComponent, WorkspaceComponent, WordComponent, 
    MapComponent, 
    ResultsComponent,ScoreComponent
  ],
  bootstrap: [ AppComponent ],
  
})
export class AppModule { }



