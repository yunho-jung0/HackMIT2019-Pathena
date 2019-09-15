import {Component} from '@angular/core';


@Component({
  selector: 'app-input-handle',
  templateUrl: './input-handle.component.html',
  styleUrls: ['./input-handle.component.css']
})
export class InputHandleComponent{

  startLoc: string;
  endLoc: string;

  constructor() { }

  addStartLoc(sl : string){
    if (sl) {
      this.startLoc = sl;
    }
  }
  addEndLoc(el : string){
    if (el) {
      this.endLoc = el;
    }
  }

  addAll(sl : string, el : string) {
    this.addStartLoc(sl);
    this.addEndLoc(el);
  }

}