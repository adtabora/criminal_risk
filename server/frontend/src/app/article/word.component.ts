import { Component,Input } from '@angular/core';
import {tagged_word} from './word.class'

@Component({
  selector: 'word-tag',
  template: `
    <div class="text-word" *ngIf="!tagged">
        {{word.word}}&nbsp;
    </div>
    <md-chip selected="true" *ngIf="tagged" [color]="color">
        {{word.word}}
    </md-chip>
    `,
    styles:[`
    .text-word:hover {
        background-color: lightblue;
    }
    `]
})

export class WordComponent {
    @Input() word: tagged_word
    tagged= false
    color: string
    ngOnInit(): void{
        let colors = {
            Loc: "warn",
            Per: "accent",
            Org: "primary",
            Misc: "none",
        }
        if( this.word.tag == "none"){
            this.tagged = false
        }else{
            this.tagged = true
            this.color = colors[ this.word.tag.substr(2) ]
        }
    }
}