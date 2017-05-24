import { Component,Input } from '@angular/core';
import {tagged_word} from './word.class'



@Component({
  selector: 'workspace',
  template: `
    <div style="display:flex;flex-wrap:wrap; margin:10px; font-size:x-large;">
      <word-tag *ngFor="let w of article.title; let word_i=index"
            [attr.id]=" '_' + word_i"
            [word]="w" 
            (click) = "tagTitleWord(word_i)"
        > 
      </word-tag>
    </div>
  
    <div>
      <div *ngFor="let sentence of article.sentences; let sent_i=index" style="display:flex;flex-wrap:wrap">
        <word-tag *ngFor="let w of sentence; let word_i=index"
            [attr.id]="sent_i + '_' + word_i"

            [word]="w" 
            (click) = "tagContentWord(sent_i,word_i)"
        > 
        </word-tag>
        <br/>
        <br/>
      </div>
    </div>
    `,
    styles:[`
    .word:hover {
        background-color: lightblue;
    }
    `]
})

export class WorkspaceComponent {
  @Input() tag: String
  @Input() color: String
  @Input() article: any


  tagContentWord(sent_id: number,  word_id: number ): void{
    var sentence = this.article.sentences[sent_id]
    this.article.sentences[sent_id] = this.tag_word(sentence, word_id)
  }

  tagTitleWord( word_id: number ): void{
    var sentence = this.article.title
    this.article.title = this.tag_word(sentence, word_id)
  }


  // Tagger
  tag_word(sentence: Array<any>, word_id: number ){
    var tag : String;
    let word = sentence[word_id];

    // check if it is the same tag which in that case put a none tag
    if (word.tag.substr(2) == this.tag){
      sentence[word_id] = {
        word: word.word,
        tag: "none"
      };
      console.log("none");
      //check the next word and correct it if necessary
      if ( sentence.length -1 > word_id){
        let next = sentence[word_id+1]
        if ( next.tag == tag ){
          sentence[word_id +1].tag = "B-" + this.tag
        }
      }

      return sentence
    }

    // check if the word is the first of its tag type
    if (word_id == 0){
      tag = "B-" + this.tag;
    }else{
      let before = sentence[word_id-1];
      if( before.tag.substr(2) == this.tag ){
        tag = "I-" + this.tag;
      } else{
        tag = "B-" + this.tag;
      }
    }

    //if the word is the first of its tag type check and correct the next one
    if ( tag[0] == "B" && sentence.length -1 > word_id){
      let next = sentence[word_id+1]
      if ( next.tag == tag ){
        sentence[word_id +1].tag = "I-" + this.tag
      }
    }

    // create a new object because this way it will trigger the update routine
    sentence[word_id] = {
      word: word.word, 
      tag:  tag
    };
    
    return sentence
  }

  
  
  

   
  
}
