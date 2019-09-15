import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';
import {map} from 'rxjs/operators';


@Component({
  selector: 'app-input-handle',
  templateUrl: './input-handle.component.html',
  styleUrls: ['./input-handle.component.css']
})

export class InputHandleComponent{

  url = '35.199.43.207';
  startLoc: string;
  endLoc: string;
  server_response : any;
  coords: Float32Array;
  streetnames : string[];


  constructor(private http:HttpClient) { }

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

  private extractData(res: Response){
    let body = res;
    return body || {};
  }

  addAll(sl : string, el : string) {
    this.addStartLoc(sl);
    this.addEndLoc(el);
    console.log(sl);
    console.log(el);
    var query = {
      "start" : {
        "type" : "address",
        "address" : sl
      },
      "end" : {
        "type" : "address",
        "address" : el
      }
    };
    console.log(query);
    this.server_response = this.http.post<JSON>(this.url + '/route', query);
    console.log(this.server_response)
    //console.log(this.server_response["path"]["coords"])
  }

}