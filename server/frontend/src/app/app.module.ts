import { NgModule, ApplicationRef, CUSTOM_ELEMENTS_SCHEMA }      from '@angular/core';
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
import {MdProgressSpinnerModule} from '@angular/material';
import {MdChipsModule} from '@angular/material'
import {MdInputModule, MdSelectModule} from '@angular/material';
import {MdTabsModule} from '@angular/material';
import {MdCheckboxModule} from '@angular/material';
import {MdCardModule} from '@angular/material';


import { AppComponent }  from './app.component';
import { ArticleEditorComponent }  from './article/article-editor.component';
import { LeftPanelComponent }  from './article/left.component';
import { LeftTopicComponent }  from './article/left-topic.component';
import { LeftEntityComponent }  from './article/left-entity.component';
import { RightPanelComponent }  from './article/right.component';
import { WorkspaceComponent }  from './article/workspace.component';


import { MapComponent }  from './map/map.component';
import { AgmCoreModule } from '@agm/core';

import { ResultsComponent }  from './result/results.component';
import { ScoreComponent }  from './result/score.component';



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
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyDii8HwHTwPH5vHYile-uNOQexmeOoMS74'
    }),
    //material
    MdButtonModule,MdButtonToggleModule,
    MdListModule,
    MdIconModule,MdSidenavModule,
    MdChipsModule, MdToolbarModule,
    MdInputModule, MdSelectModule, MdCheckboxModule,
    MdProgressSpinnerModule,
    MdTabsModule,MdCardModule,
    RouterModule.forRoot(appRoutes)
  ],
  declarations: [
    AppComponent,
    ArticleEditorComponent,  RightPanelComponent, WorkspaceComponent, 
    LeftPanelComponent, LeftTopicComponent,LeftEntityComponent,
    MapComponent, 
    ResultsComponent,ScoreComponent
  ],
  bootstrap: [ AppComponent ],
  schemas:  [ CUSTOM_ELEMENTS_SCHEMA ]
  
})
export class AppModule { }



